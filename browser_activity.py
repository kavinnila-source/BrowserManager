import random
import time


def random_scroll(driver):
    """
    Human-like random scrolling
    """

    scrolls = random.randint(3, 8)

    for _ in range(scrolls):

        pixels = random.randint(200, 700)

        driver.execute_script(
            f"window.scrollBy(0, {pixels});"
        )

        time.sleep(
            random.uniform(2, 5)
        )

    return True