import logging, os, re
from pythonjsonlogger import jsonlogger
import sys

class SensitiveMaskingFilter(logging.Filter):
    def filter(self, record):
        for attr in dir(record):
            if attr[0:2] != '__' and isinstance(getattr(record, attr), str):
                setattr(record, attr, self.sanitize(getattr(record, attr)))

        return True

    def sanitize(self, value):
        value = re.sub(r"'(.*?(PASSWORD|KEY|SECRET|AUTH|TOKEN|CREDENTIAL).*?)': '([^']+)'", r"'\1': '***'", value, flags=re.IGNORECASE)

        return value

def configure_logger(level, hide_sensitives=True):

    logging.basicConfig(level=level.upper())

    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter('%(levelname)%(message)')
    logHandler.setFormatter(formatter)
    logging.getLogger().handlers = []
    logging.getLogger().addHandler(logHandler)

    if hide_sensitives:
        logging.getLogger().addFilter(SensitiveMaskingFilter())


    def handle_exception(exc_type, exc_value, exc_traceback):
        # if issubclass(exc_type, KeyboardInterrupt):
        #     sys.__excepthook__(exc_type, exc_value, exc_traceback)
        #     return

        logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception


    return logging

