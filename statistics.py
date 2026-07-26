import threading
import time

stats = {}
lock = threading.Lock()


def register_browser(worker_id):
    with lock:
        stats[worker_id] = {
            "status": "Starting",
            "url": "-",
            "restarts": 0,
            "start_time": time.time(),
        }


def update_status(worker_id, status):
    with lock:
        if worker_id in stats:
            stats[worker_id]["status"] = status


def update_url(worker_id, url):
    with lock:
        if worker_id in stats:
            stats[worker_id]["url"] = url


def increment_restart(worker_id):
    with lock:
        if worker_id in stats:
            stats[worker_id]["restarts"] += 1
            stats[worker_id]["start_time"] = time.time()


def print_statistics():
    with lock:

        print("\033[2J\033[H", end="")

        print("=" * 70)
        print("           BrowserManager v1.6 Live Dashboard")
        print("=" * 70)
        print(f"Updated : {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 70)

        running = 0

        for worker_id in sorted(stats):

            data = stats[worker_id]

            uptime = int(time.time() - data["start_time"])
            minutes = uptime // 60
            seconds = uptime % 60

            if data["status"] == "Running":
                running += 1
                icon = "🟢"
            else:
                icon = "🔴"

            print(f"{icon} Browser {worker_id}")
            print(f"   Status    : {data['status']}")
            print(f"   URL       : {data['url']}")
            print(f"   Uptime    : {minutes:02}:{seconds:02}")
            print(f"   Restarts  : {data['restarts']}")
            print("-" * 70)

        print(f"Running Browsers : {running}/{len(stats)}")
        print("=" * 70)
