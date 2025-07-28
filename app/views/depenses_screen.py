from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from components.entry_row import EntryRow
from controllers.budget_controller import BudgetController
from kivy.uix.screenmanager import Screen
from logger import logger
from functools import partial
import json
import os
from kivy.app import App
from kivy.uix.popup import Popup




# page depense
class DepenseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        title_label = Label(text="Liste des depenses", font_size=48, size_hint=(1, None), height=100, bold=True,
                            color=(0, 0, 0, 1))
        layout.add_widget(title_label)

        self.table_layout = GridLayout(cols=4, size_hint_y=None, spacing=5,
                                       row_force_default=True, row_default_height=60)
        self.table_layout.bind(minimum_height=self.table_layout.setter('height'))

        self.scroll = ScrollView()
        self.scroll.add_widget(self.table_layout)
        layout.add_widget(self.scroll)

        # Label fixe pour afficher le total des dépenses
        self.total_depenses_label = Label(
            text="Total des dépenses : 0.00 €",
            size_hint=(1, None),
            height=50,
            font_size=48,
            color=(0, 0.5, 0, 1)
        )
        layout.add_widget(self.total_depenses_label)

        buttons_layout = BoxLayout(size_hint=(1, None), height=60, spacing=10)

        self.btn_voir_charges_fixe = Button(text="Voir charges fixe")
        self.btn_voir_charges_fixe.bind(on_press=lambda x: setattr(self.manager, 'current', 'charges_fixe'))
        buttons_layout.add_widget(self.btn_voir_charges_fixe)

        self.btn_voir_revenus = Button(text="Voir Revenus")
        self.btn_voir_revenus.bind(on_press=lambda x: setattr(self.manager, 'current', 'revenus'))
        buttons_layout.add_widget(self.btn_voir_revenus)

        self.btn_retour = Button(text="Retour")
        self.btn_retour.bind(on_press=lambda x: setattr(self.manager, 'current', 'principal'))
        buttons_layout.add_widget(self.btn_retour)

        layout.add_widget(buttons_layout)
        self.add_widget(layout)

    def on_pre_enter(self):
        
    

        data_file = "donnees_budget.json"
    
        self.table_layout.clear_widgets()
        self.table_layout.add_widget(Label(text="Date", bold=True, color=(0, 0, 0, 1)))
        self.table_layout.add_widget(Label(text="Nom", bold=True, color=(0, 0, 0, 1)))
        self.table_layout.add_widget(Label(text="Montant (€)", bold=True, color=(0, 0, 0, 1)))
        self.table_layout.add_widget(Label(text="Action", bold=True, color=(0, 0, 0, 1)))
    
        # Lecture des dépenses depuis la clé 'depense'
        depenses = []
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                depenses = data.get("depense", [])
    
        for index, item in enumerate(depenses):
            self.table_layout.add_widget(Label(text=item['date'], color=(0, 0, 0, 1)))
            self.table_layout.add_widget(Label(text=item['nom'], color=(0, 0, 0, 1)))
            self.table_layout.add_widget(Label(text=f"{item['montant']:.2f} €", color=(0, 0, 0, 1)))
    
            container = BoxLayout(orientation='horizontal', size_hint_x=1)
            container.add_widget(Widget(size_hint_x=1))  # espace vide à gauche
            btn_suppr = Button(text="X", size_hint=(1, 1), width=50, background_color=(1, 0, 0, 1))
            btn_suppr.bind(on_press=lambda btn, idx=index: self.afficher_confirmation_suppression(idx))
            container.add_widget(btn_suppr)
            container.add_widget(Widget(size_hint_x=1))  # espace vide à droite
            self.table_layout.add_widget(container)
    
        total_depenses = sum(item['montant'] for item in depenses)
        self.total_depenses_label.text = f"Total des dépenses : {total_depenses:.2f} €"

    def supprimer_depense(self, index, *args):
        app = App.get_running_app()
    
        # Charger les données JSON
        try:
            with open('donnees_budget.json', 'r', encoding='utf-8') as f:
                donnees = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            donnees = {}
    
        depenses = donnees.get('depense', [])
    
        # Vérifier l'index et supprimer si valide
        if 0 <= index < len(depenses):
            depense_supprimee = depenses.pop(index)
            donnees['depense'] = depenses
    
            # Vérifie si la dépense supprimée correspond à une charge fixe
            charges_fixes = donnees.get("charges_fixe", [])
            nom_charge = depense_supprimee.get("nom")
    
            # Vérifie si le nom correspond à une charge fixe connue
            noms_charges_fixes = [charge.get("nom") for charge in charges_fixes]
            if nom_charge in noms_charges_fixes:
                # Préparer l’entrée à ajouter
                nouvelle_charge = {
                    "nom": depense_supprimee.get("nom"),
                    "date": depense_supprimee.get("date"),
                    "montant": depense_supprimee.get("montant"),
                    "reste_a_payer": depense_supprimee.get("montant")
                }
    
                # Éviter les doublons exacts dans charges_a_payer
                deja_presente = False
                for charge in donnees.get("charges_a_payer", []):
                    if charge.get("nom") == nouvelle_charge["nom"] and charge.get("date") == nouvelle_charge["date"]:
                        deja_presente = True
                        break
    
                if not deja_presente:
                    donnees.setdefault("charges_a_payer", []).append(nouvelle_charge)
    
            # Sauvegarder les données modifiées
            with open('donnees_budget.json', 'w', encoding='utf-8') as f:
                json.dump(donnees, f, ensure_ascii=False, indent=4)
                
    def afficher_confirmation_suppression(self, index):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
    
        message = Label(
            text="Confirmer la suppression de cette dépense ?",
            size_hint=(1, None),
            height=80,
            halign="center",
            valign="middle"
        )
        message.bind(size=message.setter('text_size'))  # pour centrer le texte
    
        boutons = BoxLayout(size_hint=(1, None), height=100, spacing=20)
        btn_annuler = Button(text="Annuler")
        btn_confirmer = Button(text="Confirmer", background_color=(1, 0, 0, 1))
    
        popup = Popup(
            title="Confirmation",
            content=layout,
            size_hint=(None, None),
            size=(1000, 500),
            auto_dismiss=False
        )
    
        # ✅ Action avec mise à jour immédiate après suppression
        def confirmer_action(instance):
            popup.dismiss()
            self.supprimer_depense(index)
            self.on_pre_enter()  # recharge la liste des dépenses
            
    
        btn_annuler.bind(on_press=popup.dismiss)
        btn_confirmer.bind(on_press=confirmer_action)
    
        boutons.add_widget(btn_annuler)
        boutons.add_widget(btn_confirmer)
    
        layout.add_widget(message)
        layout.add_widget(Widget())  # pousse les boutons vers le bas
        layout.add_widget(boutons)
    
        popup.open()
    
            # Mettre à jour l'affichage
        self.on_pre_enter()
        self.manager.get_screen('principal').mettre_a_jour_labels()
        