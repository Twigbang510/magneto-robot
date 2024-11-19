from robocorp.tasks import task
from helper import *
from driver_manager import get_driver
from selenium.webdriver.common.by import By

@task
def process_cart(quantity):
    """"
    Process a quantity and check quantity against.
    """
    driver = get_driver()
    go_to_cart()
    while True:
        wait_until_element_is_visible(By.CSS_SELECTOR, '.cart.item')
        product_list_element = driver.find_elements(By.CSS_SELECTOR, '.cart.item')
        for product in product_list_element:
            check_quantity(product, quantity)
        click_on_element_by_locator(By.CSS_SELECTOR, '.action.update')

        if not navigate_to_next_page(driver):
            break        
def go_to_cart():
    click_on_element_by_locator(By.CLASS_NAME, 'showcart')
    click_on_element_by_locator(By.CLASS_NAME, 'viewcart')

def check_quantity(product, quantity):
    product_quantity_element = product.find_element(By.CSS_SELECTOR, '.input-text.qty')
    product_quantity = product_quantity_element.get_attribute('value')
    if int(product_quantity) != int(quantity):
        product_quantity_element.clear()
        product_quantity_element.send_keys(str(quantity))
        logger.info(f"Updated product quantity to {quantity} for product: {product.text}")

def navigate_to_next_page(driver):
    """
    Navigate to the next page if available.
    """
    try:
        next_button = wait_until_element_is_visible(By.CSS_SELECTOR, '.action.next')
        next_button.click()
        logger.info("Navigated to the next page.")
        return True
    except Exception as e:
        logger.warning("No more pages to navigate. ")
        return False

    