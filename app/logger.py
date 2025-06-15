import logging
import os
from datetime import datetime

# Tentative d'import pour stockage Android
try:
    from android.storage import app_storage_path
    storage_path = app_storage_path()
except ImportError:
    # Fallback générique pour tests hors Android (ex: PC ou Pydroid)
    storage_path = os.path.expanduser("~/Documents/MonAppLogs")

# Crée le dossier de logs s’il n'existe pas
os.makedirs(storage_path, exist_ok=True)

# Nom du fichier log basé sur la date
log_filename = f"log_{datetime.now().strftime('%Y-%m-%d')}.txt"
log_path = os.path.join(storage_path, log_filename)

# Configuration du logger
logger = logging.getLogger("MonAppLogger")
logger.setLevel(logging.DEBUG)

# Supprimer les anciens handlers si redémarrage
if logger.hasHandlers():
    logger.handlers.clear()

# Handler fichier
file_handler = logging.FileHandler(log_path, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Handler console (optionnel)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logger.info("Journalisation démarrée")