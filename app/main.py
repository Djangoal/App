from kivy.core.window import Window
from kivy.config import Config
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import BooleanProperty
from kivy.clock import Clock
import sys
import os
import json
import platform

# Android
try:
    from android.storage import app_storage_path
    from jnius import autoclass
    from android import activity
except ImportError:
    app_storage_path = lambda: os.getcwd()
    autoclass = None
    activity = None

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
Config.set('graphics', 'multisamples', '0')
Config.set('graphics', 'fullscreen', '0')
Config.set('kivy', 'exit_on_escape', '0')


# ---------------- Gestion des exceptions ----------------
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Exception non gérée", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


# ---------------- SplashScreen ----------------
class SplashScreen(Screen):
    pass


# ---------------- APPLICATION ----------------
class MonApp(App):
    activer_pin = BooleanProperty(False)
    show_total_revenus = BooleanProperty(True)
    show_total_charges = BooleanProperty(True)
    show_total_depenses = BooleanProperty(True)
    show_restant_a_payer = BooleanProperty(True)

    def build(self):
        # Dossier interne sécurisé
        self.app_dir = app_storage_path()
        self.config_path = os.path.join(self.app_dir, "config.json")

        # Charger la config
        self.config_data = self.charger_config()

        self.activer_pin = self.config_data.get("activer_pin", True)
        self.show_total_revenus = self.config_data.get("show_total_revenus", True)
        self.show_total_charges = self.config_data.get("show_total_charges", True)
        self.show_total_depenses = self.config_data.get("show_total_depenses", True)
        self.show_restant_a_payer = self.config_data.get("show_restant_a_payer", True)

        logger.info(f"Dossier de stockage interne : {self.app_dir}")

        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash'))

        if self.activer_pin:
            sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(pageprincipalScreen(name="principal"))
        sm.add_widget(ChargesFixesScreen(name="charges_fixe"))
        sm.add_widget(RevenusScreen(name="revenus"))
        sm.add_widget(DepenseScreen(name="depense"))
        sm.add_widget(ConfigurationScreen(name="config"))
        sm.add_widget(LogsScreen(name="logs"))
        sm.add_widget(EpargneScreen(name="epargne"))

        sm.current = 'splash'
        Clock.schedule_once(lambda dt: self.show_main_screen(sm), 0.1)

        # ✅ Ouvrir la page système de permission sur Android 11+
        if platform.system() == "Android":
            self.demander_permission_stockage()

        return sm

    # ---------------- Méthodes internes ----------------
    def show_main_screen(self, sm):
        if self.activer_pin and 'login' in sm.screen_names:
            sm.current = 'login'
        else:
            sm.current = 'principal'

        Window.canvas.ask_update()
        for screen in sm.screens:
            screen.canvas.ask_update()

    # ---------------- CONFIGURATION ----------------
    def charger_config(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
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
            with open(self.config_path, "w") as f:
                json.dump(self.config_data, f)
            logger.info(f"Configuration sauvegardée dans : {self.config_path}")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de la configuration : {e}")

    # ---------------- SAUVEGARDE DANS DOCUMENTS ----------------
    def demander_permission_stockage(self):
        """Ouvre la page Android permettant d'autoriser l'accès à tous les fichiers."""
        if platform.system() != "Android" or autoclass is None:
            logger.info("Permission stockage non nécessaire (non Android).")
            return

        try:
            Intent = autoclass('android.content.Intent')
            Settings = autoclass('android.provider.Settings')
            Uri = autoclass('android.net.Uri')

            intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION)
            uri = Uri.fromParts("package", activity.getPackageName(), None)
            intent.setData(uri)
            activity.startActivity(intent)
            logger.info("Page de permission Android ouverte avec succès.")
        except Exception as e:
            logger.error(f"Erreur lors de la demande de permission stockage : {e}")

    def sauvegarder_donnees_dans_documents(self, data):
        """Enregistre un fichier JSON dans le dossier Documents du téléphone."""
        try:
            documents_path = "/storage/emulated/0/Documents"
            if not os.path.exists(documents_path):
                os.makedirs(documents_path, exist_ok=True)

            fichier_path = os.path.join(documents_path, "donnees_budget.json")

            with open(fichier_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            logger.info(f"✅ Données enregistrées dans : {fichier_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Erreur lors de la sauvegarde dans Documents : {e}")
            return False

    def exporter_donnees(self):
        """Exemple d'export manuel vers le dossier Documents."""
        donnees = {
            "revenus": [{"nom": "Salaire", "montant": 2500}],
            "depenses": [{"nom": "Loyer", "montant": 800}]
        }

        if not self.sauvegarder_donnees_dans_documents(donnees):
            logger.warning("Échec de l'enregistrement. Vérifie la permission Android.")
        else:
            logger.info("Export des données réussi !")


if __name__ == "__main__":
    MonApp().run()
