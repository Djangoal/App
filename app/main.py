from kivy.core.window import Window
Window.softinput_mode = 'below_target'

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.utils import platform

from views.logs_screen import LogsScreen
from views.page_principal_screen import pageprincipalScreen
from views.revenus_screen import RevenusScreen
from views.charges_fixes_screen import ChargesFixesScreen
from views.depenses_screen import DepenseScreen
from views.configuration_screen import ConfigurationScreen
from views.epargne_screen import EpargneScreen

from android.permissions import request_permissions, Permission
from android.storage import app_storage_path

import hashlib
import os
import json
import sys
from logger import logger


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Exception non gérée", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.pin_entre = ""
        self.pin_length = 4

        layout = BoxLayout(orientation='vertical', padding=100, spacing=10)
        self.label = Label(
            text="Entrez votre code",
            font_size=60,
            size_hint=(1, 0.15),
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1)
        )
        self.label.bind(size=self.label.setter("text_size"))
        layout.add_widget(self.label)

        self.pin_label = Label(
            text="", 
            font_size=60, 
            size_hint=(1, 0.2),
            halign="center", 
            valign="middle",
            color=(0, 0, 0, 1)
        )
        self.pin_label.bind(size=self.pin_label.setter("text_size"))
        layout.add_widget(self.pin_label)

        buttons_layout = GridLayout(cols=3, spacing=10, size_hint=(1, 0.5))

        for i in range(1, 10):
            btn = Button(
                text=str(i),
                font_size=60,
                background_normal="",
                background_color=(0.2, 0.6, 0.86, 1),
                color=(1, 1, 1, 1)
            )
            btn.bind(on_release=self.ajouter_chiffre)
            buttons_layout.add_widget(btn)

        btn_effacer = Button(
            text="Effacer",
            font_size=48,
            background_normal="", 
            background_color=(1, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        btn_effacer.bind(on_release=self.effacer)
        buttons_layout.add_widget(btn_effacer)

        btn_zero = Button(
            text="0",
            font_size=60,
            background_normal="", 
            background_color=(0.2, 0.6, 0.86, 1),
            color=(1, 1, 1, 1)
        )
        btn_zero.bind(on_release=self.ajouter_chiffre)
        buttons_layout.add_widget(btn_zero)

        btn_valider = Button(
            text="Valider",
            font_size=48,
            background_normal="", 
            background_color=(0, 0.6, 0, 1),
            color=(1, 1, 1, 1)
        )
        btn_valider.bind(on_release=self.valider_pin)
        buttons_layout.add_widget(btn_valider)

        layout.add_widget(buttons_layout)
        self.add_widget(layout)

    def ajouter_chiffre(self, instance):
        if len(self.pin_entre) < self.pin_length:
            self.pin_entre += instance.text
            self.mettre_a_jour_label()

    def effacer(self, instance):
        self.pin_entre = self.pin_entre[:-1]
        self.mettre_a_jour_label()

    def mettre_a_jour_label(self):
        self.pin_label.text = "*" * len(self.pin_entre)

    def valider_pin(self, instance):
        if len(self.pin_entre) != self.pin_length:
            self.afficher_popup("Erreur", "Veuillez entrer un code PIN à 4 chiffres.")
            return

        config_data = App.get_running_app().config_data
        stored_hash = config_data.get("pin_hash", hashlib.sha256("1234".encode()).hexdigest())
        pin_entre_hash = hashlib.sha256(self.pin_entre.encode()).hexdigest()

        if pin_entre_hash == stored_hash:
            self.pin_entre = ""
            self.mettre_a_jour_label()
            self.manager.current = 'principal'
        else:
            self.afficher_popup("Erreur", "Code PIN incorrect.")
            self.pin_entre = ""
            self.mettre_a_jour_label()

    def afficher_popup(self, titre, message):
        popup = Popup(title=titre,
                      content=Label(text=message),
                      size_hint=(0.6, 0.4))
        popup.open()


class MonApp(App):
    activer_pin = BooleanProperty(True)
    show_total_revenus = BooleanProperty(True)
    show_total_charges = BooleanProperty(True)
    show_total_depenses = BooleanProperty(True)
    show_restant_a_payer = BooleanProperty(True)

    def build(self):
        self.definir_chemin_config()

        self.config_data = self.charger_config()

        self.activer_pin = self.config_data.get("activer_pin", True)
        self.show_total_revenus = self.config_data.get("show_total_revenus", True)
        self.show_total_charges = self.config_data.get("show_total_charges", True)
        self.show_total_depenses = self.config_data.get("show_total_depenses", True)
        self.show_restant_a_payer = self.config_data.get("show_restant_a_payer", True)

        try:
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])
        except Exception as e:
            logger.warning(f"Les permissions Android n'ont pas pu être demandées : {e}")

        sm = ScreenManager()
        if self.activer_pin:
            sm.add_widget(LoginScreen(name='login'))

        sm.add_widget(pageprincipalScreen(name="principal"))
        sm.add_widget(ChargesFixesScreen(name="charges_fixe"))
        sm.add_widget(RevenusScreen(name="revenus"))
        sm.add_widget(DepenseScreen(name="depense"))
        sm.add_widget(ConfigurationScreen(name="config"))
        sm.add_widget(LogsScreen(name="logs"))
        sm.add_widget(EpargneScreen(name="epargne"))

        sm.current = 'login' if self.activer_pin else 'principal'
        return sm

    def definir_chemin_config(self):
        if platform == "android":
            self.storage_path = app_storage_path()
        else:
            self.storage_path = os.getcwd()
        self.config_file = os.path.join(self.storage_path, "config.json")

    def charger_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
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
            with open(self.config_file, "w") as f:
                json.dump(self.config_data, f)
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de la configuration : {e}")


if __name__ == "__main__":
    MonApp().run()            
