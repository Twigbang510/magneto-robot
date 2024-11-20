from robocorp.tasks import task
import logging
from driver_manager import get_driver
from helper import *
import time
RETRIES = 5
DELAY = 3
@task
def open_browser(url):
    for attempt in range(1, RETRIES + 1):
        try:
            logger.info(f"Attempt {attempt} to open browser.")
            driver = get_driver()
            driver.get(url)
            logger.info("Chrome browser opened successfully.")
            return
        except Exception as e:
            logger.error(f"Attempt {attempt} failed: {str(e)}")
            if attempt < RETRIES:
                logger.info(f"Retrying in {DELAY} seconds...")
                time.sleep(DELAY)
            else:
                logger.error("All attempts to open the browser have failed.")
                raise Exception("Failed to open browser after multiple attempts.")
