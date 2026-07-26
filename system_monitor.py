import time
import psutil

from browser_statistics import (
    stats,
    lock,
    update_ram,
    update_cpu,
)


def monitor_system(stop_event):

    while not stop_event.is_set():

        with lock:
            browser_list = list(stats.items())

        for worker_id, data in browser_list:

            pid = data.get("pid")

            if pid in ("-", None):
                continue

            try:
                process = psutil.Process(pid)

                # Firefox child processes
                children = process.children(recursive=True)

                total_ram = process.memory_info().rss
                total_cpu = process.cpu_percent(interval=0.1)

                for child in children:
                    try:
                        total_ram += child.memory_info().rss
                        total_cpu += child.cpu_percent(interval=0.1)
                    except (
                        psutil.NoSuchProcess,
                        psutil.AccessDenied,
                    ):
                        pass

                ram_mb = total_ram / (1024 * 1024)

                update_ram(worker_id, f"{ram_mb:.1f} MB")
                update_cpu(worker_id, f"{total_cpu:.1f}%")

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ):
                update_ram(worker_id, "-")
                update_cpu(worker_id, "-")

        time.sleep(2)