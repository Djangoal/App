from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import os
from logger import logger

class LogsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Zone de texte dans un ScrollView
        self.log_view = TextInput(readonly=True, size_hint_y=None, height=1000, font_size=14)
        scroll = ScrollView(size_hint=(1, 0.9))
        scroll.add_widget(self.log_view)
        layout.add_widget(scroll)

        # Bouton retour
        btn_retour = Button(text='Retour', size_hint_y=0.1)
        btn_retour.bind(on_press=self.retour)
        layout.add_widget(btn_retour)

        self.add_widget(layout)
        self.refresh_logs()
        logger.info("Écran Logs chargé")

    def refresh_logs(self):
        try:
            if os.path.exists("app.log"):
                with open("app.log", "r", encoding='utf-8') as f:
                    self.log_view.text = f.read()
                logger.info("Fichier log chargé avec succès")
            else:
                self.log_view.text = "Aucun fichier log trouvé."
                logger.warning("Fichier app.log introuvable")
        except Exception as e:
            logger.error(f"Erreur lors du chargement des logs: {e}")
            self.log_view.text = f"Erreur: {e}"

    def retour(self, instance):
        logger.info("Retour à l'écran Configuration depuis Logs") 
        self.manager.current = 'config'  # ← Doit correspondre au nom utilisé dans add_widget()