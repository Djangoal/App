# utils/logger.py
import logging
from datetime import datetime
import os

def get_log_dir():
    try:
        from android.storage import primary_external_storage_path
        return os.path.join(primary_external_storage_path(), "my_budget_app_logs")
    except Exception:
        # fallback (utile pour Pydroid ou PC)
        return "logs"

log_dir = get_log_dir()
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_filename = datetime.now().strftime("log_%Y-%m-%d.txt")
log_path = os.path.join(log_dir, log_filename)

logging.basicConfig(
    filename=log_path,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_error(error_message):
    try:
        logging.error(error_message)
    except Exception as e:
        print(f"Erreur de log : {e}")
