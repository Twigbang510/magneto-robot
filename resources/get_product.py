from robocorp.tasks import task
import logging
from selenium.webdriver.common.by import By
from helper import *
from driver_manager import get_driver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

logger = logging.getLogger(__name__)

@task
def get_product_list(min_price, max_price, quantity, size_list, color_list):
    """
    Retrieve products within a price range and add them to the cart.
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
        raise ValueError("No products found.")

    logger.info("Selected products: %s", product_list)
    return add_to_cart(driver, product_list, quantity, size_list, color_list)

def navigate_to_next_page(driver):
    """
    Navigate to the next page if available.
    """
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, '.action.next')
        next_button.click()
        logger.info("Navigated to the next page.")
        return True
    except Exception as e:
        logger.warning("No more pages to navigate. ")
        return False

def add_to_cart(driver, product_list, quantity, size_list, color_list):
    """
    Add selected products to the cart and collect detailed product data.
    """
    full_product_list = []
    for product in product_list:
        driver.get(product['url'])
        check_ads()
        chosen_products = choose_product_options(driver, product, quantity, size_list, color_list)
        full_product_list.extend(chosen_products)

    logger.info("Products added to cart: %s", full_product_list)
    return full_product_list
def check_ads(driver):
    """
    Check for Google Ads and remove them.
    """
    if (driver.find_element(By.CSS_SELECTOR,"ins.adsbygoogle")):
        driver.execute_script("""
            var ads = document.querySelectorAll('ins.adsbygoogle');
            ads.forEach(function(ad) {
                ad.remove();
            });
        """)
        logger.info("Removed Ads")
def choose_product_options(driver, product_data, quantity, size_list, color_list):
    """
    Choose product size and color options and add them to the cart.
    """
    available_sizes = get_available_options(driver, "//div[@class='swatch-option text']")
    available_colors = get_available_options(driver, "//div[@class='swatch-option color']")

    logger.info("Available sizes: %s", available_sizes)
    logger.info("Available colors: %s", available_colors)

    result = []
    for size in size_list:
        if not is_option_available(size, available_sizes):
            result.append(create_cart_status(product_data, size, None, 'Size not available'))
            continue

        click_option(size, "swatch-option text")
        for color in color_list:
            if not is_option_available(color, available_colors):
                result.append(create_cart_status(product_data, size, color, 'Color not available'))
                continue
            color_xpath = f"//div[contains(@class, 'swatch-option color') and @option-label='{color}']"
            color_element = wait_until_element_is_visible(By.XPATH, color_xpath)
            if not color_element.get_attribute('aria-checked') == 'true':
                click_option(color, "swatch-option color")
            set_quantity(driver, quantity)
            wait_for_cart_btn(driver)
            if check_qty_error(driver):
                logger.error("Failed to add product to cart: %s, Size: %s, Color: %s", product_data['name'], size, color)
                result.append(create_cart_status(product_data, size, color, 'Failed to add to cart'))
                continue
            logger.info("Added product to cart: %s, Size: %s, Color: %s", product_data['name'], size, color)
            result.append(create_cart_status(product_data, size, color, 'Added to cart'))

    return result
def check_qty_error(driver):
    """
    Check quantity error
    """
    try:
        qty_error_element = driver.find_element(By.ID, 'qty-error')
        return qty_error_element.is_displayed()
    except NoSuchElementException:
        return False
def wait_for_cart_btn(driver): 
    """
    Wait for the cart button to be clickable.
    """
    cart_btn_element = wait_until_element_is_visible(By.ID, "product-addtocart-button")
    WebDriverWait(driver, 10).until(lambda d: 'Add to Cart' in cart_btn_element.text)
    cart_btn_element.click()
    logger.info("Clicked on cart button.")
    
def get_available_options(driver, xpath):
    """
    Retrieve available size or color options.
    """
    options = driver.find_elements(By.XPATH, xpath)
    return [opt.get_attribute('option-label') for opt in options]

def is_option_available(option_label, available_options):
    """
    Check if a specific size or color is available.
    """
    return option_label in available_options

def click_option(option_label, option_class):
    """
    Click on a specific size or color option.
    """
    xpath = f"//div[contains(@class, '{option_class}') and @option-label='{option_label}']"
    click_btn_when_clickable(By.XPATH, xpath)

def set_quantity(driver, quantity):
    """
    Set the product quantity.
    """
    try:
        quantity_element = driver.find_element(By.ID, "qty")
        quantity_element.clear()
        quantity_element.send_keys(str(quantity))
        logger.info("Set quantity: %s", quantity)
        return True
    except Exception as e:
        logger.error("Failed to set quantity: %s", str(e))
        return False

def check_price(product, min_price, max_price):
    """
    Check if a product's price is within the specified range.
    """
    try:
        product_link = wait_until_element_is_visible(By.CLASS_NAME, 'product-item-link', target=product)
        price_element = wait_until_element_is_visible(By.CLASS_NAME, 'price', target=product)

        product_price = float(price_element.text.replace("$", "").replace(",", ""))
        if float(min_price) <= product_price <= float(max_price):
            product_detail = {
                'url': product_link.get_attribute('href'),
                'name': product_link.text,
                'price': product_price,
            }
            logger.info("Product matches criteria: %s", product_detail)
            return product_detail
    except Exception as e:
        logger.error("Error checking product price or details: %s", str(e))
    return None

def create_cart_status(product, size, color, status):
    """
    Create a structured cart status for logging and return.
    """
    return {
        'name': product['name'],
        'url': product['url'],
        'price': product['price'],
        'size': size,
        'color': color,
        'status': status
    }
