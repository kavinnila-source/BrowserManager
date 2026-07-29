import time
import psutil

from browser_statistics import (
    stats,
    lock,
    update_ram,
    update_cpu,
    update_health,
)
from notification_manager import high_ram, high_cpu
from config import (
    MAX_RAM_MB,
    MAX_CPU_PERCENT,
)


def calculate_health(ram_mb: float, cpu_percent: float) -> str:
    """Return browser health status."""

    if ram_mb >= MAX_RAM_MB:
        return "🟡 High RAM"

    if cpu_percent >= MAX_CPU_PERCENT:
        return "🟠 High CPU"

    return "🟢 Healthy"


def monitor_system(stop_event):
    """Continuously monitor browser resource usage."""

    while not stop_event.is_set():

        with lock:
            browser_list = list(stats.items())

        for worker_id, data in browser_list:

            pid = data.get("pid")

            if pid in ("-", None):
                continue

            try:
                process = psutil.Process(pid)

                total_ram = process.memory_info().rss
                total_cpu = process.cpu_percent(interval=0.1)

                for child in process.children(recursive=True):
                    try:
                        total_ram += child.memory_info().rss
                        total_cpu += child.cpu_percent(interval=0.1)
                    except (
                        psutil.NoSuchProcess,
                        psutil.AccessDenied,
                    ):
                        continue

                ram_mb = total_ram / (1024 * 1024)

                update_ram(worker_id, f"{ram_mb:.1f} MB")
                update_cpu(worker_id, f"{total_cpu:.1f}%")
                health=calculate_health(ram_mb,total_cpu)
                update_health(worker_id,health)
                if "High RAM" in health:
                    high_ram(worker_id,f"{ram_mb:.1f} MB")
                elif "High CPU" in health:
                    high_cpu(worker_id,f"{total_cpu:.1f}%")

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ):
                update_ram(worker_id, "-")
                update_cpu(worker_id, "-")
                update_health(worker_id, "🔴 Offline")

        stop_event.wait(2)
