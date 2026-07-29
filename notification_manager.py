"""
notification_manager.py
Step 9 Notification Manager
"""

import time
import threading
from collections import deque

# Maximum notifications stored
MAX_NOTIFICATIONS = 100

# Thread-safe notification queue
_notifications = deque(maxlen=MAX_NOTIFICATIONS)
_lock = threading.Lock()


def add_notification(level, title, message):
    """
    Add a notification.

    Levels:
        success
        info
        warning
        error
    """

    notification = {
        "time": time.strftime("%H:%M:%S"),
        "level": level,
        "title": title,
        "message": message,
    }

    with _lock:
        _notifications.appendleft(notification)

    return notification


def get_notifications():
    """
    Return all notifications (newest first)
    """

    with _lock:
        return list(_notifications)


def clear_notifications():
    """
    Remove all notifications
    """

    with _lock:
        _notifications.clear()


def notification_count():
    """
    Total notifications currently stored.
    """

    with _lock:
        return len(_notifications)


# --------------------------------------------------
# Browser Helper Functions
# --------------------------------------------------

def browser_started(worker_id):
    add_notification(
        "success",
        "Browser Started",
        f"Browser {worker_id} started successfully."
    )


def browser_stopped(worker_id):
    add_notification(
        "info",
        "Browser Stopped",
        f"Browser {worker_id} stopped."
    )


def browser_restarted(worker_id, reason):
    add_notification(
        "warning",
        "Browser Restarted",
        f"Browser {worker_id} restarted. Reason: {reason}"
    )


def browser_crashed(worker_id, reason):
    add_notification(
        "error",
        "Browser Crashed",
        f"Browser {worker_id} crashed. Reason: {reason}"
    )


def high_ram(worker_id, ram):
    add_notification(
        "warning",
        "High RAM Usage",
        f"Browser {worker_id} RAM usage: {ram:.1f} MB"
    )


def high_cpu(worker_id, cpu):
    add_notification(
        "warning",
        "High CPU Usage",
        f"Browser {worker_id} CPU usage: {cpu:.1f}%"
    )


def slow_page(worker_id, load_time):
    add_notification(
        "warning",
        "Slow Page",
        f"Browser {worker_id} page load time: {load_time:.2f} sec"
    )


def driver_error(worker_id, error):
    add_notification(
        "error",
        "Driver Error",
        f"Browser {worker_id}: {error}"
    )


# --------------------------------------------------
# Optional
# --------------------------------------------------

def latest_notification():
    """
    Return latest notification or None
    """

    with _lock:
        if not _notifications:
            return None

        return _notifications[0]