# driver_manager.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

driver = None

def initialize_driver():
    """Initialize the global Chrome driver with specified options."""
    global driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    return driver

def get_driver():
    """Return the current driver if initialized; raise error if not."""
    global driver
    if driver is None:
        raise ValueError("Driver not initialized. Call initialize_driver first.")
    return driver

def quit_driver():
    """Close and clean up the driver."""
    global driver
    if driver:
        driver.quit()
        driver = None