import logging
import os
from logging.handlers import RotatingFileHandler

# === Pastikan folder logs ada ===
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# === Path file log ===
log_file = os.path.join(LOG_DIR, "app.log")

# === Buat logger utama ===
logger = logging.getLogger("ChatbotLogger")
logger.setLevel(logging.INFO)

# === Rotating File Handler berbasis SIZE ===
handler = RotatingFileHandler(
    log_file,
    maxBytes=2 * 1024 * 1024,  # 2MB → rotate otomatis kalau penuh
    backupCount=5,            # simpan 5 file cadangan
    encoding="utf-8"
)

# === Format isi log ===
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)
handler.setFormatter(formatter)

# === Tambahin handler ke logger ===
logger.addHandler(handler)

# === Biar nggak log dobel di console ===
logger.propagate = False

# === Wrapper gampang dipanggil ===
def log_info(message):
    print(message)
    logger.info(message)

def log_warning(message):
    print("[WARNING]", message)
    logger.warning(message)

def log_error(message):
    print("[ERROR]", message)
    logger.error(message)