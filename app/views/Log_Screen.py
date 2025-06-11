from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from utils.logger import init_logger

class LogScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.log_display = TextInput(readonly=True, size_hint=(1, 1), font_size=12)
        self.add_widget(self.log_display)

        # Initialise le logger
        self.logger = init_logger(self.update_log)

    def update_log(self, logs):
        self.log_display.text = logs
