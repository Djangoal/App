import logging
import os
from datetime import datetime

# Détermine un chemin sûr selon l'environnement
def get_log_path():
    try:
        from android.storage import app_storage_path
        app_path = app_storage_path()
    except:
        app_path = os.getcwd()  # Pour test sur PC
    log_dir = os.path.join(app_path, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_filename = f"log_{datetime.now().strftime('%Y-%m-%d')}.txt"
    return os.path.join(log_dir, log_filename)

log_path = get_log_path()

# Configuration du logger
logger = logging.getLogger("MonAppLogger")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(log_path, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Console (facultatif)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logger.info("Journalisation démarrée")
