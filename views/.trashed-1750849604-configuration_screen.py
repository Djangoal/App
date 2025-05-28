import os
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class ConfigurationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        titre = Label(text="Page de Configuration", font_size=40, color=(0, 0, 0, 1))
        layout.add_widget(titre)

        # Boutons cacher/afficher les totaux
        self.bouton_revenu = Button(text="Masquer le total des revenus", size_hint=(1, None), height=100)
        self.bouton_revenu.bind(on_press=self.toggle_revenu)
        layout.add_widget(self.bouton_revenu)

        self.bouton_charges = Button(text="Masquer le total des charges fixes", size_hint=(1, None), height=100)
        self.bouton_charges.bind(on_press=self.toggle_charges)
        layout.add_widget(self.bouton_charges)

        self.bouton_depenses = Button(text="Masquer le total des dépenses", size_hint=(1, None), height=100)
        self.bouton_depenses.bind(on_press=self.toggle_depenses)
        layout.add_widget(self.bouton_depenses)

        # Réinitialisation
        bouton_reset = Button(text="Réinitialiser les données", size_hint=(1, None), height=100)
        bouton_reset.bind(on_press=self.reinitialiser_donnees)
        layout.add_widget(bouton_reset)

        # Retour
        bouton_retour = Button(text="Retour", size_hint=(1, None), height=100)
        bouton_retour.bind(on_press=self.retour_page_principale)
        layout.add_widget(bouton_retour)

        self.add_widget(layout)

    def toggle_revenu(self, instance):
        principal = self.manager.get_screen("principal")
        if principal.total_revenu_label.opacity == 1:
            principal.total_revenu_label.opacity = 0
            instance.text = "Afficher le total des revenus"
        else:
            principal.total_revenu_label.opacity = 1
            instance.text = "Masquer le total des revenus"

    def toggle_charges(self, instance):
        principal = self.manager.get_screen("principal")
        if principal.total_charges_label.opacity == 1:
            principal.total_charges_label.opacity = 0
            instance.text = "Afficher le total des charges fixes"
        else:
            principal.total_charges_label.opacity = 1
            instance.text = "Masquer le total des charges fixes"

    def toggle_depenses(self, instance):
        principal = self.manager.get_screen("principal")
        if principal.total_depenses_label.opacity == 1:
            principal.total_depenses_label.opacity = 0
            instance.text = "Afficher le total des dépenses"
        else:
            principal.total_depenses_label.opacity = 1
            instance.text = "Masquer le total des dépenses"

    def reinitialiser_donnees(self, instance):
        if os.path.exists("donnees_budget.json"):
            os.remove("donnees_budget.json")
        principal = self.manager.get_screen("principal")
        principal.recharger_donnees()  # à adapter à ta méthode de mise à jour de l'écran principal

    def retour_page_principale(self, instance):
        self.manager.current = "principal"