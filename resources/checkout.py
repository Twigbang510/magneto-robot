from robocorp.tasks import task
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from helper import *
from driver_manager import get_driver

logger = logging.getLogger(__name__)

@task
def process_checkout(shipping_address):
    """
    Task to complete the checkout process and retrieve the order number.
    """
    try:
        driver = get_driver()
        go_to_checkout(driver)

        if not wait_until_element_is_visible(By.CLASS_NAME, 'shipping-address-item'):
            fill_address_form(driver, shipping_address)
            
        # Select first available shipping option
        select_shipping_option(driver)
        
        # Proceed to the next step
        click_on_element_by_locator(By.CSS_SELECTOR, 'button.action.continue.primary')
        logger.info("Clicked continue on the shipping page.")

        # Place the order
        place_order(driver)

        # Retrieve and return order number
        order_number = get_order_number(driver)
        logger.info(f"Order placed successfully. Order number: {order_number}")
        return order_number

    except IndexError:
        logger.error("Shipping option not found.")
    except AttributeError:
        logger.error("Order number element or other required elements not found.")
    except Exception as e:
        logger.error(f"Checkout process failed: {str(e)}")
    return None


def fill_address_form(driver, shipping_address):
    """
    Fill the shipping address form.
    """
    try:
        input_data = [
            ('input[name=firstname]', shipping_address['first_name']),
            ('input[name=lastname]', shipping_address['last_name']),
            ('input[name=company]', shipping_address['company']),
            ('input[name="street[0]"]', shipping_address['address_line1']),
            ('input[name=city]', shipping_address['city']),
            ('input[name=postcode]', shipping_address['zip_code']),
            ('input[name=telephone]', shipping_address['phone_number']),
        ]
        for selector, value in input_data:
            fill_input_form(By.CSS_SELECTOR, selector, value)
        
        select_options(driver, By.CSS_SELECTOR, 'select[name=region_id]', shipping_address['state'])
        select_options(driver, By.CSS_SELECTOR, 'select[name=country_id]', shipping_address['country'])
        check_error_message()
    except Exception as e:
        logger.error(f"Error filling the address form: {str(e)}")


def select_shipping_option(driver):
    """
    Select the first shipping option available.
    """
    try:
        shipping_options = driver.find_elements(By.CSS_SELECTOR, "tbody .row input[type='radio']")
        if shipping_options:
            shipping_options[0].click()
            logger.info("Selected the first shipping option.")
        else:
            raise IndexError("No shipping options found.")
    except Exception as e:
        logger.error(f"Error selecting shipping option: {str(e)}")


def place_order(driver):
    """
    Place the order by clicking the final checkout button.
    """
    try:
        order_btn = wait_until_element_is_visible(By.CSS_SELECTOR, 'button.action.primary.checkout')
        driver.execute_script("arguments[0].click()", order_btn)
        logger.info("Clicked on the place order button.")
    except Exception as e:
        logger.error(f"Error placing order: {str(e)}")


def get_order_number(driver):
    """
    Retrieve the order number after placing the order.
    """
    try:
        order_num_element = wait_until_element_is_visible(By.CLASS_NAME, 'order-number')
        return order_num_element.get_attribute("innerText")
    except Exception as e:
        logger.error(f"Error retrieving order number: {str(e)}")
        return None


def select_options(driver, locator, selector, option_text):
    """
    Select an option from a dropdown.
    """
    try:
        select_element = Select(driver.find_element(locator, selector))
        select_element.select_by_visible_text(option_text)
        logger.info(f"Selected option: {option_text}")
    except Exception as e:
        logger.error(f"Error selecting option '{option_text}': {str(e)}")


def fill_input_form(locator, selector, value):
    """
    Fill an input form with the specified value.
    """
    try:
        input_element = wait_until_element_is_visible(locator, selector)
        input_element.clear()
        input_element.send_keys(value)
        logger.info(f"Filled input: {value}")
    except Exception as e:
        logger.error(f"Error filling input '{value}': {str(e)}")


def check_error_message():
    """
    Check for error messages on the page.
    """
    try:
        error_element = wait_until_element_is_visible(By.CSS_SELECTOR, '.message.warning')
        if error_element:
            error_message = error_element.get_attribute("innerText")
            logger.error(f"Error message displayed: {error_message}")
            raise Exception(error_message)
    except Exception as e:
        logger.info("No error message found.")


def go_to_checkout(driver):
    """
    Navigate to the checkout page.
    """
    try:
        wait_until_element_is_visible(By.CSS_SELECTOR, 'button.action.primary')
        checkout_buttons = driver.find_elements(By.CSS_SELECTOR, 'button.action.primary.checkout')
        if len(checkout_buttons) > 1:
            checkout_buttons[1].click()
            logger.info("Navigated to the checkout page.")
        else:
            raise IndexError("Insufficient checkout buttons found.")
    except Exception as e:
        logger.error(f"Error navigating to checkout: {str(e)}")
