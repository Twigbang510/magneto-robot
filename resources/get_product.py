from robocorp.tasks import task
import logging
from selenium.webdriver.common.by import By
from helper import *
from driver_manager import get_driver

logger = logging.getLogger(__name__)

@task
def get_product_list(min_price, max_price, quantity, size, color):
    """
    Task to retrieve product list within a price range and add to cart with specified options.
    """
    driver = get_driver()
    wait_until_element_is_visible(By.CSS_SELECTOR, '.products.list.items.product-items')
    product_list_elements = driver.find_elements(By.CSS_SELECTOR, '.product-item-info')
    product_list = []

    for product in product_list_elements:
        logger.info("Checking product: %s", product)
        checked_product = check_price(product,min_price,  max_price)
        if checked_product:
            product_list.append(checked_product)

    logger.info("Selected product list: %s", product_list)
    add_to_cart(driver, product_list, quantity, size, color)
    return product_list

def add_to_cart(driver, product_list, quantity, size, color):
    """
    Add selected products to the cart.
    """
    for product in product_list:
        driver.get(product['url'])
        choose_option(driver, size, color)
        set_quantity(driver, quantity)
        click_on_element_by_locator(By.ID, 'product-addtocart-button')
        logger.info("Added product to cart: %s", product)
        # Adding a short wait time between actions for stability
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, 'product-addtocart-button')))

def choose_option(driver, size, color):
    """
    Select the specified size and color options for the product.
    """
    click_on_element_by_locator(By.XPATH, f"//div[@class='swatch-option text' and @option-label='{size}']")
    logger.info("Selected size: %s", size)
    click_on_element_by_locator(By.XPATH, f"//div[@class='swatch-option color' and @option-label='{color}']")
    logger.info("Selected color: %s", color)

def set_quantity(driver, quantity):
    """
    Set the desired quantity for the product.
    """
    quantity_element = driver.find_element(By.ID, "qty")
    quantity_element.clear()
    quantity_element.send_keys(str(quantity))
    logger.info("Set quantity: %s", quantity)

def check_price(product, min_price, max_price):
    """
    Check the price of a product and return product details if it meets the price criteria.
    """
    try:
        product_detail_element = wait_until_element_is_visible(By.CLASS_NAME, 'product-item-link', target=product)
        product_url = product_detail_element.get_attribute('href')
        product_name = product_detail_element.text

        price_element = wait_until_element_is_visible(By.CLASS_NAME, 'price', target=product)
        product_price = float(price_element.text.replace("$", "").replace(",", ""))

        if float(min_price) <= product_price <= float(max_price):
            product_detail = {
                'url': product_url,
                'name': product_name,
                'price': product_price
            }
            logger.info("Selected product for cart: %s", product_detail)
            return product_detail
    except Exception as e:
        logger.error(f"Error retrieving product price or details: {str(e)}")
    return None
