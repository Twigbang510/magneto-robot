from robocorp.tasks import task
import logging
from selenium.webdriver.common.by import By
from helper import *
from driver_manager import get_driver

logger = logging.getLogger(__name__)

@task
def process_checkout():
    """
    Task to complete the checkout process and retrieve the order number.
    """
    try:
        driver = get_driver()
        go_to_checkout(driver)

        # Select shipping option
        shipping_options = driver.find_elements(By.CSS_SELECTOR, "tbody .row input[type='radio']")
        shipping_options[0].click()
        logger.info("Selected first shipping option.")
        
        # Proceed to the next step in checkout
        click_on_element_by_locator(By.CSS_SELECTOR, 'button.action.continue.primary')
        logger.info("Clicked continue on shipping page.")

        # Place the order
        order_btn_element = wait_until_element_is_visible(By.CSS_SELECTOR, 'button.action.primary.checkout')
        driver.execute_script("arguments[0].click()", order_btn_element)
        logger.info("Order button clicked.")

        # Retrieve order number
        order_num_element = wait_until_element_is_visible(By.CLASS_NAME, 'order-number')
        order_number = order_num_element.get_attribute("innerText")
        logger.info(f"Order placed successfully. Order number: {order_number}")
        return order_number

    except IndexError:
        logger.error("Shipping option not found.")
    except AttributeError:
        logger.error("Order number element or other required elements not found.")
    except Exception as e:
        logger.error(f"Checkout process failed: {str(e)}")
    return None

def go_to_checkout(driver):
    """
    Navigate to the checkout page.
    """
    try:
        wait_until_element_is_visible(By.CSS_SELECTOR, 'button.action.primary')
        checkout_btn_elements = driver.find_elements(By.CSS_SELECTOR, 'button.action.primary.checkout')
        checkout_btn_elements[1].click()
        logger.info("Navigated to the checkout page.")
    except IndexError:
        logger.error("Checkout button not found or insufficient elements.")
    except Exception as e:
        logger.error(f"Failed to navigate to checkout page: {str(e)}")
