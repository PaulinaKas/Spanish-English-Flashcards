import logging

def setup_logger(log_to_console=False):
    logger = logging.getLogger('SimpleLogger')
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler('logs.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

logger = setup_logger(log_to_console=False) # info / warning / error levels, for example logger.warning()