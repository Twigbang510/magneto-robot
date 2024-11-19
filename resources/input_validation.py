from robocorp.tasks import task
import logging
from helper import *

logger = logging.getLogger(__name__)

@task
def check_valid_size_input(input, valid_input):
    size_list = [size.strip().upper() for size in input.split(',')]    
    valid_size = set([size for size in size_list if size.upper() in valid_input])
    logger.info("Valid input is: %s", valid_size)
    
    invalid_size = set([size for size in size_list if size.upper() not in valid_input])
    if invalid_size: 
        logger.warning("Invalid input(s): %s", ', '.join(invalid_size))
    
    return list(valid_size)

def check_valid_color_input(input, valid_color):
    color_list = [color.strip().upper() for color in input.split(',')]
    valid_color = set([color.capitalize() for color in color_list if color in valid_color])
    logger.info("Valid input is: %s", valid_color)
    
    invalid_color = set([color.capitalize() for color in color_list if color not in valid_color])
    if invalid_color:
        logger.warning("Invalid input(s): %s", ', '.join(invalid_color))
    
    return list(valid_color)