import random
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException


def human_reading(driver):
    """
    Simulates human reading behavior.

    One call = one activity cycle.
    Control returns to browser_worker.py after completion.
    """

    try:
        # Total scroll actions
        actions = random.randint(4, 8)

        for _ in range(actions):

            # Current page height
            page_height = driver.execute_script(
                "return document.body.scrollHeight"
            )

            # Random scroll distance
            distance = random.randint(200, 700)

            # Scroll down
            driver.execute_script(
                "window.scrollBy(0, arguments[0]);",
                distance
            )

            # Reading pause
            time.sleep(random.uniform(2.0, 5.0))

            # Occasionally scroll slightly upward
            if random.random() < 0.30:

                up = random.randint(100, 300)

                driver.execute_script(
                    "window.scrollBy(0, -arguments[0]);",
                    up
                )

                time.sleep(random.uniform(1.0, 3.0))

            # Occasionally move to a random element
            if random.random() < 0.25:

                try:
                    elements = driver.find_elements(
                        By.TAG_NAME,
                        "a"
                    )

                    if elements:

                        random.choice(elements).location_once_scrolled_into_view
                        time.sleep(random.uniform(1.0, 2.0))

                except Exception:
                    pass

            # Near bottom → return upward slightly
            current = driver.execute_script(
                "return window.pageYOffset;"
            )

            if current > page_height * 0.85:

                driver.execute_script(
                    "window.scrollTo(0, arguments[0]);",
                    int(page_height * random.uniform(0.35, 0.60))
                )

                time.sleep(random.uniform(2.0, 4.0))

    except WebDriverException:
        pass

    except Exception:
        pass