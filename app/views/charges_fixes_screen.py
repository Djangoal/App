# Importation des modules Kivy et standard
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
import json
import os
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from utils import lire_et_calculer_charges_a_payer
from kivy.core.window import Window
from kivy.metrics import sp

class ChargesFixesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.charges_a_payer = []  # Liste des charges partiellement payées
        
        # Calcul dynamique de la taille de la police selon la hauteur de l'écran
        self.font_size_label = max(12, Window.height * 0.02)  # 2% de la hauteur, minimum 12

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Hauteurs adaptatives
        btn_height = Window.height * 0.06          # 6% de la hauteur de l'écran
        row_height = Window.height * 0.04          # 4% par ligne du tableau
        max_scroll_height = Window.height * 0.5    # 50% de la hauteur pour ScrollView

        # === Bouton afficher/masquer charges fixes ===
        self.btn_toggle_fixes = Button(text='Afficher les Charges Fixes', size_hint_y=None, height=btn_height)
        self.btn_toggle_fixes.bind(on_release=self.toggle_charges_fixes)
        self.layout.add_widget(self.btn_toggle_fixes)

        # Conteneur tableau charges fixes
        self.table_fixes_container = ScrollView(size_hint=(1, None), height=0)
        self.table_layout = GridLayout(cols=4, size_hint_y=None, spacing=5,
                                       row_force_default=True, row_default_height=row_height)
        self.table_layout.bind(minimum_height=self.table_layout.setter('height'))
        self.table_fixes_container.add_widget(self.table_layout)
        self.layout.add_widget(self.table_fixes_container)

        # Total charges fixes
        self.total_charges_fixes_label = Label(
            text="Total des charges : 0.00 €",
            size_hint=(1, None),
            height=btn_height,
            font_size=sp(15),
            color=(0,0,0,1)
        )
        self.layout.add_widget(self.total_charges_fixes_label)

        # === Bouton afficher/masquer charges à payer ===
        self.btn_toggle_payer = Button(text='Afficher les Charges à Payer', size_hint_y=None, height=btn_height)
        self.btn_toggle_payer.bind(on_release=self.toggle_charges_a_payer)
        self.layout.add_widget(self.btn_toggle_payer)

        # Conteneur tableau charges à payer
        self.table_payer_container = ScrollView(size_hint=(1, None), height=0)
        self.payer_layout = GridLayout(cols=2, size_hint_y=None, spacing=5,
                                       row_force_default=True, row_default_height=row_height)
        self.payer_layout.bind(minimum_height=self.payer_layout.setter('height'))
        self.table_payer_container.add_widget(self.payer_layout)
        self.layout.add_widget(self.table_payer_container)

        # Total restant à payer
        self.total_Charges_à_Payer_label = Label(
            text="Total des charges restant à payer : 0.00 €",
            size_hint=(1, None),
            height=btn_height,
            font_size=sp(15),
            color=(0,0,0,1)
        )
        self.layout.add_widget(self.total_Charges_à_Payer_label)

        # Boutons navigation
        buttons_layout = BoxLayout(size_hint=(1, None), height=btn_height, spacing=10)
        self.btn_voir_revenus = Button(text="Revenus")
        self.btn_voir_revenus.bind(on_press=lambda x: setattr(self.manager, 'current', 'revenus'))
        buttons_layout.add_widget(self.btn_voir_revenus)

        self.btn_voir_depense = Button(text="Dépense")
        self.btn_voir_depense.bind(on_press=lambda x: setattr(self.manager, 'current', 'depense'))
        buttons_layout.add_widget(self.btn_voir_depense)

        self.btn_retour = Button(text="Retour")
        self.btn_retour.bind(on_press=lambda x: setattr(self.manager, 'current', 'principal'))
        buttons_layout.add_widget(self.btn_retour)

        self.layout.add_widget(buttons_layout)
        self.add_widget(self.layout)

        # États d’affichage
        self.fixes_visible = False
        self.payer_visible = False
        self.max_scroll_height = max_scroll_height

    # === Toggle charges fixes ===
    def toggle_charges_fixes(self, instance):
        if self.table_fixes_container.height == 0:
            self.table_fixes_container.height = min(self.table_layout.height, self.max_scroll_height)
            self.btn_toggle_fixes.text = 'Masquer les Charges Fixes'
        else:
            self.table_fixes_container.height = 0
            self.btn_toggle_fixes.text = 'Afficher les Charges Fixes'

    # === Toggle charges à payer ===
    def toggle_charges_a_payer(self, *args):
        self.payer_visible = not self.payer_visible
        self.table_payer_container.height = min(self.payer_layout.height, self.max_scroll_height) if self.payer_visible else 0
        self.btn_toggle_payer.text = 'Masquer les Charges à Payer' if self.payer_visible else 'Afficher les Charges à Payer'

    # === Mise à jour de l’écran lors de l’affichage ===
    def on_pre_enter(self):
        charges_fixes, self.charges_a_payer, total_a_payer = lire_et_calculer_charges_a_payer()
    
        # === Affichage des charges fixes ===
        self.table_layout.clear_widgets()

        # Entêtes
        headers = ["Date", "Nom", "Montant (€)", "Action"]
        for h in headers:
            self.table_layout.add_widget(Label(
                text=f"[b]{h}[/b]",
                markup=True,
                color=(0, 0, 0, 1),
                font_size=self.font_size_label
            ))
        
        # Lignes du tableau
        for index, item in enumerate(charges_fixes):
            self.table_layout.add_widget(Label(
                text=item['date'],
                color=(0, 0, 0, 1),
                font_size=self.font_size_label
            ))
            self.table_layout.add_widget(Label(
                text=item['nom'],
                color=(0, 0, 0, 1),
                font_size=self.font_size_label
            ))
            self.table_layout.add_widget(Label(
                text=f"{item['montant']:.2f} €",
                color=(0, 0, 0, 1),
                font_size=self.font_size_label
            ))
        
            # Bouton "Modifier" dynamique
            anchor = AnchorLayout(anchor_x='center', anchor_y='center')
            btn_modifier = Button(
                text="Modifier",
                size_hint=(0.8, 0.8),  # proportionnel à la cellule
                font_size=self.font_size_label,
                background_color=(0.2, 0.6, 0.8, 1)
            )
            btn_modifier.bind(on_press=lambda btn, idx=index: self.ouvrir_popup_modification(idx))
            anchor.add_widget(btn_modifier)
            self.table_layout.add_widget(anchor)
    
        # === Affichage des charges à payer ===
        self.payer_layout.clear_widgets()
        self.payer_layout.add_widget(Label(text="[b]Nom[/b]", markup=True, color=(0, 0, 0, 1)))
        self.payer_layout.add_widget(Label(text="[b]Reste à payer (€)[/b]", markup=True, color=(0, 0, 0, 1)))
    
        for item in self.charges_a_payer:
            self.payer_layout.add_widget(Label(text=item['nom'], color=(0, 0, 0, 1)))
            reste = item.get('reste_a_payer', 0)
            if reste < 0:
                lbl = Label(text=f"{abs(reste):.2f} €", color=(0.2, 0.4, 1, 1))
            else:
                lbl = Label(text=f"+{reste:.2f} €", color=(0, 0.5, 0, 1))
            self.payer_layout.add_widget(lbl)
    
        # Totaux
        total_charges = sum(item['montant'] for item in charges_fixes)
        self.total_charges_fixes_label.text = f"Total des charges : {abs(total_charges):.2f} €"
        self.total_Charges_à_Payer_label.text = f"Total des charges restant à payer : {total_a_payer:.2f} €"

    # === Affiche le popup de modification d’une charge fixe ===
    def ouvrir_popup_modification(self, index):
        chemin = "donnees_budget.json"
        if os.path.exists(chemin):
            with open(chemin, 'r', encoding='utf-8') as f:
                donnees = json.load(f)
        else:
            donnees = {}
    
        charges_fixes = donnees.get('charges_fixe', [])
        if index >= len(charges_fixes):
            return
    
        charge = charges_fixes[index]
    
        # 🔹 Taille dynamique du texte
        font_size = max(14, Window.height * 0.02)
    
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
    
        # Champs de modification avec tailles adaptées
        
    
        date_input = TextInput(
            text=charge['date'], 
            multiline=False, 
            hint_text="Date",
            font_size=font_size,
            size_hint_y=None, 
            height=font_size * 2
        )
        nom_input = TextInput(
            text=charge['nom'], 
            multiline=False, 
            hint_text="Nom",
            font_size=font_size,
            size_hint_y=None, 
            height=font_size * 2
        )
        montant_input = TextInput(
            text=str(charge['montant']), 
            multiline=False, 
            hint_text="Montant",
            font_size=font_size,
            size_hint_y=None, 
            height=font_size * 2
        )
    
        layout.add_widget(date_input)
        layout.add_widget(nom_input)
        layout.add_widget(montant_input)
    
        # Boutons popup avec tailles proportionnelles
        btns = BoxLayout(size_hint_y=None, height=font_size * 3, spacing=10)
    
        btn_valider = Button(text="Valider", font_size=font_size, background_color=(0, 0.6, 0, 1))
        btn_supprimer = Button(text="Supprimer", font_size=font_size, background_color=(0.8, 0, 0, 1))
        btn_annuler = Button(text="Annuler", font_size=font_size, background_color=(0.5, 0.5, 0.5, 1))
    
        btns.add_widget(btn_valider)
        btns.add_widget(btn_supprimer)
        btns.add_widget(btn_annuler)
    
        layout.add_widget(btns)
    
        # 🔹 Popup adaptée à l'écran (90% largeur, 70% hauteur)
        popup = Popup(
            title="Modifier la charge",
            content=layout,
            size_hint=(0.9, 0.3),
            auto_dismiss=False,
            title_size=font_size * 1.2
        )
    
        

        # Actions des boutons
        btn_valider.bind(on_press=lambda x: self.modifier_charge(index, date_input.text, nom_input.text, montant_input.text, popup))
        btn_supprimer.bind(on_press=lambda x: (self.supprimer_charge(index), popup.dismiss()))
        btn_annuler.bind(on_press=popup.dismiss)

        popup.open()

    # === Enregistre les modifications d'une charge fixe ===
    def modifier_charge(self, index, nouvelle_date, nouveau_nom, nouveau_montant, popup):
        try:
            nouveau_montant = float(nouveau_montant)
        except ValueError:
            return  # Valeur non valide

        chemin = "donnees_budget.json"
        if os.path.exists(chemin):
            with open(chemin, 'r', encoding='utf-8') as f:
                donnees = json.load(f)
        else:
            donnees = {}

        charges_fixes = donnees.get('charges_fixe', [])
        if 0 <= index < len(charges_fixes):
            charge = charges_fixes[index]
            charge['date'] = nouvelle_date
            charge['nom'] = nouveau_nom
            charge['montant'] = nouveau_montant

            donnees['charges_fixe'] = charges_fixes
            with open(chemin, 'w', encoding='utf-8') as f:
                json.dump(donnees, f, indent=4, ensure_ascii=False)

            self.on_pre_enter()  # Recharge l’écran
            popup.dismiss()

    # === Supprime une charge fixe ===
    def supprimer_charge(self, index):
        chemin = "donnees_budget.json"
        if os.path.exists(chemin):
            with open(chemin, 'r', encoding='utf-8') as f:
                donnees = json.load(f)
        else:
            donnees = {}

        charges_fixes = donnees.get('charges_fixe', [])
        if 0 <= index < len(charges_fixes):
            charges_fixes.pop(index)
            donnees['charges_fixe'] = charges_fixes

            with open(chemin, 'w', encoding='utf-8') as f:
                json.dump(donnees, f, indent=4, ensure_ascii=False)

            self.on_pre_enter()  # Recharge l’écran après suppression