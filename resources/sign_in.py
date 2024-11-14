from robocorp.tasks import task
import logging
from selenium.webdriver.common.by import By
from helper import click_on_element_by_locator
from driver_manager import get_driver

logger = logging.getLogger(__name__)

@task
def sign_in(email, password):
    """
    Task to sign in to the website using the provided email and password.
    """
    driver = get_driver()
    try:
        # Click on the sign in button
        click_on_element_by_locator(By.CSS_SELECTOR, 'li.authorization-link a')
        logger.info("Clicked on the sign in button.")

        # Enter email
        email_field = driver.find_element(By.ID, 'email')
        email_field.clear()
        email_field.send_keys(email)
        logger.info("Entered email.")

        # Enter password
        password_field = driver.find_element(By.ID, 'pass')
        password_field.clear()
        password_field.send_keys(password)
        logger.info("Entered password.")

        # Submit the login form
        click_on_element_by_locator(By.ID, 'send2')
        logger.info("Submitted login form.")

    except Exception as e:
        logger.error(f"Error in login task: {str(e)}")
