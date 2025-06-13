import os
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import BooleanProperty


class ConfigurationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        titre = Label(text="Page de Configuration", font_size=40, color=(0, 0, 0, 1))
        layout.add_widget(titre)

        # Boutons pour afficher/masquer les totaux
        bouton_revenus = Button(text="Afficher/Masquer Total Revenus", size_hint=(1, None), height=100)
        bouton_revenus.bind(on_press=self.on_toggle_revenus)
        layout.add_widget(bouton_revenus)

        bouton_charges = Button(text="Afficher/Masquer Total Charges", size_hint=(1, None), height=100)
        bouton_charges.bind(on_press=self.on_toggle_charges)
        layout.add_widget(bouton_charges)

        bouton_depenses = Button(text="Afficher/Masquer Total Dépenses", size_hint=(1, None), height=100)
        bouton_depenses.bind(on_press=self.on_toggle_depenses)
        layout.add_widget(bouton_depenses)

        # Bouton pour réinitialiser les données
        bouton_reset = Button(text="Réinitialiser les données", size_hint=(1, None), height=100)
        bouton_reset.bind(on_press=self.reinitialiser_donnees)
        layout.add_widget(bouton_reset)

        # Bouton retour
        bouton_retour = Button(text="Retour", size_hint=(1, None), height=100)
        bouton_retour.bind(on_press=self.retour_page_principale)
        layout.add_widget(bouton_retour)

        self.add_widget(layout)

    def on_toggle_revenus(self, instance):
        app = App.get_running_app()
        app.show_total_revenus = not app.show_total_revenus

    def on_toggle_charges(self, instance):
        app = App.get_running_app()
        app.show_total_charges = not app.show_total_charges

    def on_toggle_depenses(self, instance):
        app = App.get_running_app()
        app.show_total_depenses = not app.show_total_depenses

    def reinitialiser_donnees(self, instance):
        if os.path.exists("donnees_budget.json"):
            os.remove("donnees_budget.json")
        self.manager.get_screen("principal").total = 0
        self.manager.get_screen("principal").soldes = []
        self.manager.get_screen("principal").solde_label.text = "Solde: 0.00 €"

    def retour_page_principale(self, instance):
        self.manager.current = "principal"