from robocorp.tasks import task
import logging
from selenium.webdriver.common.by import By
from helper import wait_until_element_is_visible, click_on_element_by_locator
from driver_manager import get_driver

logger = logging.getLogger(__name__)

@task
def get_product_list(min_price, max_price, quantity, size, color):
    """
    Task to retrieve products within a price range and add them to the cart.
    """
    driver = get_driver()
    product_list = []

    while True:
        wait_until_element_is_visible(By.CSS_SELECTOR, '.products.list.items.product-items')
        product_elements = driver.find_elements(By.CSS_SELECTOR, '.product-item-info')

        for product in product_elements:
            product_data = check_price(product, min_price, max_price)
            if product_data:
                product_list.append(product_data)

        if not navigate_to_next_page(driver):
            break

    if not product_list:
        logger.error("No products found within the specified price range.")
        raise Exception("No products found.")

    logger.info("Selected products: %s", product_list)
    add_to_cart(driver, product_list, quantity, size, color)
    return product_list

def navigate_to_next_page(driver):
    """
    Navigate to the next page if available.
    """
    try:
        next_buttons = driver.find_elements(By.CSS_SELECTOR, '.action.next')
        if next_buttons:
            next_buttons[1].click()
            logger.info("Navigated to the next page.")
            return True
        return False
    except Exception as e:
        logger.info("No more pages to navigate. %s", str(e))
        return False

def add_to_cart(driver, product_list, quantity, size, color):
    """
    Add selected products to the cart.
    """
    for product in product_list:
        driver.get(product['url'])
        choose_product_options(driver, size, color)
        set_quantity(driver, quantity)
        click_on_element_by_locator(By.ID, 'product-addtocart-button')
        logger.info("Added to cart: %s", product)

def choose_product_options(driver, size, color):
    """
    Select size and color options for a product.
    """
    try:
        click_on_element_by_locator(By.XPATH, f"//div[@class='swatch-option text' and @option-label='{size}']")
        logger.info("Selected size: %s", size)
    except Exception as e:
        logger.warning("Size option not available: %s", str(e))

    try:
        click_on_element_by_locator(By.XPATH, f"//div[@class='swatch-option color' and @option-label='{color}']")
        logger.info("Selected color: %s", color)
    except Exception as e:
        logger.warning("Color option not available: %s", str(e))

def set_quantity(driver, quantity):
    """
    Set the product quantity.
    """
    try:
        quantity_element = driver.find_element(By.ID, "qty")
        quantity_element.clear()
        quantity_element.send_keys(str(quantity))
        logger.info("Set quantity: %s", quantity)
    except Exception as e:
        logger.error("Failed to set quantity: %s", str(e))

def check_price(product, min_price, max_price):
    """
    Check if a product's price is within the specified range.
    """
    try:
        product_link_element = wait_until_element_is_visible(By.CLASS_NAME, 'product-item-link', target=product)
        product_url = product_link_element.get_attribute('href')
        product_name = product_link_element.text

        price_element = wait_until_element_is_visible(By.CLASS_NAME, 'price', target=product)
        product_price = float(price_element.text.replace("$", "").replace(",", ""))

        if float(min_price) <= product_price <= float(max_price):
            product_detail = {'url': product_url, 'name': product_name, 'price': product_price}
            logger.info("Product matches criteria: %s", product_detail)
            return product_detail
    except Exception as e:
        logger.error("Error checking product price or details: %s", str(e))
    return None
