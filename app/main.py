import os
import json
import sys
import traceback

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.utils import platform
from kivy.logger import Logger as logger

# --- GESTION DES ERREURS ---
def redirect_errors():
    def handle_exception(exc_type, exc_value, exc_traceback):
        try:
            with open("/sdcard/kivy_error_log.txt", "w") as f:
                traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
        except Exception as e:
            logger.error(f"Erreur lors de l'écriture du log: {e}")
    sys.excepthook = handle_exception

redirect_errors()

# --- PERMISSIONS (ANDROID) ---
if platform == "android":
    from android.permissions import request_permissions, Permission, check_permission
    from android.storage import app_storage_path

    def demander_permissions():
        def callback(permissions, results):
            for p, r in zip(permissions, results):
                logger.info(f"Permission {p}: {'OK' if r else 'REFUSÉ'}")

        request_permissions(
            [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE],
            callback,
        )

    demander_permissions()
    chemin_base = app_storage_path()
else:
    chemin_base = os.getcwd()

chemin_config = os.path.join(chemin_base, "config.json")

# --- CHARGEMENT CONFIG ---
def charger_config():
    try:
        if os.path.exists(chemin_config):
            with open(chemin_config, "r") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Erreur lors du chargement config: {e}")
    return {}

# --- SAUVEGARDE CONFIG ---
def sauvegarder_config(config):
    try:
        with open(chemin_config, "w") as f:
            json.dump(config, f)
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde config: {e}")

# --- APPLICATION PRINCIPALE ---
class MonBudgetApp(App):
    def build(self):
        config = charger_config()
        total_revenus = config.get("revenus", 0)
        total_depenses = config.get("depenses", 0)

        solde = total_revenus - total_depenses

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text=f"Revenus : {total_revenus}"))
        layout.add_widget(Label(text=f"Dépenses : {total_depenses}"))
        layout.add_widget(Label(text=f"Solde : {solde}"))

        return layout

if __name__ == "__main__":
    MonBudgetApp().run()
