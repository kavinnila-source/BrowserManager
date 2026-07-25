import threading
import time

from browser_worker import run_browser
from config import NUMBER_OF_WINDOWS, STARTUP_DELAY_SECONDS

stop_event = threading.Event()

threads = []

for i in range(NUMBER_OF_WINDOWS):
    t = threading.Thread(
        target=run_browser,
        args=(i + 1, stop_event),
        daemon=True
    )

    t.start()
    threads.append(t)

    # Wait before starting the next browser
    time.sleep(STARTUP_DELAY_SECONDS)

print(f"{NUMBER_OF_WINDOWS} browser workers started.")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping all browser workers...")

    stop_event.set()

    for t in threads:
     t.join(timeout=5)

alive = [t.name for t in threads if t.is_alive()]

if alive:
    print(f"Threads still running: {alive}")
else:
    print("All browser workers stopped.")

print("Shutdown complete.")