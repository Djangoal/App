from kivy.core.window import Window
from kivy.config import Config
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import BooleanProperty
from kivy.clock import Clock
import sys
import os
import json
from android.permissions import request_permissions, Permission
from logger import logger

# Import des écrans
from views.login_screen import LoginScreen
from views.logs_screen import LogsScreen 
from views.page_principal_screen import pageprincipalScreen
from views.revenus_screen import RevenusScreen
from views.charges_fixes_screen import ChargesFixesScreen
from views.depenses_screen import DepenseScreen
from views.configuration_screen import ConfigurationScreen
from views.epargne_screen import EpargneScreen

# ---------------- CONFIG SDL2 ----------------
Config.set('graphics', 'multisamples', '0')  # désactive anti-aliasing
Config.set('graphics', 'fullscreen', '0')
Config.set('kivy', 'exit_on_escape', '0')
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
    activer_pin = BooleanProperty(True)
    show_total_revenus = BooleanProperty(True)
    show_total_charges = BooleanProperty(True)
    show_total_depenses = BooleanProperty(True)
    show_restant_a_payer = BooleanProperty(True)

    def build(self):
        self.config_data = self.charger_config()

        self.activer_pin = self.config_data.get("activer_pin", True)
        self.show_total_revenus = self.config_data.get("show_total_revenus", True)
        self.show_total_charges = self.config_data.get("show_total_charges", True)
        self.show_total_depenses = self.config_data.get("show_total_depenses", True)
        self.show_restant_a_payer = self.config_data.get("show_restant_a_payer", True)

        # Demander les permissions Android
        try:
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])
        except Exception as e:
            logger.warning(f"Les permissions Android n'ont pas pu être demandées : {e}")

        sm = ScreenManager()

        # Ajout du SplashScreen blanc
        sm.add_widget(SplashScreen(name='splash'))

        # Ajout des autres écrans
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

        # ---------------- Rafraîchissement et passage au vrai écran ----------------
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
        from kivy.core.window import Window
        Window.canvas.ask_update()
        for screen in sm.screens:
            screen.canvas.ask_update()

    def charger_config(self):
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Erreur lors du chargement de la configuration : {e}")
        return {}

    def sauvegarder_config(self):
        self.config_data["activer_pin"] = self.activer_pin
        self.config_data["show_total_revenus"] = self.show_total_revenus
        self.config_data["show_total_charges"] = self.show_total_charges
        self.config_data["show_total_depenses"] = self.show_total_depenses
        self.config_data["show_restant_a_payer"] = self.show_restant_a_payer

        try:
            with open("config.json", "w") as f:
                json.dump(self.config_data, f)
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de la configuration : {e}")


if __name__ == "__main__":
    MonApp().run()
