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
from threading import Thread
from dashboard.web_dashboard import start_dashboard


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
