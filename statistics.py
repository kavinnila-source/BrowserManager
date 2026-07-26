import threading
import time

stats = {}
lock = threading.Lock()

def register_browser(worker_id):
    with lock:
        stats[worker_id] = {
            "status": "Starting",
            "url": "-",
            "zoom": "-",
            "window_size": "-",
            "user_agent": "-",
            "title": "-",
            "profile": "-",
            "pid": "-",
            "ram": "-",
            "cpu": "-",
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

def update_zoom(worker_id, zoom):
    with lock:
        if worker_id in stats:
            stats[worker_id]["zoom"] = zoom

def update_window_size(worker_id, width, height):
    with lock:
        if worker_id in stats:
            stats[worker_id]["window_size"] = f"{width} x {height}"

def update_user_agent(worker_id, user_agent):
    with lock:
        if worker_id in stats:
            stats[worker_id]["user_agent"] = user_agent

def update_title(worker_id, title):
    with lock:
        if worker_id in stats:
            stats[worker_id]["title"] = title

def update_profile(worker_id, profile):
    with lock:
        if worker_id in stats:
            stats[worker_id]["profile"] = profile

def update_pid(worker_id, pid):
    with lock:
        if worker_id in stats:
            stats[worker_id]["pid"] = pid


def update_ram(worker_id, ram):
    with lock:
        if worker_id in stats:
            stats[worker_id]["ram"] = ram


def update_cpu(worker_id, cpu):
    with lock:
        if worker_id in stats:
            stats[worker_id]["cpu"] = cpu


def increment_restart(worker_id):
    with lock:
        if worker_id in stats:
            stats[worker_id]["restarts"] += 1
            stats[worker_id]["start_time"] = time.time()

def print_statistics():
    with lock:
        print("\033[2J\033[H", end="")
        print("=" * 70)
        print("           BrowserManager v1.8 Live Dashboard")
        print("=" * 70)
        print(f"Updated : {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 70)
        running = 0

        total_ram = 0.0
        total_cpu = 0.0

        for worker_id in sorted(stats):
            data = stats[worker_id]

            try:
                total_ram += float(str(data["ram"]).replace(" MB", ""))
            except:
                pass

            try:
                total_cpu += float(str(data["cpu"]).replace("%", ""))
            except:
                pass

            uptime = int(time.time() - data["start_time"])
            minutes = uptime // 60
            seconds = uptime % 60
            icon = "🟢" if data["status"]=="Running" else "🔴"
            if data["status"]=="Running":
                running +=1
            print(f"{icon} Browser {worker_id}")
            print(f"   Status      : {data['status']}")
            print(f"   URL         : {data['url']}")
            print(f"   Zoom        : {data['zoom']}")
            print(f"   Window      : {data['window_size']}")
            print(f"   User-Agent  : {data['user_agent']}")
            print(f"   Title       : {data['title']}")
            print(f"   Profile     : {data['profile']}")
            print(f"   PID         : {data['pid']}")
            print(f"   RAM         : {data['ram']}")
            print(f"   CPU         : {data['cpu']}")
            print(f"   Uptime      : {minutes:02}:{seconds:02}")
            print(f"   Restarts    : {data['restarts']}")
            print("-"*70)

            print(f"Running Browsers : {running}/{len(stats)}")
            print(f"Total RAM        : {total_ram / 1024:.2f} GB")
            print(f"Total CPU        : {total_cpu:.1f}%")
            print("=" * 70)
