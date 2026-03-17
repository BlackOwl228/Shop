import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler("app.log", maxBytes=1024 * 1024, backupCount=3)
file_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(file_formatter)
logger.addHandler(console_handler)
