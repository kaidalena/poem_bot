import logging
from os import path
from logging.handlers import TimedRotatingFileHandler

LOG_LEVEL = logging.DEBUG
FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FOLDER = "logs"


def get_logger(logger_name):
    log_file = path.join(LOG_FOLDER, f"{logger_name}.log")
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    file_handler = TimedRotatingFileHandler(log_file, encoding="UTF-8", when='H', interval=1)
    file_handler.setFormatter(FORMATTER)
    file_handler.suffix = "%Y-%m-%d_%H%M%S"
    logger.addHandler(file_handler)
    return logger
