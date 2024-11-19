from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from driver_manager import get_driver
import logging
logging.basicConfig(
    filename="python.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
def get_target(driver, target=None):
    return target if target is not None else driver

    
def wait_until_element_is_visible(selector, element_locator, timeout=10, target = None):
    """Wait until element is visible until timeout occurs and returns the element"""
    driver = get_driver()   
    try:
        target = get_target(driver, target)
        element = WebDriverWait(target, timeout).until(
            EC.presence_of_element_located((selector, element_locator))
        )
        logger.info(f"Element with locator ({selector}, {element_locator}) is now visible.")
        return element
    except Exception as e:
        logger.error(f"Error waiting for element with locator ({selector}, {element_locator}): {str(e)}")
        return None

def click_on_element_by_locator(selector, element_locator, target=None):
    """Find and click an element by selector and element locator."""
    driver = get_driver()
    try:
        target = get_target(driver, target)
        element = wait_until_element_is_visible(selector, element_locator, target=target)
        if element:
            element.click()
            logger.info(f"Clicked on element with locator ({selector}, {element_locator}).")
        else:
            logger.warning(f"Element with locator ({selector}, {element_locator}) is not visible for clicking.")
    except Exception as e:
        logger.error(f"Error clicking on element with locator ({selector}, {element_locator}): {str(e)}")

def click_on_existing_element(element, target=None, timeout=10):
    """Wait until the provided element is clickable and then click it."""
    driver = get_driver()
    try:
        target = get_target(driver, target)
        WebDriverWait(target, timeout).until(EC.element_to_be_clickable(element))
        element.click()
        logger.info(f"Clicked on provided element: {element}")
    except Exception as e:
        logger.error(f"Error clicking on existing element: {element} - {str(e)}")

def click_on_position_of_element(selector, element_locator, position, target=None):
    """Finds and clicks a position of the given element"""
    driver = get_driver()
    try:
        target = get_target(driver, target)
        wait_until_element_is_visible(selector, element_locator, target=target)
        elements = target.find_elements(selector, element_locator)
        if 0 <= position < len(elements):
            elements[position].click()
            logger.info(f"Clicked on element at position {position} ({selector}, {element_locator}).")
        else:
            logger.warning(f"Position {position} is out of range for elements ({selector}, {element_locator}).")
    except Exception as e:
        logger.error(f"clicking position of element ({selector}, {element_locator})", e)

def click_btn_when_clickable(selector, element_locator, target =None):
    """Finds and clicks a button when it becomes clickable"""
    driver = get_driver()
    try:
        target = get_target(driver, target)
        element = wait_until_element_is_visible(selector, element_locator, target=target)
        WebDriverWait(target, 10).until(EC.element_to_be_clickable(element))
        element.click()
        logger.info(f"Clicked on button : {element_locator}")
    except Exception as e:
        logger.error(f"Error clicking button : {element_locator} - {str(e)}")
        
def hover_element(element):
    """Hover the element with the given selector"""
    driver = get_driver()
    try:
        ActionChains(driver).move_to_element(element).perform()
        logger.info(f"Hovered over element : {element}")
    except Exception as e:
        logger.error(f"Error hovering over element : {element} - {str(e)}")