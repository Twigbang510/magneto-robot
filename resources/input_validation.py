from robocorp.tasks import task
import logging
from helper import *

logger = logging.getLogger(__name__)

@task
def check_valid_input(input, valid_input):
    size_list = [size.strip().upper() for size in input.split(',')]    
    valid_size = set([size for size in size_list if size in valid_input])
    logger.info("Valid input is: %s", valid_size)
    
    invalid_size = set([size for size in size_list if size not in valid_input])
    if invalid_size: 
        logger.warning("Invalid input(s): %s", ', '.join(invalid_size))
    
    return valid_size
