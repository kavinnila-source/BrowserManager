import os
import random
import time
import psutil

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait


from config import (
    URLS,
    MIN_ACTIVE_MINUTES,
    MAX_ACTIVE_MINUTES,
    MIN_RESTART_DELAY_MINUTES,
    MAX_RESTART_DELAY_MINUTES,
    MIN_WIDTH,
    MAX_WIDTH,
    MIN_HEIGHT,
    MAX_HEIGHT,
    MIN_X,
    MAX_X,
    MIN_Y,
    MAX_Y,
    PROFILE_FOLDER,
    MIN_ZOOM,
    MAX_ZOOM,
)

from logger import log
from user_agents import (
    get_random_user_agent,
    format_user_agent,
)
from health_monitor import is_browser_alive
from browser_activity import human_reading

from statistics import (
    register_browser,
    update_status,
    update_url,
    increment_restart,
    update_zoom,
    update_window_size,
    update_user_agent,
    update_pid,
)


def run_browser(worker_id, stop_event):
    while not stop_event.is_set():
        driver = None

        try:
            log(f"Browser {worker_id} Starting...")

            register_browser(worker_id)
            update_status(worker_id, "Starting")

            base_dir = os.path.dirname(os.path.abspath(__file__))

            gecko_path = os.path.join(
                base_dir,
                "drivers",
                "geckodriver.exe"
            )

            profile_path = os.path.join(
                base_dir,
                PROFILE_FOLDER,
                f"profile_{worker_id}"
            )

            os.makedirs(profile_path, exist_ok=True)

            service = Service(gecko_path)

            options = Options()

            # Firefox Preferences
            options.set_preference("dom.webnotifications.enabled", False)
            options.set_preference("signon.rememberSignons", False)
            options.set_preference("toolkit.telemetry.enabled", False)
            options.set_preference(
                "browser.crashReports.unsubmittedCheck.autoSubmit2",
                False,
            )
            options.set_preference(
                "app.shield.optoutstudies.enabled",
                False,
            )

            options.add_argument("-profile")
            options.add_argument(profile_path)

            user_agent = get_random_user_agent()

            options.set_preference(
                "general.useragent.override",
                user_agent,
            )

            update_user_agent(
                worker_id,
                format_user_agent(user_agent),
            )

            log(f"Browser {worker_id} User-Agent: {user_agent}")

            driver = webdriver.Firefox(
                 service=service,
                 options=options,
            )    

            gecko_pid = driver.service.process.pid
            firefox_pid = gecko_pid

            try:
                gecko = psutil.Process(gecko_pid)
                time.sleep(1)

                for child in gecko.children(recursive=True):
                    try:
                        if child.name().lower() == "firefox.exe":
                            firefox_pid = child.pid
                            break
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

            update_pid(worker_id, firefox_pid)

            width = random.randint(MIN_WIDTH, MAX_WIDTH)
            height = random.randint(MIN_HEIGHT, MAX_HEIGHT)

            x = random.randint(MIN_X, MAX_X)
            y = random.randint(MIN_Y, MAX_Y)

            driver.set_window_size(width, height)
            driver.set_window_position(x, y)

            update_window_size(worker_id, width, height)

            selected_url = random.choice(URLS)

            log(f"Browser {worker_id} Opening {selected_url}")

            driver.get(selected_url)

            update_url(worker_id, selected_url)
            update_status(worker_id, "Running")

            WebDriverWait(driver, 60).until(
                lambda d: d.execute_script(
                    "return document.readyState"
                ) == "complete"
            )

            # Apply random browser zoom
            zoom = random.randint(MIN_ZOOM, MAX_ZOOM)

            driver.execute_script(
                f"document.body.style.zoom='{zoom}%'"
            )

            update_zoom(worker_id, f"{zoom}%")

            log(f"Browser {worker_id} Zoom set to {zoom}%")

            active_minutes = random.randint(
                MIN_ACTIVE_MINUTES,
                MAX_ACTIVE_MINUTES,
            )

            log(
                f"Browser {worker_id} Active for "
                f"{active_minutes} minute(s)"
            )

            # Initial activity
            human_reading(driver)
            log(f"Browser {worker_id} Initial human reading completed.")

            next_activity = random.randint(15, 40)

            for second in range(active_minutes * 60):

                if stop_event.is_set():
                    break

                if not is_browser_alive(driver, worker_id):
                    log(f"Browser {worker_id} is not responding.")
                    break

                if second >= next_activity:

                    human_reading(driver)
                    log(f"Browser {worker_id} Human reading completed.")

                    next_activity = second + random.randint(15, 40)

                time.sleep(1)

        except Exception as e:
            log(f"Browser {worker_id} ERROR: {e}")

        finally:
            if driver is not None:
                log(f"Browser {worker_id} Closing...")
                update_status(worker_id, "Stopped")
                driver.quit()
                log(f"Browser {worker_id} Closed")

        if stop_event.is_set():
            break

        increment_restart(worker_id)

        restart_delay = random.randint(
            MIN_RESTART_DELAY_MINUTES,
            MAX_RESTART_DELAY_MINUTES,
        )

        log(
            f"Browser {worker_id} Restarting in "
            f"{restart_delay} minute(s)..."
        )

        for _ in range(restart_delay * 60):
            if stop_event.is_set():
                break
            time.sleep(1)