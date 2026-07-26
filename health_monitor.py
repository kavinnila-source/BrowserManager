from utils.logger import log


def is_browser_alive(driver, worker_id):
    try:
        driver.current_url
        return True

    except Exception as e:
        log(f"Browser {worker_id} Health Check Failed: {e}")
        return False