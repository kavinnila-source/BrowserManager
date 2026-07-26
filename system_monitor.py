import threading
import time
import psutil

from statistics import stats, lock


def monitor_system(stop_event):

    while not stop_event.is_set():

        with lock:

            for worker_id, data in stats.items():

                pid = data.get("pid")

                if pid == "-" or pid is None:
                    continue

                try:
                    process = psutil.Process(pid)

                    ram_mb = process.memory_info().rss / (1024 * 1024)
                    cpu = process.cpu_percent(interval=0)

                    data["ram"] = f"{ram_mb:.1f} MB"
                    data["cpu"] = f"{cpu:.1f}%"

                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess,
                ):
                    data["ram"] = "-"
                    data["cpu"] = "-"

        time.sleep(2)