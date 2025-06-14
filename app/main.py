import sys
import traceback
from kivy.utils import platform

if platform == "android":
    from android.storage import app_storage_path
    import os

    # Répertoire où enregistrer les logs (dans l'espace sécurisé de l'appli)
    log_path = os.path.join(app_storage_path(), "error_log.txt")

    def exception_hook(exctype, value, tb):
        with open(log_path, "w") as f:
            traceback.print_exception(exctype, value, tb, file=f)

    sys.excepthook = exception_hook
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import BooleanProperty
from views.logs_screen import LogsScreen  # Chemin selon ton arborescence

from views.page_principal_screen import pageprincipalScreen
from views.revenus_screen import RevenusScreen
from views.charges_fixes_screen import ChargesFixesScreen
from views.depenses_screen import DepenseScreen
from views.configuration_screen import ConfigurationScreen
import sys
from logger import logger

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Exception non gérée", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception


    

class MonApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(pageprincipalScreen(name="principal"))
        sm.add_widget(ChargesFixesScreen(name="charges_fixe"))
        sm.add_widget(RevenusScreen(name="revenus"))
        sm.add_widget(DepenseScreen(name="depense"))
        sm.add_widget(ConfigurationScreen(name="config"))
        sm.add_widget(LogsScreen(name="logs"))
        return sm
        
        # Propriétés pour afficher/masquer les totaux
    show_total_revenus = BooleanProperty(True)
    show_total_charges = BooleanProperty(True)
    show_total_depenses = BooleanProperty(True)

if __name__ == "__main__":
    MonApp().run()