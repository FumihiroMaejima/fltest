from flask import Flask
import logging

def create_logger():
    logger = logging.getLogger()
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('app.log')
    c_handler.setLevel(logging.WARNING)
    f_handler.setLevel(logging.WARNING)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    return logger


logger = create_logger()
