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

def go_to_cart():
    click_on_element_by_locator(By.CLASS_NAME, 'showcart')
    click_on_element_by_locator(By.CLASS_NAME, 'viewcart')

    
    