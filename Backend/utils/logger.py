import logging
import os
from logging.handlers import RotatingFileHandler


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


log_file = os.path.join(LOG_DIR, "app.log")

# Buat logger utama
logger = logging.getLogger("ChatbotLogger")
logger.setLevel(logging.INFO)

# Rotating File Handler berbasis SIZE 
handler = RotatingFileHandler(
    log_file,
    maxBytes=2 * 1024 * 1024,  
    backupCount=5,            # simpan 5 file cadangan
    encoding="utf-8"
)


formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)
handler.setFormatter(formatter)


logger.addHandler(handler)


logger.propagate = False


def log_info(message):
    print(message)
    logger.info(message)

def log_warning(message):
    print("[WARNING]", message)
    logger.warning(message)

def log_error(message):
    print("[ERROR]", message)
    logger.error(message)