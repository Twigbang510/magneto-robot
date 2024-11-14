from robocorp.tasks import task
import logging
from driver_manager import get_driver
from helper import *

@task
def open_browser(url):
    try: 
        driver = get_driver()
        driver.get(url)
        logger.info("Chrome browser opened")
    except Exception as e:
        logging.error(f"Failed to open browser: {str(e)}")
