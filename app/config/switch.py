from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.core.window import Window
from kivy.app import App

class SwitchesSection(BoxLayout):
    def __init__(self, parent_screen, **kwargs):
        super().__init__(orientation='vertical', spacing=Window.height*0.015, padding=Window.height*0.015, **kwargs)
        self.parent_screen = parent_screen
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))

        app = App.get_running_app()
        self.switch_revenus = Switch(active=app.show_total_revenus)
        self.switch_charges = Switch(active=app.show_total_charges)
        self.switch_depenses = Switch(active=app.show_total_depenses)
        self.switch_restant_a_payer = Switch(active=app.show_restant_a_payer)

        self.switch_revenus.bind(active=self.on_toggle_revenus)
        self.switch_charges.bind(active=self.on_toggle_charges)
        self.switch_depenses.bind(active=self.on_toggle_depenses)
        self.switch_restant_a_payer.bind(active=self.on_toggle_restant_a_payer)

        self.add_widget(self._create_line("Afficher Revenus", self.switch_revenus))
        self.add_widget(self._create_line("Afficher Charges", self.switch_charges))
        self.add_widget(self._create_line("Afficher Dépenses", self.switch_depenses))
        self.add_widget(self._create_line("Afficher à Payer", self.switch_restant_a_payer))

    def _create_line(self, label_text, widget):
        box = BoxLayout(size_hint_y=None, height=50)
        label = Label(text=label_text, color=(0,0,0,1), size_hint_x=0.7)
        widget.size_hint_x = 0.3
        box.add_widget(label)
        box.add_widget(widget)
        return box

    def on_toggle_revenus(self, instance, value):
        app = App.get_running_app()
        app.show_total_revenus = value
        app.sauvegarder_config()

    def on_toggle_charges(self, instance, value):
        app = App.get_running_app()
        app.show_total_charges = value
        app.sauvegarder_config()

    def on_toggle_depenses(self, instance, value):
        app = App.get_running_app()
        app.show_total_depenses = value
        app.sauvegarder_config()

    def on_toggle_restant_a_payer(self, instance, value):
        app = App.get_running_app()
        app.show_restant_a_payer = value
        app.sauvegarder_config()