import logging
import os
from datetime import datetime

# Détection du chemin de stockage en toute sécurité
def get_storage_path():
    try:
        from android.storage import app_storage_path
        return app_storage_path()
    except Exception:
        # Fallback: PC ou Pydroid
        return os.path.expanduser("~/Documents/MonAppLogs")

# Répertoire des logs
storage_path = get_storage_path()
os.makedirs(storage_path, exist_ok=True)

# Nom du fichier log (par date)
log_filename = f"log_{datetime.now().strftime('%Y-%m-%d')}.txt"
log_path = os.path.join(storage_path, log_filename)

# Configuration du logger
logger = logging.getLogger("MonAppLogger")
logger.setLevel(logging.DEBUG)

# Nettoyage des handlers précédents
if logger.hasHandlers():
    logger.handlers.clear()

# Fichier log
file_handler = logging.FileHandler(log_path, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Console (optionnel)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logger.info("Journalisation démarrée")