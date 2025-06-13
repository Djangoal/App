import logging
from logging.handlers import RotatingFileHandler
import os

if not os.path.exists('logs'):
    os.makedirs('logs')

logger = logging.getLogger('budget_app')
logger.setLevel(logging.DEBUG)

file_handler = RotatingFileHandler('logs/app.log', maxBytes=1000000, backupCount=3, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)