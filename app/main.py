from kivy.core.window import Window
from kivy.config import Config
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import BooleanProperty
from kivy.clock import Clock
import sys
from android.permissions import request_permissions, Permission
from logger import logger

# Import du gestionnaire de configuration
from models.app_config import AppConfig

# Import des écrans
from views.login_screen import LoginScreen
from views.logs_screen import LogsScreen
from views.page_principal_screen import pageprincipalScreen
from views.revenus_screen import RevenusScreen
from views.charges_fixes_screen import ChargesFixesScreen
from views.depenses_screen import DepenseScreen
from views.configuration_screen import ConfigurationScreen
from views.epargne_screen import EpargneScreen

from plyer import notification
from jnius import autoclass

# Initialisation AdMob via Plyer wrapper
PythonActivity = autoclass('org.kivy.android.PythonActivity')
# Si le wrapper expose une fonction init
# AdMob.init(PythonActivity.mActivity)
# Window.softinput_mode = 'below_target'  # à activer après le lancement si nécessaire

# ---------------- Gestion des exceptions ----------------
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Exception non gérée", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception

# ---------------- SplashScreen ----------------
class SplashScreen(Screen):
    pass  # écran blanc vide pour éviter l'écran noir

# ---------------- APPLICATION ----------------
class MonApp(App):
    # Propriétés dynamiques liées à la configuration
    activer_pin = BooleanProperty(True)
    show_total_revenus = BooleanProperty(True)
    show_total_charges = BooleanProperty(True)
    show_total_depenses = BooleanProperty(True)
    show_restant_a_payer = BooleanProperty(True)

    def build(self):
        # Chargement de la configuration
        self.config_manager = AppConfig()
        cfg = self.config_manager.data

        # Affectation des valeurs depuis la configuration
        self.activer_pin = cfg.get("activer_pin", False)
        self.show_total_revenus = cfg.get("show_total_revenus", True)
        self.show_total_charges = cfg.get("show_total_charges", True)
        self.show_total_depenses = cfg.get("show_total_depenses", True)
        self.show_restant_a_payer = cfg.get("show_restant_a_payer", True)

        # Demander les permissions Android
        try:
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])
        except Exception as e:
            logger.warning(f"Les permissions Android n'ont pas pu être demandées : {e}")

        # Gestionnaire d'écrans
        sm = ScreenManager()

        # Ajout du SplashScreen blanc
        sm.add_widget(SplashScreen(name='splash'))

        # Ajout des écrans de l’application
        if self.activer_pin:
            sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(pageprincipalScreen(name="principal"))
        sm.add_widget(ChargesFixesScreen(name="charges_fixe"))
        sm.add_widget(RevenusScreen(name="revenus"))
        sm.add_widget(DepenseScreen(name="depense"))
        sm.add_widget(ConfigurationScreen(name="config"))
        sm.add_widget(LogsScreen(name="logs"))
        sm.add_widget(EpargneScreen(name="epargne"))

        # Écran de départ temporaire
        sm.current = 'splash'

        # Rafraîchissement et passage au bon écran
        Clock.schedule_once(lambda dt: self.show_main_screen(sm), 0.1)

        return sm

    # ---------------- Méthodes internes ----------------
    def show_main_screen(self, sm):
        """Remplace le SplashScreen par l'écran Login ou Principal"""
        if self.activer_pin and 'login' in sm.screen_names:
            sm.current = 'login'
        else:
            sm.current = 'principal'
        # Forcer redraw complet pour éviter écran noir
        Window.canvas.ask_update()
        for screen in sm.screens:
            screen.canvas.ask_update()

    def sauvegarder_config(self):
        """Met à jour la configuration et la sauvegarde via AppConfig"""
        self.config_manager["activer_pin"] = self.activer_pin
        self.config_manager["show_total_revenus"] = self.show_total_revenus
        self.config_manager["show_total_charges"] = self.show_total_charges
        self.config_manager["show_total_depenses"] = self.show_total_depenses
        self.config_manager["show_restant_a_payer"] = self.show_restant_a_payer


if __name__ == "__main__":
    MonApp().run()
