import threading
import signal
import sys
import time

from config import (
    NUMBER_OF_WINDOWS,
    STARTUP_DELAY_SECONDS,
)

from browser_worker import run_browser
from utils.logger import log
from browser_statistics import print_statistics
from system_monitor import monitor_system
from flask import Flask
from threading import Thread
from browser_statistics import stats

app = Flask(__name__)


@app.route("/")
def dashboard():

    html = """
    <html>
    <head>
        <meta http-equiv="refresh" content="2">
        <title>BrowserManager Dashboard</title>
    </head>
    <body>
        <h1>🚀 BrowserManager Live Dashboard</h1>
        <hr>
    """

    for worker_id, data in stats.items():

        html += f"""
        <div style="border:1px solid #ccc;
                    padding:15px;
                    margin:15px;
                    border-radius:10px;">

        <h2>Browser {worker_id}</h2>

        Status : {data.get('status','-')}<br>
        Health : {data.get('health','-')}<br>
        URL : {data.get('url','-')}<br>
        Title : {data.get('title','-')}<br>
        RAM : {data.get('ram','-')}<br>
        CPU : {data.get('cpu','-')}<br>

        </div>
        """

    html += "</body></html>"

    return html

def start_dashboard():
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False,
    )

stop_event = threading.Event()
threads = []


def shutdown(signum=None, frame=None):
    log("Shutdown requested...")

    stop_event.set()

    for t in threads:
        if t.is_alive():
            t.join(timeout=5)

    log("All browsers stopped.")
    sys.exit(0)


def main():

    signal.signal(signal.SIGINT, shutdown)

    try:

        log("=" * 60)
        log("BrowserManager v1.8 Live Dashboard")
        log("=" * 60)

        monitor_thread = threading.Thread(
            target=monitor_system,
            args=(stop_event,),
            daemon=True,
        )
        monitor_thread.start()
        threads.append(monitor_thread)

        for worker_id in range(1, NUMBER_OF_WINDOWS + 1):

            thread = threading.Thread(
                target=run_browser,
                args=(worker_id, stop_event),
                daemon=True,
            )

            thread.start()
            threads.append(thread)

            log(f"Browser {worker_id} thread started.")

            if worker_id < NUMBER_OF_WINDOWS:
                log(
                    f"Waiting {STARTUP_DELAY_SECONDS} second(s) "
                    "before starting next browser..."
                )
                stop_event.wait(STARTUP_DELAY_SECONDS)

        log(f"{NUMBER_OF_WINDOWS} browser workers started.")

        last_stats = 0

        while not stop_event.is_set():

            now = time.time()

            if now - last_stats >= 5:
                print_statistics()
                last_stats = now

            for thread in threads:
                if not thread.is_alive() and thread is not monitor_thread:
                    log("A worker thread stopped unexpectedly.")

            stop_event.wait(1)

    except KeyboardInterrupt:
        shutdown()

    except Exception as e:
        log(f"Manager ERROR: {e}")
        shutdown()


if __name__ == "__main__":

    dashboard_thread = Thread(
        target=start_dashboard,
        daemon=True
    )
    dashboard_thread.start()

    log("🌐 Web Dashboard Started : http://127.0.0.1:5000")

    main()
