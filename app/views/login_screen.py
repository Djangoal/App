# login_screen.py
import hashlib
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.metrics import sp


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.pin_entre = ""
        self.pin_length = 4

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Label "Entrez votre code"
        self.label = Label(
            text="Entrez votre code",
            font_size=sp(26),
            size_hint=(1, 0.2),
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1)
        )
        self.label.bind(size=self.label.setter("text_size"))
        layout.add_widget(self.label)

        # Label PIN (****)
        self.pin_label = Label(
            text="",
            font_size=sp(32),
            size_hint=(1, 0.2),
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1)
        )
        self.pin_label.bind(size=self.pin_label.setter("text_size"))
        layout.add_widget(self.pin_label)

        # Clavier numérique
        buttons_layout = GridLayout(
            cols=3,
            spacing=10,
            size_hint=(1, 0.6)
        )

        # Chiffres 1-9
        for i in range(1, 10):
            btn = Button(
                text=str(i),
                font_size=sp(28),
                background_normal="",
                background_color=(0.2, 0.6, 0.86, 1),
                color=(1, 1, 1, 1)
            )
            btn.bind(on_release=self.ajouter_chiffre)
            buttons_layout.add_widget(btn)

        # Effacer
        btn_effacer = Button(
            text="<-",
            font_size=sp(22),
            background_normal="",
            background_color=(1, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        btn_effacer.bind(on_release=self.effacer)
        buttons_layout.add_widget(btn_effacer)

        # 0
        btn_zero = Button(
            text="0",
            font_size=sp(28),
            background_normal="",
            background_color=(0.2, 0.6, 0.86, 1),
            color=(1, 1, 1, 1)
        )
        btn_zero.bind(on_release=self.ajouter_chiffre)
        buttons_layout.add_widget(btn_zero)

        # Valider
        btn_valider = Button(
            text="OK",
            font_size=sp(22),
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
        popup = Popup(
            title=titre,
            content=Label(text=message),
            size_hint=(0.6, 0.4)
        )
        popup.open()