from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.checkbox import CheckBox
from functools import partial
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
import json
from kivy.uix.widget import Widget
import os
from logger import logger
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock
from models.data_manager import DataManager
Window.clearcolor = (1, 1, 1, 1)

class CercledCheckbox(BoxLayout):
    def __init__(self, label_text, **kwargs):
        super().__init__(orientation='horizontal', spacing=15, size_hint=(None, None), height=60, width=300, **kwargs)

        self.checkbox = CheckBox(group='type', size_hint=(None, None), size=(50, 50))
        self.label = Label(
            text=label_text,
            color=(0, 0, 0, 1),
            font_size=28,
            size_hint=(None, None),
            size=(200, 50),
            halign='left',
            valign='middle'
        )
        self.label.bind(size=self.label.setter('text_size'))

        self.add_widget(self.checkbox)
        self.add_widget(self.label)

        with self.checkbox.canvas.after:
            Color(0, 0, 0, 1)
            self.circle = Line(circle=(self.checkbox.center_x, self.checkbox.center_y, 25), width=1.8)
        self.checkbox.bind(pos=self.update_circle, size=self.update_circle)

    def update_circle(self, *args):
        c_x = self.checkbox.center_x
        c_y = self.checkbox.center_y
        self.circle.circle = (c_x, c_y, 25)

    @property
    def active(self):
        return self.checkbox.active

    @active.setter
    def active(self, val):
        self.checkbox.active = val

class DateInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        # Garde uniquement les chiffres
        substring = ''.join(c for c in substring if c.isdigit())

        # Retirer les '/' existants dans le texte courant
        text = self.text.replace('/', '')

        # Limiter la longueur à 8 caractères (JJMMAAAA)
        if len(text) >= 8:
            return

        new_text = text + substring
        if len(new_text) > 4:
            new_text = new_text[:2] + '/' + new_text[2:4] + '/' + new_text[4:]
        elif len(new_text) > 2:
            new_text = new_text[:2] + '/' + new_text[2:]
        else:
            new_text = new_text

        self.text = new_text
        # Positionner le curseur à la fin
        self.cursor = (len(self.text), 0)

class pageprincipalScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        app = App.get_running_app()
        app.bind(show_total_revenus=self.update_affichage_revenus)
        app.bind(show_total_charges=self.update_affichage_charges)
        app.bind(show_total_depenses=self.update_affichage_depenses)
        # ... après avoir créé le label et ajouté à l'écran
        app = App.get_running_app()
        app.bind(show_restant_a_payer=self.update_affichage_restant_a_payer)
        self.update_affichage_restant_a_payer(app,               app.show_restant_a_payer)
        
        self.data_file = "donnees_budget.json"
        self.soldes = []
        self.total = 0
        self.main_layout = BoxLayout(orientation='vertical')
        
        # --- Layout principal ---
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # --- Barre de titre avec bouton de fermeture ---
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        with header.canvas.before:
            Color(1, 0, 0, 1)
            self.header_bg = Rectangle(size=header.size, pos=header.pos)
        header.bind(size=lambda w, s: setattr(self.header_bg, 'size', s),
                       pos=lambda w, p: setattr(self.header_bg, 'pos', p))

        title = Label(
            text='[b]Mon Budget Perso[/b]',
            markup=True,
            font_size=74,
            halign='center',
            valign='middle',
            size_hint=(1, 1),
            height=40,
            color=(0.2, 0.4, 0.86, 1)
        )
        title.bind(size=title.setter('text_size'))

        close_button = Button(
            text='X',
            size_hint=(0.2, 1),
            width=40,
            background_color=(0.2, 0.4, 0.86, 1),
            color=(1, 0, 0, 1),
            font_size=84
        )
        close_button.bind(on_release=self.close_app)

        header.add_widget(title)
        header.add_widget(close_button)
        layout.add_widget(header)

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        main_layout.add_widget(Label(size_hint=(1, None), height=30))

        layout.add_widget(main_layout)
        self.add_widget(layout)

        # Formulaire de saisie
        input_wrapper = BoxLayout(size_hint=(1, None), height=280, padding=2)
        with input_wrapper.canvas.before:
            Color(0, 0, 0, 1)
            self.border_rect = Rectangle(size=input_wrapper.size, pos=input_wrapper.pos)
        input_wrapper.bind(size=lambda w, s: setattr(self.border_rect, 'size', s),
                           pos=lambda w, p: setattr(self.border_rect, 'pos', p))

        inner_layout = BoxLayout(orientation='vertical', spacing=5, padding=10, size_hint=(1, 1))
        with inner_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.bg_rect = Rectangle(size=inner_layout.size, pos=inner_layout.pos)
        inner_layout.bind(size=lambda w, s: setattr(self.bg_rect, 'size', s),
                          pos=lambda w, p: setattr(self.bg_rect, 'pos', p))

        self.nom_input = self.champ("Nom", 80)
        self.date_input = DateInput(hint_text="Date (jj/mm/aaaa)", multiline=False, size_hint=(1, None), height=80)
        self.montant_input = self.champ("Montant", 80)

        inner_layout.add_widget(self.nom_input)
        inner_layout.add_widget(self.date_input)
        inner_layout.add_widget(self.montant_input)
        input_wrapper.add_widget(inner_layout)

        main_layout.add_widget(input_wrapper)
        
        # Catégories
        checkbox_wrapper = BoxLayout(size_hint=(1, None), height=110, padding=10, spacing=40)
        with checkbox_wrapper.canvas.before:
            Color(1, 1, 1, 1)
            self.checkbox_bg = Rectangle(size=checkbox_wrapper.size, pos=checkbox_wrapper.pos)
        checkbox_wrapper.bind(size=lambda w, s: setattr(self.checkbox_bg, 'size', s),
                              pos=lambda w, p: setattr(self.checkbox_bg, 'pos', p))

        self.revenu_cbox = CercledCheckbox("Revenu")
        self.charges_fixe_cbox = CercledCheckbox("Charges Fixes")
        self.depense_cbox = CercledCheckbox("depense")

        checkbox_wrapper.add_widget(self.revenu_cbox)
        checkbox_wrapper.add_widget(self.charges_fixe_cbox)
        checkbox_wrapper.add_widget(self.depense_cbox)
        main_layout.add_widget(checkbox_wrapper)

        main_layout.add_widget(BoxLayout())

        # Labels des totaux par catégorie
        
        
        self.label_restant_a_payer = Label(
            text="Total restant a payer : 0.00 €",
            font_size=32,
            size_hint=(1, None),
            height=50,
            halign='left',
            valign='middle',
            color=(0, 0, 0, 1)
        )
        self.label_restant_a_payer.bind(size=self.label_restant_a_payer.setter('text_size'))
        main_layout.add_widget(self.label_restant_a_payer)
        
        
        self.label_revenus = Label(
            text="Total Revenus : 0.00 €",
            font_size=32,
            size_hint=(1, None),
            height=50,
            halign='left',
            valign='middle',
            color=(0, 0, 0, 1)
        )
        self.label_revenus.bind(size=self.label_revenus.setter('text_size'))
        main_layout.add_widget(self.label_revenus)

        self.label_charges = Label(
            text="Total Charges Fixes : 0.00 €",
            font_size=32,
            size_hint=(1, None),
            height=50,
            halign='left',
            valign='middle',
            color=(0, 0, 0, 1)
        )
        self.label_charges.bind(size=self.label_charges.setter('text_size'))
        main_layout.add_widget(self.label_charges)

        self.label_depenses = Label(
            text="Total Dépenses : 0.00 €",
            font_size=32,
            size_hint=(1, None),
            height=50,
            halign='left',
            valign='middle',
            color=(0, 0, 0, 1)
        )
        self.label_depenses.bind(size=self.label_depenses.setter('text_size'))
        main_layout.add_widget(self.label_depenses)

        self.solde_label = Label(
            text="Solde : 0.00 €",
            font_size=40,
            size_hint=(1, None),
            height=80,
            halign='center',
            valign='middle',
            color=(1, 0, 0, 1)
        )
        self.solde_label.bind(size=self.solde_label.setter('text_size'))
        main_layout.add_widget(self.solde_label)
        
        # Bouton valider
        self.valider_btn = Button(
            text="Valider",
            size_hint=(1, None),
            height=200,
            background_color=(0.2, 0.6, 0.86, 1)
        )
        self.valider_btn.bind(on_press=self.ajouter_valeur)
        main_layout.add_widget(self.valider_btn)

        # Navigation
        bottom_layout = BoxLayout(size_hint=(1, None), height=100, spacing=10)
        self.bouton_page_charges = Button(text="Charges Fixes")
        self.bouton_page_revenus = Button(text="Revenus")
        self.bouton_page_depense = Button(text="Dépenses")
        self.bouton_page_config = Button(
            background_normal='config.png',
            background_down='config.png',
            size_hint=(None, None),
            size=(100, 100)
        )

        self.bouton_page_charges.bind(on_press=partial(self.changer_ecran, "charges_fixe"))
        self.bouton_page_revenus.bind(on_press=partial(self.changer_ecran, "revenus"))
        self.bouton_page_depense.bind(on_press=partial(self.changer_ecran, "depense"))
        self.bouton_page_config.bind(on_press=partial(self.changer_ecran, "config"))

        bottom_layout.add_widget(self.bouton_page_config)
        bottom_layout.add_widget(self.bouton_page_charges)
        bottom_layout.add_widget(self.bouton_page_revenus)
        bottom_layout.add_widget(self.bouton_page_depense)
        main_layout.add_widget(bottom_layout)



        self.charger_donnees()
        self.mettre_a_jour_labels()
        # Appliquer l'état initial des totaux
        self.update_affichage_revenus(app, app.show_total_revenus)
        self.update_affichage_charges(app, app.show_total_charges)
        self.update_affichage_depenses(app, app.show_total_depenses)
        self.update_affichage_restant_a_payer(app, app.show_restant_a_payer)

    def champ(self, hint, height=80):
        return TextInput(hint_text=hint, multiline=False, size_hint=(1, None), height=height)

    def update_affichage_revenus(self, instance, value):
        self.label_revenus.opacity = 1 if value else 0

    def update_affichage_charges(self, instance, value):
        self.label_charges.opacity = 1 if value else 0

    def update_affichage_depenses(self, instance, value):
        self.label_depenses.opacity = 1 if value else 0
        
    def update_affichage_restant_a_payer(self,      instance, value):
        if hasattr(self, 'label_restant_a_payer'):
           self.label_restant_a_payer.opacity = 1     if value else 0
           self.label_restant_a_payer.disabled = not value
    
    
        
        
    def changer_ecran(self, nom_ecran, instance):
        self.manager.current = nom_ecran

    def ajouter_valeur(self, instance):
        try:
            montant = float(self.montant_input.text)
            nom = self.nom_input.text.strip()
            date = self.date_input.text.strip()
    
            if not nom or not date:
                return  # Empêche l'enregistrement si un champ est vide
    
            if self.revenu_cbox.active:
                categorie = 'revenu'
            elif self.charges_fixe_cbox.active:
                categorie = 'charges_fixe'
                montant = -abs(montant)  # montant négatif pour charge fixe
            elif self.depense_cbox.active:
                categorie = 'depense'
                montant = -abs(montant)  # montant négatif pour dépense
            else:
                return  # Aucune catégorie sélectionnée
    
            nouvelle_entree = {
                "nom": nom,
                "date": date,
                "montant": montant
            }
    
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {}
    
            for cat in ['revenu', 'charges_fixe', 'depense']:
                if cat not in data:
                    data[cat] = []
    
            data[categorie].append(nouvelle_entree)
    
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
    
            # Réinitialiser les champs
            self.nom_input.text = ""
            self.date_input.text = ""
            self.montant_input.text = ""
            self.revenu_cbox.active = False
            self.charges_fixe_cbox.active = False
            self.depense_cbox.active = False
    
            self.charger_donnees()
            self.mettre_a_jour_labels()
    
        except ValueError:
            print("Montant invalide")
        
                                
    def sauvegarder_donnees(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump({"soldes": self.soldes}, f, ensure_ascii=False, indent=4)

    def charger_donnees(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.soldes = data.get("soldes", [])
                self.mettre_a_jour_labels()
    def on_pre_enter(self):
          self.charger_donnees()
    def lire_total_charges_a_payer(self):
        try:
            with open("donnees_budget.json", "r", encoding='utf-8') as f:
                data = json.load(f)
            return data.get("total_charges_a_payer", 0)
        except Exception as e:
            print(f"Erreur lecture total charges : {e}")
            return 0
    
    def mettre_a_jour_labels(self):
        try:
            with open('donnees_budget.json', 'r', encoding='utf-8') as f:
                donnees = json.load(f)
        except Exception as e:
            print("Erreur lors de la lecture du fichier JSON :", e)
            donnees = {}
    
        total_revenus = sum(item.get('montant', 0) for item in donnees.get('revenu', []))
        total_charges = sum(item.get('montant', 0) for item in donnees.get('charges_fixe', []))
        total_depenses = sum(item.get('montant', 0) for item in donnees.get('depense', []))
        total_a_payer = sum(item.get('montant', 0) for item in donnees.get('a_payer', []))
    
        self.label_revenus.text = f"Total Revenus : {total_revenus:.2f} €"
        self.label_charges.text = f"Total Charges Fixes : {abs(total_charges):.2f} €"
        self.label_depenses.text = f"Total Dépenses : {abs(total_depenses):.2f} €"
        self.label_restant_a_payer.text = f"Restant à payer : {abs(total_a_payer):.2f} €"
    
        # Calcul du solde
        solde = total_revenus + total_charges + total_depenses 
        self.solde_label.text = f"Solde : {solde:.2f} €"
            
    
        
    def afficher_popup(self, titre, message):
        layout =    BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text=message))
        btn = Button(text='Fermer', size_hint=(1, 0.25))
        layout.add_widget(btn)
        popup = Popup(title=titre, content=layout, size_hint=(None, None), size=(300, 200))
        btn.bind(on_release=popup.dismiss)
        popup.open()

    def close_app(self, instance):
        App.get_running_app().stop()
        