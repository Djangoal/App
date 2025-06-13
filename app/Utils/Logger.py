# utils/logger.py
import logging
from datetime import datetime
import os

# Crée le dossier de logs s'il n'existe pas
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Fichier de log avec date
log_filename = datetime.now().strftime("log_%Y-%m-%d.txt")
log_path = os.path.join(log_dir, log_filename)

# Configuration du logger
logging.basicConfig(
    filename=log_path,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_error(error_message):
    logging.error(error_message)

# Alias compatible
def log_crash_info(message):
    log_error(message)
