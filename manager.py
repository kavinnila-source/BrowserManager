import threading
import signal
import sys

from config import (
    NUMBER_OF_WINDOWS,
    STARTUP_DELAY_SECONDS,
)

from browser_worker import run_browser
from logger import log


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
        log("BrowserManager v1.4 Stable")
        log("=" * 60)

        for worker_id in range(1, NUMBER_OF_WINDOWS + 1):

            thread = threading.Thread(
                target=run_browser,
                args=(worker_id, stop_event),
                daemon=True,
            )

            thread.start()
            threads.append(thread)

            log(f"Browser {worker_id} thread started.")

            # Wait before starting the next browser
            if worker_id < NUMBER_OF_WINDOWS:

                log(
                    f"Waiting {STARTUP_DELAY_SECONDS} second(s) "
                    "before starting next browser..."
                )

                stop_event.wait(STARTUP_DELAY_SECONDS)

        log(f"{NUMBER_OF_WINDOWS} browser workers started.")

        while not stop_event.is_set():

            for thread in threads:

                if not thread.is_alive():
                    log("A worker thread stopped unexpectedly.")

            stop_event.wait(2)

    except KeyboardInterrupt:
        shutdown()

    except Exception as e:
        log(f"Manager ERROR: {e}")
        shutdown()


if __name__ == "__main__":
    main()