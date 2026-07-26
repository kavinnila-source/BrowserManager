from datetime import datetime
import os
import threading

from config import ENABLE_CONSOLE_LOG

# Thread-safe logging
log_lock = threading.Lock()

# Create logs folder automatically
LOG_FOLDER = "logs"
os.makedirs(LOG_FOLDER, exist_ok=True)

# Daily log file
LOG_FILE = os.path.join(
    LOG_FOLDER,
    f"{datetime.now().strftime('%Y-%m-%d')}.log"
)


def log(message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    text = f"[{now}] {message}"

    with log_lock:

        # Console (Only if enabled)
        if ENABLE_CONSOLE_LOG:
            print(text)

        # File
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(text + "\n")