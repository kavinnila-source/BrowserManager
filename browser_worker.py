import os
import random
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait

from config import (
    URLS,
    MIN_ACTIVE_MINUTES,
    MAX_ACTIVE_MINUTES,
    RESTART_DELAY_MINUTES,
    MIN_WIDTH,
    MAX_WIDTH,
    MIN_HEIGHT,
    MAX_HEIGHT,
    MIN_X,
    MAX_X,
    MIN_Y,
    MAX_Y,
    PROFILE_FOLDER,
)

from logger import log
from user_agents import get_random_user_agent
from health_monitor import is_browser_alive
from browser_activity import random_scroll
from mouse_activity import random_mouse_movement


def run_browser(worker_id, stop_event):
    while not stop_event.is_set():
        driver = None

        try:
            log(f"Browser {worker_id} Starting...")

            # Base directory
            base_dir = os.path.dirname(os.path.abspath(__file__))

            # Geckodriver path
            gecko_path = os.path.join(
                base_dir,
                "drivers",
                "geckodriver.exe"
            )

            # Firefox profile path
            profile_path = os.path.join(
                base_dir,
                PROFILE_FOLDER,
                f"profile_{worker_id}"
            )

            # Create profile folder
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

            # Profile
            options.add_argument("-profile")
            options.add_argument(profile_path)

            # Random User Agent
            user_agent = get_random_user_agent()

            options.set_preference(
                "general.useragent.override",
                user_agent,
            )

            log(f"Browser {worker_id} User-Agent: {user_agent}")

            driver = webdriver.Firefox(
                service=service,
                options=options,
            )

            # Random window size
            width = random.randint(MIN_WIDTH, MAX_WIDTH)
            height = random.randint(MIN_HEIGHT, MAX_HEIGHT)

            # Random window position
            x = random.randint(MIN_X, MAX_X)
            y = random.randint(MIN_Y, MAX_Y)

            driver.set_window_size(width, height)
            driver.set_window_position(x, y)

            selected_url = random.choice(URLS)

            log(f"Browser {worker_id} Opening {selected_url}")

            driver.get(selected_url)

            # Wait until page loads
            WebDriverWait(driver, 60).until(
                lambda d: d.execute_script(
                    "return document.readyState"
                ) == "complete"
            )

            active_minutes = random.randint(
                MIN_ACTIVE_MINUTES,
                MAX_ACTIVE_MINUTES,
            )

            log(
                f"Browser {worker_id} Active for "
                f"{active_minutes} minute(s)"
            )

            # Initial human activity
            random_scroll(driver)
            log(f"Browser {worker_id} Initial scrolling completed.")

            #random_mouse_movement(driver)
            #log(f"Browser {worker_id} Initial mouse movement completed.")

            next_scroll = random.randint(15, 40)

            # Keep browser open
            for second in range(active_minutes * 60):

                if stop_event.is_set():
                    break

                if not is_browser_alive(driver, worker_id):
                    log(f"Browser {worker_id} is not responding.")
                    break

                if second >= next_scroll:

                    random_scroll(driver)
                    log(f"Browser {worker_id} Random scrolling completed.")

                    #random_mouse_movement(driver)
                    #log(f"Browser {worker_id} Random mouse movement completed.")

                    next_scroll = second + random.randint(15, 40)

                time.sleep(1)

        except Exception as e:
            log(f"Browser {worker_id} ERROR: {e}")

        finally:
            if driver is not None:
                log(f"Browser {worker_id} Closing...")
                driver.quit()
                log(f"Browser {worker_id} Closed")

        if stop_event.is_set():
            break

        log(
            f"Browser {worker_id} Restarting in "
            f"{RESTART_DELAY_MINUTES} minute(s)..."
        )

        for _ in range(RESTART_DELAY_MINUTES * 60):
            if stop_event.is_set():
                break
            time.sleep(1)
