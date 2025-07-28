from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import os
from logger import logger, log_path  # Importe aussi log_path

class LogsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # TextInput readonly dans ScrollView pour afficher les logs
        self.log_view = TextInput(readonly=True, font_size=14, size_hint_y=None)
        self.log_view.bind(minimum_height=self.log_view.setter('height'))

        scroll = ScrollView(size_hint=(1, 0.9))
        scroll.add_widget(self.log_view)
        layout.add_widget(scroll)

        # Bouton retour
        btn_retour = Button(text='Retour', size_hint_y=0.1)
        btn_retour.bind(on_press=self.retour)
        layout.add_widget(btn_retour)

        self.add_widget(layout)

        logger.info("Écran Logs chargé")

    def on_pre_enter(self, *args):
        """ Rafraîchit les logs à chaque fois que l'écran est affiché """
        self.refresh_logs()

    def refresh_logs(self):
        try:
            if os.path.exists(log_path):
                with open(log_path, "r", encoding='utf-8') as f:
                    self.log_view.text = f.read()
                logger.info("Fichier log chargé avec succès")
            else:
                self.log_view.text = "Aucun fichier log trouvé."
                logger.warning(f"Fichier {log_path} introuvable")
        except Exception as e:
            logger.error(f"Erreur lors du chargement des logs: {e}")
            self.log_view.text = f"Erreur: {e}"

    def retour(self, instance):
        logger.info("Retour à l'écran Configuration depuis Logs")
        self.manager.current = 'config'