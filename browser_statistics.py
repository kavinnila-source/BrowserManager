
import threading
import time
from notification_manager import add_notification, get_notifications

stats = {}
lock = threading.Lock()


def register_browser(worker_id):
    with lock:
        stats[worker_id] = {
            "status":"Starting",
            "url":"-",
            "zoom":"-",
            "window_size":"-",
            "user_agent":"-",
            "title":"-",
            "profile":"-",
            "browser_version":"-",
            "started_at":"-",
            "health":"🟢 Healthy",
            "load_time":"-",
            "pid":"-",
            "ram":"-",
            "cpu":"-",
            "restarts":0,
            "start_time":time.time(),
        }
    add_notification(
    "success",
    "Browser Registered",
    f"Browser {worker_id} registered."
)


def _update(worker_id,key,value):
    with lock:
        if worker_id in stats:
            stats[worker_id][key]=value

def update_status(worker_id,v): _update(worker_id,"status",v)
def update_url(worker_id,v): _update(worker_id,"url",v)
def update_zoom(worker_id,v): _update(worker_id,"zoom",v)
def update_user_agent(worker_id,v): _update(worker_id,"user_agent",v)
def update_title(worker_id,v): _update(worker_id,"title",v)
def update_profile(worker_id,v): _update(worker_id,"profile",v)
def update_browser_version(worker_id,v): _update(worker_id,"browser_version",v)
def update_started_at(worker_id,v): _update(worker_id,"started_at",v)
def update_health(worker_id,v): _update(worker_id,"health",v)
def update_load_time(worker_id,v): _update(worker_id,"load_time",v)
def update_pid(worker_id,v): _update(worker_id,"pid",v)
def update_ram(worker_id,v): _update(worker_id,"ram",v)
def update_cpu(worker_id,v): _update(worker_id,"cpu",v)

def update_window_size(worker_id,width,height):
    _update(worker_id,"window_size",f"{width} x {height}")

def increment_restart(worker_id):
    with lock:
        if worker_id in stats:
            stats[worker_id]["restarts"] += 1
            stats[worker_id]["start_time"] = time.time()
    add_notification(
    "warning",
    "Browser Restarted",
    f"Browser {worker_id} restarted."
)

def get_summary():
    running=0
    total_ram=0.0
    total_cpu=0.0
    healthy=0

    with lock:
        values=list(stats.values())

    for data in values:
        if data["status"]=="Running":
            running+=1
        if "Healthy" in str(data["health"]):
            healthy+=1
        try:
            total_ram+=float(str(data["ram"]).replace(" MB",""))
        except (ValueError, TypeError):
            pass
        try:
            total_cpu+=float(str(data["cpu"]).replace("%",""))
        except (ValueError, TypeError):
            pass

    return {
        "running":running,
        "total":len(values),
        "healthy":healthy,
        "total_ram":round(total_ram,1),
        "total_cpu":round(total_cpu,1),
    }


def print_statistics():
    with lock:
        print("\033[2J\033[H", end="")
        print("="*70)
        print("BrowserManager v2.0 Live Dashboard")
        print("="*70)
        print(f"Updated : {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-"*70)
        for wid,data in sorted(stats.items()):
            print(f"Browser {wid} | {data['status']} | {data['health']} | RAM {data['ram']} | CPU {data['cpu']}")
        print("-"*70)
        print(get_summary())
