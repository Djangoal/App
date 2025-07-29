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
from cercled_checkbox import CercledCheckbox
from kivy.graphics import Color, Line
from date_input import DateInput
from utils import calculer_total_charges_restantes
import math




class pageprincipalScreen(Screen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        app = App.get_running_app()
        app.bind(show_total_revenus=self.update_affichage_revenus)
        app.bind(show_total_charges=self.update_affichage_charges)
        app.bind(show_total_depenses=self.update_affichage_depenses)
        
        # ... après avoir créé le label et ajouté à l'écran
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
            color=(0.2, 0.4, 1, 1)
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
            Color(1, 0.6, 0.6, 1)
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
        checkbox_wrapper = BoxLayout(size_hint=(1, None), height=110, padding=10)
        
        with checkbox_wrapper.canvas.before:
            # Encadrement noir
            Color(0, 0, 0, 1)
            self.checkbox_border = Rectangle(size=(checkbox_wrapper.width + 4, checkbox_wrapper.height + 4),
                                             pos=(checkbox_wrapper.x - 2, checkbox_wrapper.y - 2))
        
            # Fond orange
            Color(1, 0.6, 0.3, 1)
            self.checkbox_bg = Rectangle(size=checkbox_wrapper.size, pos=checkbox_wrapper.pos)
        
        # Fonction de mise à jour des positions et tailles
        def update_checkbox_canvas(instance, value):
            self.checkbox_bg.size = instance.size
            self.checkbox_bg.pos = instance.pos
            self.checkbox_border.size = (instance.width + 4, instance.height + 4)
            self.checkbox_border.pos = (instance.x - 2, instance.y - 2)
        
        # Lier les changements de taille/position à la mise à jour du fond + bordure
        checkbox_wrapper.bind(size=update_checkbox_canvas, pos=update_checkbox_canvas)
        
        # ✅ Conteneur centré pour les checkbox
        checkbox_container = BoxLayout(
            orientation='horizontal',
            spacing=40,
            size_hint=(None, None),
            width=600,  # Ajuste si nécessaire
            height=80,
            pos_hint={'center_x': 2, 'center_y': 0.7}
        )
        
        # Création des cases
        self.revenu_cbox = CercledCheckbox("Revenu")
        self.charges_fixe_cbox = CercledCheckbox("Charges Fixes")
        self.depense_cbox = CercledCheckbox("depense")
        
        # Ajout dans le conteneur centré
        checkbox_container.add_widget(self.revenu_cbox)
        checkbox_container.add_widget(self.charges_fixe_cbox)
        checkbox_container.add_widget(self.depense_cbox)
        
        # Ajout du conteneur dans le fond encadré
        checkbox_wrapper.add_widget(checkbox_container)
        
        main_layout.add_widget(checkbox_wrapper)
        
        
        # Bouton valider
        self.valider_btn = Button(
            text="Valider",
            size_hint=(1, None),
            height=200,
            background_color=(0.2, 0.6, 0.86, 1)
        )
        self.valider_btn.bind(on_press=self.ajouter_valeur)
        main_layout.add_widget(self.valider_btn)
        
        main_layout.add_widget(BoxLayout())

        # Labels des totaux par catégorie
        
        
        
        self.total_charges_restantes_label = Label(
            text="restant a payer : 0.00 €",
            font_size=32,
            size_hint=(1, None),
            height=50,
            halign='center',
            valign='middle',
            padding=(0, 10),  # (horizontal, vertical)
            color=(0, 0, 0, 1)
        )
        self.total_charges_restantes_label.bind(size=self.total_charges_restantes_label.setter('text_size'))
        main_layout.add_widget(self.total_charges_restantes_label)
        
        
        
        
        self.label_revenus = Label(
            text="Revenus : 0.00 €",
            font_size=32,
            size_hint=(1, None),
            height=50,
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1)
        )
        self.label_revenus.bind(size=self.label_revenus.setter('text_size'))
        main_layout.add_widget(self.label_revenus)

        self.label_charges = Label(
            text="Charges Fixes : 0.00 €",
            font_size=32,
            size_hint=(1, None),
            height=50,
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1)
        )
        self.label_charges.bind(size=self.label_charges.setter('text_size'))
        main_layout.add_widget(self.label_charges)

        self.label_depenses = Label(
            text="Dépenses : 0.00 €",
            font_size=32,
            size_hint=(1, None),
            height=50,
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1)
        )
        self.label_depenses.bind(size=self.label_depenses.setter('text_size'))
        main_layout.add_widget(self.label_depenses)
        
        self.label_economie = Label(
            text="Économie depense arrondi : 0.00 €",
             font_size=32,
            size_hint=(1, None),
            height=50,
            halign='center',
            valign='middle',
            padding=(0, 10),  # (horizontal, vertical)
            color=(0, 0, 0, 1)
        )
        main_layout.add_widget(self.label_economie)
        self.mise_a_jour_economie()

        # Conteneur horizontal pour les deux labels
        labels_row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=80)
        
        # Label de gauche (Solde)
        self.solde_label = Label(
            text="Solde actuel : 0.00 €",
            font_size=40,
            size_hint=(0.5, 1),
            halign='left',
            valign='middle',
            color=(1, 0, 0, 1)
        )
        self.solde_label.bind(size=self.solde_label.setter('text_size'))
        
        # Label de droite (Fin de mois)
        self.fin_label = Label(
            text="fin_de_mois : 0.00 €",
            font_size=40,
            size_hint=(0.5, 1),
            halign='right',
            valign='middle',
            color=(1, 0, 0, 1)
        )
        self.fin_label.bind(size=self.fin_label.setter('text_size'))
        
        # Ajout des deux labels au même conteneur
        labels_row.add_widget(self.solde_label)
        labels_row.add_widget(self.fin_label)
        
        # Ajout du conteneur au layout principal
        main_layout.add_widget(labels_row)
        
        
        
        
        self.calculer_restant_a_payer()

        # Navigation
        bottom_layout = BoxLayout(size_hint=(1, None), height=100, spacing=10)
        self.bouton_page_charges = Button(text="Charges")
        self.bouton_page_revenus = Button(text="Revenus")
        self.bouton_page_depense = Button(text="Dépenses")
        self.bouton_page_epargne= Button(text="epargne")
        self.bouton_page_config = Button(
            background_normal='config.png',
            background_down='config.png',
            size_hint=(None, None),
            size=(100, 100)
        )

        self.bouton_page_charges.bind(on_press=partial(self.changer_ecran, "charges_fixe"))
        self.bouton_page_epargne.bind(on_press=partial(self.changer_ecran, "epargne"))
        self.bouton_page_revenus.bind(on_press=partial(self.changer_ecran, "revenus"))
        self.bouton_page_depense.bind(on_press=partial(self.changer_ecran, "depense"))
        self.bouton_page_config.bind(on_press=partial(self.changer_ecran, "config"))

        bottom_layout.add_widget(self.bouton_page_config)
        bottom_layout.add_widget(self.bouton_page_charges)
        bottom_layout.add_widget(self.bouton_page_revenus)
        bottom_layout.add_widget(self.bouton_page_depense)
        bottom_layout.add_widget(self.bouton_page_epargne)
        main_layout.add_widget(bottom_layout)
         
        self.charger_donnees()
        self.mettre_a_jour_labels()
        self.calculer_restant_a_payer()
        # Appliquer l'état initial des totaux
        self.update_affichage_revenus(app, app.show_total_revenus)
        self.update_affichage_charges(app, app.show_total_charges)
        self.update_affichage_depenses(app, app.show_total_depenses)
        
    def on_pre_enter(self):
        self.charger_donnees()        
        self.mettre_a_jour_labels()
        self.mise_a_jour_economie()
        self.appliquer_config()
        
    def ajouter_valeur(self, instance):
        try:
            montant = float(self.montant_input.text)
            nom = self.nom_input.text.strip()
            date = self.date_input.text.strip()
    
            if not nom or not date:
                return
    
            if self.revenu_cbox.active:
                categorie = 'revenu'
            elif self.charges_fixe_cbox.active:
                categorie = 'charges_fixe'
                montant = -abs(montant)
            elif self.depense_cbox.active:
                categorie = 'depense'
                montant = -abs(montant)
            else:
                return
    
            nouvelle_entree = {
                "nom": nom,
                "date": date,
                "montant": montant
            }
    
            data = {}
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
    
            for cat in ['revenu', 'charges_fixe', 'depense']:
                if cat not in data:
                    data[cat] = []
    
            data[categorie].append(nouvelle_entree)
    
            # ✅ Mise à jour des charges à payer
            if categorie == 'charges_fixe':
                charges_a_payer = data.get("charges_a_payer", [])
                charges_a_payer.append({
                    "nom": nom,
                    "date": date,
                    "montant": abs(montant),
                    "reste_a_payer": montant  # négatif
                })
                data["charges_a_payer"] = charges_a_payer
    
            elif categorie == 'depense':
                charges_a_payer = data.get("charges_a_payer", [])
                montant_restant = abs(montant)
    
                for charge in charges_a_payer:
                    if charge["nom"].lower() == nom.lower() and montant_restant > 0:
                        if abs(charge["reste_a_payer"]) >= montant_restant:
                            charge["reste_a_payer"] += montant_restant  # vers 0
                            montant_restant = 0
                        else:
                            montant_restant -= abs(charge["reste_a_payer"])
                            charge["reste_a_payer"] = 0
    
                data["charges_a_payer"] = charges_a_payer
    
            # ✅ Écriture dans le fichier AVANT de mettre à jour l'interface
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
    
            # ✅ Réinitialisation des champs
            self.nom_input.text = ""
            self.date_input.text = ""
            self.montant_input.text = ""
            self.revenu_cbox.active = False
            self.charges_fixe_cbox.active = False
            self.depense_cbox.active = False
    
            # ✅ Mise à jour de l'interface (les données JSON sont désormais à jour)
            self.charger_donnees()
            self.mettre_a_jour_labels()
            self.calculer_restant_a_payer()
            self.maj_total_charges_restantes()
            self.mise_a_jour_economie()
    
        except ValueError:
            print("Montant invalide")
            
            
    
    
    def charger_donnees(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.soldes = data.get("soldes", [])
                self.mettre_a_jour_labels()
                self.calculer_restant_a_payer()
                
################################################################calcul et mise a jour solde  ######                      
    
    def maj_total_charges_restantes(self):
        total_restant = calculer_total_charges_restantes()
        self.total_charges_restantes_label.text = f"Total charges à payer : {abs(total_restant):.2f} €"
  
    def calculer_restant_a_payer(self):
        chemin_fichier = self.data_file
        total_restant = 0.0
    
        if os.path.exists(chemin_fichier):
            with open(chemin_fichier, "r", encoding="utf-8") as f:
                donnees = json.load(f)
                charges_a_payer = donnees.get("charges_a_payer", [])
                
                for charge in charges_a_payer:
                    montant = charge.get("reste_a_payer", 0.0)
                    if montant < 0:
                        total_restant += montant
    
        self.total_charges_restantes_label.text = f"Total restant à payer : {abs(total_restant):.2f} €"
        
        
    
    def mettre_a_jour_labels(self):
        # Lecture des données JSON
        try:
            with open('donnees_budget.json', 'r', encoding='utf-8') as f:
                donnees = json.load(f)
        except Exception as e:
            print("Erreur lors de la lecture du fichier JSON :", e)
            donnees = {}
        
        # Calcul des totaux
        total_revenus = sum(item.get('montant', 0) for item in donnees.get('revenu', []))
        total_charges = sum(item.get('montant', 0) for item in donnees.get('charges_fixe', []))
        total_depenses = sum(item.get('montant', 0) for item in donnees.get('depense', []))
        
        # ✅ Total du reste à payer dans les charges à payer
        total_reste_a_payer = sum(
            item.get('reste_a_payer', 0) for item in donnees.get('charges_a_payer', [])
        )
        
        # ✅ Mise à jour des labels
        self.label_revenus.text = f"Total Revenus : {total_revenus:.2f} €"
        self.label_charges.text = f"Total Charges Fixes : {abs(total_charges):.2f} €"
        self.label_depenses.text = f"Total Dépenses : {abs(total_depenses):.2f} €"
        
        # ✅ Solde (les dépenses sont déjà négatives)
        solde = total_revenus + total_depenses
        self.solde_label.text = f"Solde actuel : {solde:.2f} €"
        self.solde_label.color = (0.2, 0.4, 1, 1) if solde >= 0 else (1, 0, 0, 1)
        
        # ✅ Fin de mois (revenus - dépenses - reste à payer réel)
        fin_de_mois = total_revenus - abs(total_depenses) - abs(total_reste_a_payer)
        self.fin_label.text = f"Fin de mois : {fin_de_mois:.2f} €"
        self.fin_label.color = (0.2, 0.6, 0.2, 1) if fin_de_mois >= 0 else (1, 0, 0, 1)
        
    
    
 ##################################################################### sauvegarde ###########
 
    def sauvegarder_donnees(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump({"soldes": self.soldes}, f, ensure_ascii=False, indent=4)
            
            
    
##############################################################################################    afficher/masquer totaux      ####
    
    def update_affichage_revenus(self, instance, value):
        self.label_revenus.opacity = 1 if value else 0

    def update_affichage_charges(self, instance, value):
        self.label_charges.opacity = 1 if value else 0

    def update_affichage_depenses(self, instance, value):
        self.label_depenses.opacity = 1 if value else 0
        
    def update_affichage_restant_a_payer(self, instance, value):
        self.total_charges_restantes_label.opacity = 1 if value else 0
        self.total_charges_restantes_label.height = 50 if value else 0
        app.bind(show_restant_a_payer=self.update_affichage_restant_a_payer)
            
            
#################################################################################################         popup        ###########                    
    def afficher_popup(self, titre, message):
        layout =    BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text=message))
        btn = Button(text='Fermer', size_hint=(1, 0.25))
        layout.add_widget(btn)
        popup = Popup(title=titre, content=layout, size_hint=(None, None), size=(300, 200))
        btn.bind(on_release=popup.dismiss)
        popup.open()

##################################################################################################    fonctions         #######


    def appliquer_config(self):
        app = App.get_running_app()
        self.label_revenus.opacity = 1 if app.show_total_revenus else 0
        self.label_charges.opacity = 1 if app.show_total_charges else 0
        self.label_depenses.opacity = 1 if app.show_total_depenses else 0
        self.total_charges_restantes_label.opacity = 1 if app.show_restant_a_payer else 0
        
    def champ(self, hint, height=80):
        return TextInput(hint_text=hint, multiline=False, size_hint=(1, None), height=height)

    def changer_ecran(self, nom_ecran, instance):
        self.manager.current = nom_ecran
        self.mettre_a_jour_labels()
        
    def calculer_total_economie_arrondi(self):
        chemin_fichier = "donnees_budget.json"
        total = 0

        if not os.path.exists(chemin_fichier):
            return 0.0

        try:
            with open(chemin_fichier, "r", encoding="utf-8") as f:
                donnees = json.load(f)
                for dep in donnees.get("depense", []):
                    montant = abs(float(dep["montant"]))
                    economie = math.ceil(montant) - montant
                    total += economie
        except Exception as e:
            print(f"Erreur lors du calcul : {e}")
            return 0.0

        return round(total, 2)

    def mise_a_jour_economie(self):
        total = self.calculer_total_economie_arrondi()  # ✅ avec self maintenant
        self.label_economie.text = f"Économie depense arrondi : {total:.2f} €"
            
    
    def close_app(self, instance):
        App.get_running_app().stop()
        
