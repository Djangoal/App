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
from logger import logger
from functools import partial
import json
import os
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout




# page depense
class DepenseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # proportions réduites
        title_font = Window.height * 0.035
        row_height = Window.height * 0.06
        button_height = Window.height * 0.06
        small_font = Window.height * 0.022
        # 📐 Taille d'écran dynamique
        self.base_width = 1080
        self.scale = Window.width / self.base_width

        layout = BoxLayout(orientation='vertical', padding=5, spacing=5)

        title_label = Label(
            text="Liste des dépenses",
            font_size=title_font,
            size_hint=(1, None),
            height=Window.height * 0.08,
            bold=True,
            color=(0, 0, 0, 1)
        )
        layout.add_widget(title_label)

        self.table_layout = GridLayout(
            cols=4,
            size_hint_y=None,
            spacing=3,
            row_force_default=True,
            row_default_height=row_height
        )
        self.table_layout.bind(minimum_height=self.table_layout.setter('height'))

        self.scroll = ScrollView()
        self.scroll.add_widget(self.table_layout)
        layout.add_widget(self.scroll)

        # Label total
        self.total_depenses_label = Label(
            text="Total des dépenses : 0.00 €",
            size_hint=(1, None),
            height=button_height,
            font_size=title_font * 0.7,
            color=(0, 0.5, 0, 1)
        )
        layout.add_widget(self.total_depenses_label)

        # Boutons navigation
        buttons_layout = BoxLayout(size_hint=(1, None), height=button_height, spacing=5)

        self.btn_voir_charges_fixe = Button(text="Charges fixe", font_size=small_font)
        self.btn_voir_charges_fixe.bind(on_press=lambda x: setattr(self.manager, 'current', 'charges_fixe'))
        buttons_layout.add_widget(self.btn_voir_charges_fixe)

        self.btn_voir_revenus = Button(text="Revenus", font_size=small_font)
        self.btn_voir_revenus.bind(on_press=lambda x: setattr(self.manager, 'current', 'revenus'))
        buttons_layout.add_widget(self.btn_voir_revenus)

        self.btn_retour = Button(text="Retour", font_size=small_font)
        self.btn_retour.bind(on_press=lambda x: setattr(self.manager, 'current', 'principal'))
        buttons_layout.add_widget(self.btn_retour)

        layout.add_widget(buttons_layout)
        self.add_widget(layout)

    def on_pre_enter(self):
        data_file = "donnees_budget.json"
    
        # Lecture des dépenses
        depenses = []
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                depenses = data.get("depense", [])
    
        # === Affichage du tableau ===
        self.table_layout.clear_widgets()
    
        header_font = dp(18 * self.scale)
        row_font = dp(16 * self.scale)
    
        # --- En-têtes avec proportions ---
        self.table_layout.add_widget(Label(
            text="[b]Date[/b]", markup=True, color=(0, 0, 0, 1),
            font_size=header_font, size_hint_x=0.25
        ))
        self.table_layout.add_widget(Label(
            text="[b]Nom[/b]", markup=True, color=(0, 0, 0, 1),
            font_size=header_font, size_hint_x=0.4
        ))
        self.table_layout.add_widget(Label(
            text="[b]Montant[/b]", markup=True, color=(0, 0, 0, 1),
            font_size=header_font, size_hint_x=0.25
        ))
        self.table_layout.add_widget(Label(
            text="", markup=True, color=(0, 0, 0, 1),
            font_size=header_font, size_hint_x=0.1
        ))
    
        # --- Lignes du tableau ---
        for index, item in enumerate(depenses):
            self.table_layout.add_widget(Label(
                text=item['date'],
                color=(0, 0, 0, 1),
                font_size=row_font, size_hint_x=0.25
            ))
            self.table_layout.add_widget(Label(
                text=item['nom'],
                color=(0, 0, 0, 1),
                font_size=row_font, size_hint_x=0.4
            ))
            self.table_layout.add_widget(Label(
                text=f"{item['montant']:.2f} €",
                color=(0, 0, 0, 1),
                font_size=row_font, size_hint_x=0.25
            ))
    
            # Colonne Action (bouton supprimer)
            container = AnchorLayout(anchor_x="center", anchor_y="center", size_hint_x=0.1)
            btn_suppr = Button(
                text="X",
                font_size=row_font,
                size_hint=(None, None),  # on contrôle largeur et hauteur
                size=(dp(40), dp(20)),   # largeur et hauteur fixes
                background_color=(1, 0, 0, 1)
            )
            btn_suppr.bind(on_press=lambda btn, idx=index: self.afficher_confirmation_suppression(idx))
            container.add_widget(btn_suppr)
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
            size_hint=(1, 1),
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
            size_hint=(0.8, 0.3),  # 80% largeur, 30% hauteur de l'écran
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
        