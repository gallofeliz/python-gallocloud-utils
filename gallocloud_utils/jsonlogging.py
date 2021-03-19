import logging, os
from pythonjsonlogger import jsonlogger

def configure_logger(level):

    logging.basicConfig(level=level)

    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter('%(levelname)%(message)')
    logHandler.setFormatter(formatter)
    logging.getLogger().handlers = []
    logging.getLogger().addHandler(logHandler)

    return logging
