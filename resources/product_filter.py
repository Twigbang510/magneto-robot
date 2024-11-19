from robocorp.tasks import task
import logging
from selenium.webdriver.common.by import By
from helper import *
from driver_manager import get_driver

logger = logging.getLogger(__name__)

@task
def product_filter(category_id, size, color):
    """
    Task to filter products based on category, size, and color.
    """
    driver = get_driver()
    go_to_category_page(driver, category_id)
    # click_on_position_of_element(By.ID, 'mode-list', 0)
    # choose_size(size)
    # choose_color(color)

def go_to_category_page(driver, category_id):
    """
    Navigate to the specified category page.
    """
    try:
        logger.info("Navigating to the category page.")
        element = wait_until_element_is_visible(By.ID, category_id)
        if element:
            url = element.get_attribute('href')
            driver.get(url)
            logger.info(f"Successfully navigated to category page: {url}")
        else:
            logger.warning(f"Category element with ID {category_id} not found.")
    except Exception as e:
        logger.error(f"Failed to open category page: {str(e)}")

def choose_size(size):
    """
    Select the specified size from the size filter options.
    """
    try:
        click_on_element_by_locator(By.XPATH, "//div[@data-role='title' and text()='Size']")
        logger.info("Opened size filter dropdown.")
        click_on_element_by_locator(By.XPATH, f"//div[@class='swatch-option text ' and @option-label='{size}']")
        logger.info(f"Selected size: {size}")
    except Exception as e:
        logger.error(f"Failed to select size '{size}': {str(e)}")

def choose_color(color):
    """
    Select the specified color from the color filter options.
    """
    try:
        click_on_element_by_locator(By.XPATH, "//div[@data-role='title' and text()='Color']")
        logger.info("Opened color filter dropdown.")
        click_on_element_by_locator(By.XPATH, f"//div[@class='swatch-option color ' and @option-label='{color}']")
        logger.info(f"Selected color: {color}")
    except Exception as e:
        logger.error(f"Failed to select color '{color}': {str(e)}")
