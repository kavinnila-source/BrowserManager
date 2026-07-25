import random
import time


def random_mouse_movement(driver):
    """
    Marionette-safe mouse activity.

    Firefox + Selenium sometimes throws errors with
    ActionChains.move_by_offset(), so for now we simulate
    user activity using small random pauses only.

    This keeps the browser session looking active without
    risking browser crashes.
    """

    try:
        moves = random.randint(3, 6)

        for _ in range(moves):
            time.sleep(random.uniform(0.5, 2.0))

        return True

    except Exception:
        return False