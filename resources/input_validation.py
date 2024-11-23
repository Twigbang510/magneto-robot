from robocorp.tasks import task
import logging
from selenium.webdriver.common.by import By
from helper import *
from driver_manager import get_driver

logger = logging.getLogger(__name__)

@task
def check_valid_size_input(input, valid_input):
    size_list = [size.strip().upper() for size in input.split(',')]    
    valid_size = {size for size in size_list if size.upper() in valid_input}
    invalid_size = {size for size in size_list if size.upper() not in valid_input}
    if invalid_size: 
        logger.warning("Invalid input(s): %s", ', '.join(invalid_size))
    if not valid_size:
        logger.error("No valid sizes provided. Stopping the process.")
        raise ValueError("No valid sizes found.")
    logger.info("Valid input is: %s", valid_size)
    return list(valid_size)

def check_valid_color_input(input, valid_color):
    color_list = [color.strip().lower() for color in input.split(',')]
    valid_colors = {color.capitalize() for color in color_list if color.capitalize() in valid_color}
    invalid_colors = {color.capitalize() for color in color_list if color.capitalize() not in valid_color}
    if invalid_colors:
        logger.warning("Invalid input(s): %s", ', '.join(invalid_colors))
    if not valid_colors:
        logger.error("No valid colors provided. Stopping the process.")
        raise ValueError("No valid colors found.")
    logger.info("Valid input is: %s", valid_colors)
    return list(valid_colors)

def get_available_size():
    size_element = wait_until_element_is_visible(By.CSS_SELECTOR, '.swatch-attribute.swatch-layered.size')
    size_list_element = size_element.find_elements(By.CSS_SELECTOR, '.swatch-option.text ')
    available_size_list = [size.get_attribute('innerText') for size in size_list_element]
    if not get_available_color:
        logger.error("No available sizes found.")
        raise ValueError("No available sizes found.")
    logger.info("Available size is: %s", available_size_list)
    return available_size_list

def get_available_color():
    color_element = wait_until_element_is_visible(By.CSS_SELECTOR, '.swatch-attribute.swatch-layered.color')
    color_list_element = color_element.find_elements(By.CSS_SELECTOR, '.swatch-option.color ')
    available_color_list = [color.get_attribute('option-label') for color in color_list_element]
    if not available_color_list:
        logger.error("No available colors found.")
        raise ValueError("No available colors found.")
    logger.info("Available color is: %s", available_color_list)
    return available_color_list