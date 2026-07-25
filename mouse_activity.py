import random
import time

from selenium.webdriver.common.action_chains import ActionChains


def random_mouse_movement(driver):
    """
    Simulate simple human-like mouse movement.
    """

    actions = ActionChains(driver)

    moves = random.randint(5, 10)

    for _ in range(moves):

        x = random.randint(-100, 100)
        y = random.randint(-100, 100)

        try:
            actions.move_by_offset(x, y).perform()
        except Exception:
            # Ignore if movement is outside the viewport
            pass

        time.sleep(random.uniform(0.5, 2.0))

    return True