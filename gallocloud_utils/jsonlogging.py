import logging, os, re
from pythonjsonlogger import jsonlogger

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

    return logging

