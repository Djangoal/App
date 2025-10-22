from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.app import App

from config.popup import afficher_popup
import hashlib

class PinSection(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=Window.height*0.01, padding=Window.height*0.01, **kwargs)
        self.size_hint_y = None
        self.height = Window.height*0.21

        # Fond encadré bleu
        with self.canvas.before:
            Color(0.2, 0.6, 0.86, 1)  # bleu
            self.rect = RoundedRectangle(radius=[10])
        self.bind(pos=self.update_rect, size=self.update_rect)

        app = App.get_running_app()

        # Ligne du switch
        switch_line = BoxLayout(orientation='horizontal', size_hint_y=None, height=Window.height*0.05)
        switch_label = Label(text="Activer le code PIN", size_hint_x=0.9, font_size=Window.height*0.025)
        self.switch_pin = Switch(active=app.activer_pin)
        self.switch_pin.bind(active=self.toggle_pin)
        switch_line.add_widget(switch_label)
        switch_line.add_widget(self.switch_pin)

        # Champs PIN
        self.new_pin_input = TextInput(
            hint_text="Nouveau PIN (4 chiffres)",
            password=False,
            input_filter='int',
            multiline=False,
            size_hint_y=None,
            height=Window.height*0.04,
            font_size=Window.height*0.025
        )
        self.confirm_pin_input = TextInput(
            hint_text="Confirmer PIN",
            password=False,
            input_filter='int',
            multiline=False,
            size_hint_y=None,
            height=Window.height*0.04,
            font_size=Window.height*0.025
        )

        # Bouton enregistrer
        btn_enregistrer = Button(
            text="Enregistrer le PIN",
            size_hint_y=None,
            height=Window.height*0.04,
            font_size=Window.height*0.025
        )
        btn_enregistrer.bind(on_press=self.changer_pin)

        # Ajout widgets
        self.add_widget(switch_line)
        self.add_widget(self.new_pin_input)
        self.add_widget(self.confirm_pin_input)
        self.add_widget(btn_enregistrer)

    # =================== Méthodes PIN ===================
    def toggle_pin(self, instance, value):
        app = App.get_running_app()
        pin_hash = app.config_manager.data.get("pin_hash", "")
        if value and not pin_hash:
            # Annule l'activation si aucun PIN défini
            self.switch_pin.active = False
            afficher_popup("Vous devez d'abord définir un code PIN avant de l'activer.", "Erreur")
            return
        app.activer_pin = value
        app.config_manager["activer_pin"] = value
        app.sauvegarder_config()

    def changer_pin(self, instance):
        nouveau_pin = self.new_pin_input.text.strip()
        confirmation = self.confirm_pin_input.text.strip()
        if len(nouveau_pin) != 4 or not nouveau_pin.isdigit():
            afficher_popup("Le PIN doit contenir 4 chiffres.", "Erreur")
            return
        if nouveau_pin != confirmation:
            afficher_popup("Les deux codes PIN ne correspondent pas.", "Erreur")
            return
        app = App.get_running_app()
        pin_hash = hashlib.sha256(nouveau_pin.encode()).hexdigest()
        app.config_manager["pin_hash"] = pin_hash
        app.sauvegarder_config()
        afficher_popup("Le code PIN a été modifié.", "Succès")
        self.new_pin_input.text = ""
        self.confirm_pin_input.text = ""

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size