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
from utils import lire_et_calculer_charges_a_payer

class LimitedTextInput(TextInput):
    max_chars = 13  # limite de caractères

    def insert_text(self, substring, from_undo=False):
        if len(self.text) + len(substring) > self.max_chars:
            substring = substring[:self.max_chars - len(self.text)]
        super(LimitedTextInput, self).insert_text(substring, from_undo=from_undo)





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

       
        
        # --- Barre de titre responsive ---
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        
        # Fond rouge du header
        with header.canvas.before:
            Color(1, 0, 0, 1)
            self.header_bg = Rectangle(size=header.size, pos=header.pos)
        
        header.bind(
            size=lambda w, s: setattr(self.header_bg, 'size', s),
            pos=lambda w, p: setattr(self.header_bg, 'pos', p)
        )
        
        # Titre centré
        title = Label(
            text='[b]Mon Budget Perso[/b]',
            markup=True,
            halign='center',
            valign='middle',
            color=(0.2, 0.4, 1, 1)
        )
        title.bind(size=lambda instance, value: setattr(title, 'text_size', (title.width, title.height)))
        
        # Bouton de fermeture
        close_button = Button(
            text='X',
            size_hint=(None, 1),
            width=Window.width * 0.1,
            background_color=(0.2, 0.4, 0.86, 1),
            background_normal='',  # Assure la couleur sur Android
            color=(1, 0, 0, 1)
        )
        close_button.bind(on_release=self.close_app)
        
        # Ajout des widgets au header
        header.add_widget(title)
        header.add_widget(close_button)
        layout.add_widget(header)
        
        # Fonction pour adapter les tailles dynamiquement
        def update_header_sizes(*args):
            header_height = Window.height * 0.1
            title.font_size = header_height * 0.5  # Texte à moitié de la hauteur du header
            close_button.font_size = header_height * 0.4
            close_button.width = Window.width * 0.1
            title.text_size = (title.width, title.height)  # Recentrage exact du texte
        
        Window.bind(size=update_header_sizes)
        update_header_sizes()
        
        
        


        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        main_layout.add_widget(Label(size_hint=(1, None), height=30))

        layout.add_widget(main_layout)
        self.add_widget(layout)
        
##########################################################################################

        # Formulaire de saisie
        input_wrapper = BoxLayout(size_hint=(1, None), height=0.15 * Window.height, padding=2)
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

        # Champs de saisie avec size_hint_y pour s'adapter
        self.nom_input = LimitedTextInput(
        hint_text="Nom",
        multiline=False,
        size_hint_y=1
    )
        self.date_input = DateInput(hint_text="Date (jj/mm/aaaa)", multiline=False, size_hint_y=1)
        self.montant_input = TextInput(hint_text="Montant", multiline=False, size_hint_y=1)
        
        inner_layout.add_widget(self.nom_input)
        inner_layout.add_widget(self.date_input)
        inner_layout.add_widget(self.montant_input)
        input_wrapper.add_widget(inner_layout)

        main_layout.add_widget(input_wrapper)
    ##########################################################################################    
                # Catégories
        checkbox_wrapper = BoxLayout(size_hint=(1, None), height=0.06* Window.height, padding=2)
        
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
            size_hint=(0.9, None),  # 90% de la largeur du parent
            height=0.1 * Window.height,
            pos_hint={'center_x': 0.2, 'center_y': 1}
        )
        
        
        # Création des cases
        self.revenu_cbox = CercledCheckbox("Revenu", size_hint_y=1)
        self.charges_fixe_cbox = CercledCheckbox("Charges Fixes", size_hint_y=1)
        self.depense_cbox = CercledCheckbox("Dépense", size_hint_y=1)
        
        self.revenu_cbox.size_hint_x = 0.3
        self.charges_fixe_cbox.size_hint_x = 0.3
        self.depense_cbox.size_hint_x = 0.3
        
        # Ajout dans le conteneur centré
        
      
        checkbox_container.add_widget(Widget(size_hint_x=0.05))  # espace gauche
        checkbox_container.add_widget(self.revenu_cbox)
        checkbox_container.add_widget(self.charges_fixe_cbox)
        checkbox_container.add_widget(self.depense_cbox)
        
        checkbox_container.add_widget(Widget(size_hint_x=0.05))  # espace droite
        
        # Ajout du conteneur dans le fond encadré
        checkbox_wrapper.add_widget(checkbox_container)
        
        main_layout.add_widget(checkbox_wrapper)
        
##########################################################################################
        
                    # BOUTON VALIDER #
        
        self.valider_btn = Button(
            text="Valider",
            size_hint=(1, 0.3),  # prend 15% de la hauteur du parent
            background_color=(0.2, 0.6, 0.86, 1)
        )
        self.valider_btn.bind(on_press=self.ajouter_valeur)
        main_layout.add_widget(self.valider_btn)
        
        main_layout.add_widget(BoxLayout())
        
        
##############################
##############################
##############################      
                        # LABELS #

                # --- ScrollView pour les labels ---
        scroll = ScrollView(size_hint=(1, 0.8))  # prend 80% de la hauteur du parent
        
        # Conteneur vertical à l'intérieur du ScrollView
        labels_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,  # permet de définir height dynamique
            spacing=10,
            padding=10
        )
        labels_container.bind(minimum_height=labels_container.setter('height'))
        
        # --- Création des labels ---
        labels_data = [
            ("Restant à payer : 0.00 €", "total_charges_restantes_label"),
            ("Revenus : 0.00 €", "label_revenus"),
            ("Charges Fixes : 0.00 €", "label_charges"),
            ("Dépenses : 0.00 €", "label_depenses"),
            #("Économie dépense arrondi : 0.00 €", "label_economie")
        ]
        
        for text, attr_name in labels_data:
            label = Label(
                text=text,
                font_size=32,
                size_hint_y=None,
                height=50,  # hauteur fixe pour éviter chevauchement
                halign='center',
                valign='middle',
                color=(0, 0, 0, 1)
            )
            label.bind(size=label.setter('text_size'))  # texte centré
            setattr(self, attr_name, label)
            labels_container.add_widget(label)
        
        # --- Conteneur horizontal pour Solde et Fin de mois ---
        labels_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=80,
            spacing=20
        )
        
        self.solde_label = Label(
            text="Solde actuel : 0.00 €",
            font_size=40,
            size_hint_x=0.5,
            halign='left',
            valign='middle',
            color=(1, 0, 0, 1)
        )
        self.solde_label.bind(size=self.solde_label.setter('text_size'))
        
        self.fin_label = Label(
            text="Fin de mois : 0.00 €",
            font_size=40,
            size_hint_x=0.5,
            halign='right',
            valign='middle',
            color=(1, 0, 0, 1)
        )
        self.fin_label.bind(size=self.fin_label.setter('text_size'))
        
        labels_row.add_widget(self.solde_label)
        labels_row.add_widget(self.fin_label)
        
        labels_container.add_widget(labels_row)
        
        # --- Ajout du conteneur dans le ScrollView ---
        scroll.add_widget(labels_container)
        
        # --- Ajout du ScrollView dans le layout principal ---
        main_layout.add_widget(scroll)
        
        
        
        self.calculer_restant_a_payer()
        
##############################
##############################
##############################            # Création du layout pour la barre de navigation
        bottom_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=100,
            spacing=10
        )
        
        # Liste des boutons principaux avec leurs textes
        buttons_data = [
            ("Charge", "charges_fixe"),
            ("Revenu", "revenus"),
            ("Dépense", "depense"),
            ("Épargne", "epargne")
        ]
        
        # Création des boutons principaux avec texte adaptatif
        buttons = []
        for text, screen_name in buttons_data:
            btn_width = Window.width * 0.2  # 20% de la largeur de l’écran
            btn = Button(
                text=text,
                size_hint=(None, 1),
                width=btn_width
            )
        
            # Centrage du texte dans le bouton
            btn.halign = "center"
            btn.valign = "middle"
            btn.text_size = (btn_width, None)
        
            # Fonction pour adapter la police
            def update_font_size(instance, size, b=btn):
                b.font_size = b.height * 0.4  # 40% de la hauteur du bouton
        
            # On recalcule à chaque redimensionnement
            btn.bind(size=update_font_size)
        
            # Binding pour changer d’écran
            btn.bind(on_press=partial(self.changer_ecran, screen_name))
            buttons.append(btn)
        
        # Bouton config fixe à droite
        self.bouton_page_config = Button(
            background_normal="config.png",
            background_down="config.png",
            size_hint=(None, None),
            size=(100, 100)
        )
        self.bouton_page_config.bind(on_press=partial(self.changer_ecran, "config"))
        # Ajout des widgets pour centrer les boutons principaux
        bottom_layout.add_widget(Widget())  # espace gauche
        for b in buttons:
            bottom_layout.add_widget(b)
        bottom_layout.add_widget(Widget())  # espace entre boutons et config
        bottom_layout.add_widget(self.bouton_page_config)
        
        # Ajout du layout au layout principal
        main_layout.add_widget(bottom_layout)
        main_layout.add_widget(BoxLayout(size_hint_y=1))  # espace flexible au-dessus
         
        self.charger_donnees()
        self.mettre_a_jour_labels()
        self.calculer_restant_a_payer()
        # Appliquer l'état initial des totaux
        self.update_affichage_revenus(app, app.show_total_revenus)
        self.update_affichage_charges(app, app.show_total_charges)
        self.update_affichage_depenses(app, app.show_total_depenses)
        
    def on_pre_enter(self):
        
        self.appliquer_config()
        

# ...
        _, charges_a_payer, total_a_payer = lire_et_calculer_charges_a_payer()
        self.total_charges_restantes_label.text = f"Total des charges restant à payer : {total_a_payer:.2f} €"
            
        self.charger_donnees()        
        self.mettre_a_jour_labels()
        self.mise_a_jour_economie()
        
    def ajouter_valeur(self, instance):
        try:
            montant = float(self.montant_input.text)
            nom = self.nom_input.text.strip()
            
            # On limite la longueur en surveillant le texte
            self.nom_input.bind(text=self.limiter_longueur)
        
        
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
            
            
    def limiter_longueur(self, instance, value):
            max_length = 13  # 🔹 change ici selon ton besoin
            if len(value) > max_length:
                instance.text = value[:max_length]
    
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
        self.total_charges_restantes_label.text = f"restant à payer : {abs(total_restant):.2f} €"
  
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
    
        self.total_charges_restantes_label.text = f"restant à payer : {abs(total_restant):.2f} €"
        
        
    
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
        self.label_revenus.text = f"Revenus : {total_revenus:.2f} €"
        self.label_charges.text = f"Charges Fixes : {abs(total_charges):.2f} €"
        self.label_depenses.text = f"Dépenses : {abs(total_depenses):.2f} €"
        
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
        #self.label_economie.text = f"Économie depense arrondi : {total:.2f} €"
            
    
    def close_app(self, instance):
        App.get_running_app().stop()
        