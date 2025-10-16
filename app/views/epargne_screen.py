from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
import json
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.metrics import dp



class EpargneScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.index_en_modification = None
        self.mode_modification = False
        # proportions réduites
        title_font = Window.height * 0.035
        row_height = Window.height * 0.06
        button_height = Window.height * 0.06
        small_font = Window.height * 0.022

##########################################################################################

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Titre
        titre = Label(
            text="Épargne",
            font_size=title_font,
            size_hint=(1, None),
            height=Window.height * 0.08,
            bold=True,
            color=(0, 0, 0, 1)
        )
        self.layout.add_widget(titre)

        # --- Premier formulaire ---

        scrollview = ScrollView(
            size_hint=(1, None),
            height=Window.height * 0.12
        )
        
        contenu_formulaire = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=dp(8),
            padding=dp(8)
        )
        contenu_formulaire.bind(minimum_height=contenu_formulaire.setter('height'))
        
        # Wrapper avec bordure
        input_wrapper = BoxLayout(
            size_hint=(1, None),
            height=Window.height * 0.1,
            padding=dp(2)
        )
        with input_wrapper.canvas.before:
            Color(0, 0, 0, 1)
            self.border_rect = Rectangle()
        
        def update_border_rect(*args):
            self.border_rect.size = input_wrapper.size
            self.border_rect.pos = input_wrapper.pos
        
        input_wrapper.bind(size=update_border_rect, pos=update_border_rect)
        
        # Layout interne (fond gris clair)
        inner_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(4),
            padding=dp(4)
        )
        with inner_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.bg_rect = Rectangle()
        
        def update_bg_rect(*args):
            self.bg_rect.size = inner_layout.size
            self.bg_rect.pos = inner_layout.pos
        
        inner_layout.bind(size=update_bg_rect, pos=update_bg_rect)
        
        # Champs du formulaire principal
        self.nom_input = self.creer_champ(inner_layout, "Nom", Window.height * 0.04)
        self.montant_input = self.creer_champ(inner_layout, "Montant", Window.height * 0.04)
        
        input_wrapper.add_widget(inner_layout)
        contenu_formulaire.add_widget(input_wrapper)
        scrollview.add_widget(contenu_formulaire)
        self.layout.add_widget(scrollview)
        
        # Bouton de validation principal
        self.valider_btn = Button(
            text="Valider",
            size_hint=(1, None),
            height=Window.height * 0.05,
            background_color=(0.2, 0.6, 0.86, 1)
        )
        self.valider_btn.bind(on_press=self.valider_action0)
        self.layout.add_widget(self.valider_btn)
        

        # --- Deuxième formulaire : montant livret ---

        scrollview2 = ScrollView(
            size_hint=(1, None),
            height=Window.height * 0.1
        )
        
        contenu2 = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=dp(4),
            padding=dp(4)
        )
        contenu2.bind(minimum_height=contenu2.setter('height'))
        
        # Wrapper avec bordure
        input_wrapper2 = BoxLayout(
            size_hint=(1, None),
            height=Window.height * 0.06,
            padding=dp(2)
        )
        with input_wrapper2.canvas.before:
            Color(0, 0, 0, 1)
            self.border_rect2 = Rectangle()
        
        def update_border_rect2(*args):
            self.border_rect2.size = input_wrapper2.size
            self.border_rect2.pos = input_wrapper2.pos
        
        input_wrapper2.bind(size=update_border_rect2, pos=update_border_rect2)
        
        # Layout interne (fond gris clair)
        inner_layout2 = BoxLayout(
            orientation='vertical',
            spacing=dp(4),
            padding=dp(4)
        )
        with inner_layout2.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.bg_rect2 = Rectangle()
        
        def update_bg_rect2(*args):
            self.bg_rect2.size = inner_layout2.size
            self.bg_rect2.pos = inner_layout2.pos
        
        inner_layout2.bind(size=update_bg_rect2, pos=update_bg_rect2)
        
        # Champs du formulaire
        self.livret_input = self.creer_champ(inner_layout2, "solde livret", Window.height * 0.04)
        
        # Label solde livret
        self.solde_livret_label = Label(
            text="Solde Livret : 0.00 €",
            size_hint=(1, None),
            height=Window.height * 0.03,
            font_size=Window.height * 0.02,
            color=(0, 0, 0, 1)
        )
        self.layout.add_widget(self.solde_livret_label)
        
        # Bouton valider montant livret
        valider_livret_btn = Button(
            text="Valider solde livret",
            size_hint=(1, None),
            height=Window.height * 0.04,
            background_color=(0.2, 0.6, 0.86, 1)
        )
        valider_livret_btn.bind(on_press=self.valider_action)
        
        input_wrapper2.add_widget(inner_layout2)
        contenu2.add_widget(input_wrapper2)
        scrollview2.add_widget(contenu2)
        self.layout.add_widget(scrollview2)
        self.layout.add_widget(valider_livret_btn)
        self.layout.add_widget(Widget())
##############################
############################## ############################## 
      # --- Affichage des épargnes ---
        # Bouton toggle épargnes
        self.btn_toggle = Button(
            text='Afficher les Épargnes',
            size_hint_y=None,
            height=Window.height * 0.03,
            font_size=Window.height * 0.025
        )
        self.btn_toggle.bind(on_release=self.toggle_epargnes)
        self.layout.add_widget(self.btn_toggle)
        
        # Conteneur du tableau
        self.table_container = ScrollView(
            size_hint=(1, None),
            height=0  # Masqué par défaut
        )
        self.table_layout = GridLayout(
            cols=4,
            size_hint_y=None,
            spacing=dp(5),
            row_default_height=Window.height * 0.02,
            row_force_default=True
        )
        self.table_layout.bind(minimum_height=self.table_layout.setter('height'))
        self.table_container.add_widget(self.table_layout)
        self.layout.add_widget(self.table_container)
        
        # Label total épargne
        self.total_label = Label(
            text="Total épargne : 0.00 €",
            size_hint=(1, None),
            height=Window.height * 0.03,
            font_size=Window.height * 0.02,
            color=(0, 0, 0, 1)
        )
        self.layout.add_widget(self.total_label)
        
        # Label différence non allouée
        self.diff_label = Label(
            text="Non alloué : 0.00 €",
            size_hint=(1, None),
            height=Window.height * 0.03,
            font_size=Window.height * 0.02,
            color=(0, 0, 0, 1)
        )
        self.layout.add_widget(self.diff_label)
############################## ############################## ##############################  

        # Bouton retour
        # Layout des boutons
        buttons_layout = BoxLayout(
            size_hint=(1, None),
            height=Window.height * 0.035,  # proportionnel à la hauteur de l'écran
            spacing=dp(10)
        )
        
        # Bouton retour
        self.btn_retour = Button(
            text="Retour",
            font_size=Window.height * 0.03  # taille du texte proportionnelle
        )
        self.btn_retour.bind(on_press=lambda x: setattr(self.manager, 'current', 'principal'))
        buttons_layout.add_widget(self.btn_retour)
        
        self.layout.add_widget(buttons_layout)
        self.add_widget(self.layout)
        
        # État d'affichage des épargnes
        self.epargnes_visible = False
##############################
##############################
##############################    
    def creer_champ(self, parent, hint_text, height):
        champ_wrapper = BoxLayout(size_hint=(1, None), height=height, padding=[5, 5])
        with champ_wrapper.canvas.before:
            Color(1, 1, 1, 1)
            rect = Rectangle(size=champ_wrapper.size, pos=champ_wrapper.pos)
            champ_wrapper.bind(size=lambda instance, value: setattr(rect, 'size', value),
                               pos=lambda instance, value: setattr(rect, 'pos', value))
        champ_input = TextInput(
            hint_text=hint_text,
            multiline=False,
            background_color=(0, 0, 0, 0),
            foreground_color=(0, 0, 0, 1),
            padding=[10, 10]
        )
        champ_wrapper.add_widget(champ_input)
        parent.add_widget(champ_wrapper)
        return champ_input
##############################
##############################
##############################
    def toggle_epargnes(self, *args):
        self.epargnes_visible = not self.epargnes_visible
        self.btn_toggle.text = 'Masquer les Épargnes' if self.epargnes_visible else 'Afficher les Épargnes'
        if self.epargnes_visible:
            Clock.schedule_once(self.ajuster_hauteur_tableau, 0.1)
        else:
            self.table_container.height = 1
##############################
##############################
##############################
    def ajuster_hauteur_tableau(self, *args):
        self.table_container.height = min(self.table_layout.height, 600)
##############################
##############################
##############################        
    def charger_solde_livret(self):
        chemin = "donnees_budget.json"
        try:
            with open(chemin, "r", encoding="utf-8") as f:
                donnees = json.load(f)
                solde = donnees.get("solde_livret", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            solde = 0
    
        self.solde_livret_label.text = f"Solde Livret : {solde:.2f} €"
##############################
##############################
##############################
    def on_pre_enter(self):
        
        self.charger_epargnes()
        self.charger_solde_livret()
        self.mettre_a_jour_non_alloue()
##############################
##############################
##############################

    def charger_epargnes(self):
        chemin = "donnees_budget.json"
        try:
            with open(chemin, "r", encoding="utf-8") as f:
                donnees = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            donnees = {}
    
        epargnes = donnees.get("epargne", [])
        self.table_layout.clear_widgets()
    
        header_font = dp(16)
        row_font = dp(14)
    
        # --- En-têtes du tableau (mêmes colonnes que ton fichier) ---
        self.table_layout.add_widget(Label(
            text="[b]Nom[/b]", markup=True, color=(0, 0, 0, 1),
            font_size=header_font, size_hint_x=0.35
        ))
        self.table_layout.add_widget(Label(
            text="[b]Montant[/b]", markup=True, color=(0, 0, 0, 1),
            font_size=header_font, size_hint_x=0.35
        ))
        self.table_layout.add_widget(Label(
            text="", color=(0, 0, 0, 1),
            font_size=header_font, size_hint_x=0.15
        ))
        self.table_layout.add_widget(Label(
            text="", color=(0, 0, 0, 1),
            font_size=header_font, size_hint_x=0.15
        ))
    
        # --- Lignes du tableau ---
        total = 0
        for index, item in enumerate(epargnes):
            # Colonne Nom
            self.table_layout.add_widget(Label(
                text=item['nom'], color=(0, 0, 0, 1),
                font_size=row_font, size_hint_x=0.35
            ))
            # Colonne Montant
            self.table_layout.add_widget(Label(
                text=f"{item['montant']:.2f} €", color=(0, 0, 0, 1),
                font_size=row_font, size_hint_x=0.35
            ))
    
            # Bouton Modifier
            btn_modifier = Button(
                text="Modifier",
                background_color=(0.8, 0.8, 0.2, 1),
                font_size=row_font,
                size_hint_x=0.2
            )
            btn_modifier.bind(on_press=lambda btn, idx=index: self.remplir_formulaire_modification(idx))
            self.table_layout.add_widget(btn_modifier)
    
            # Bouton Supprimer
            btn_supprimer = Button(
                text="X",
                background_color=(1, 0.4, 0.4, 1),
                font_size=row_font,
                size_hint_x=0.1
            )
            btn_supprimer.bind(on_press=lambda btn, idx=index: self.afficher_confirmation_suppression(idx))
            self.table_layout.add_widget(btn_supprimer)
    
            total += item['montant']
    
        # Mise à jour du total
        self.total_label.text = f"Total épargne : {total:.2f} €"
        self.mettre_a_jour_non_alloue()
        
##############################
##############################
##############################        
    def remplir_formulaire_modification(self, index):
        chemin = "donnees_budget.json"
        try:
            with open(chemin, "r", encoding="utf-8") as f:
                donnees = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return

        epargnes = donnees.get("epargne", [])
        if 0 <= index < len(epargnes):
            item = epargnes[index]
            self.nom_input.text = item["nom"]
            self.montant_input.text = str(item["montant"])
            self.index_en_modification = index
            self.mode_modification = True
            self.valider_btn.text = "Modifier"
            self.mettre_a_jour_non_alloue()
##############################
##############################
##############################            
    
    def valider_action(self, instance):
        if self.mode_modification:
            self.enregistrer_modification()
        else:
            self.ajouter_valeur()
            self.mettre_a_jour_non_alloue()
##############################
##############################
##############################            
    def valider_action0(self, instance):
        if self.mode_modification:
            self.enregistrer_modification()
        else:
            self.ajouter_valeur()
            self.mettre_a_jour_non_alloue()
##############################
##############################
##############################            
    def enregistrer_modification(self):
        nom = self.nom_input.text.strip()
        montant_text = self.montant_input.text.strip()
        if not nom or not montant_text:
            return

        try:
            montant = float(montant_text)
        except ValueError:
            return

        chemin = "donnees_budget.json"
        try:
            with open(chemin, "r", encoding="utf-8") as f:
                donnees = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return

        if "epargne" in donnees and 0 <= self.index_en_modification < len(donnees["epargne"]):
            donnees["epargne"][self.index_en_modification] = {
                "nom": nom,
                "montant": montant
            }
            with open(chemin, "w", encoding="utf-8") as f:
                json.dump(donnees, f, indent=4, ensure_ascii=False)

        self.nom_input.text = ""
        self.montant_input.text = ""
        self.valider_btn.text = "Valider"
        self.mode_modification = False
        self.charger_epargnes()
        self.mettre_a_jour_non_alloue()
##############################
##############################
##############################        
    def supprimer_epargne(self, index):
        chemin = "donnees_budget.json"
        try:
            with open(chemin, "r", encoding="utf-8") as f:
                donnees = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return

        if "epargne" in donnees and 0 <= index < len(donnees["epargne"]):
            del donnees["epargne"][index]
            with open(chemin, "w", encoding="utf-8") as f:
                json.dump(donnees, f, indent=4, ensure_ascii=False)

        self.charger_epargnes()
        self.mettre_a_jour_non_alloue()
##############################
##############################
##############################    
    def mettre_a_jour_non_alloue(self):
        try:
            with open("donnees_budget.json", "r", encoding="utf-8") as f:
                donnees = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            donnees = {}
    
        epargnes = donnees.get("epargne", [])
        solde_livret = donnees.get("solde_livret", 0)
        total = sum(e['montant'] for e in epargnes)
        non_alloue = solde_livret - total
        self.diff_label.text = f"Non alloué : {non_alloue:.2f} €"
##############################
##############################
##############################            
    def calculer_total_livret(self):
            chemin = "donnees_budget.json"
            total = 0
            try:
                with open(chemin, "r", encoding="utf-8") as f:
                    donnees = json.load(f)
                    livret_data = donnees.get("epargne", [])  # Ou autre clé si tu utilises un autre nom
                    for item in livret_data:
                        total += float(item.get("montant", 0))
            except (FileNotFoundError, json.JSONDecodeError):
                pass
            return total
##############################
##############################
##############################

    def ajouter_valeur(self):
        chemin = "donnees_budget.json"
        try:
            with open(chemin, "r", encoding="utf-8") as f:
                donnees = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            donnees = {}
    
        livret_text = self.livret_input.text.strip() if hasattr(self, "livret_input") else ""
        nom = self.nom_input.text.strip() if hasattr(self, "nom_input") else ""
        montant_text = self.montant_input.text.strip() if hasattr(self, "montant_input") else ""
    
        modifie = False
    
        # Cas 1 : mise à jour du solde livret
        if livret_text:
            try:
                montant = float(livret_text)
            except ValueError:
                return  # Tu peux ajouter une alerte ici
            donnees["solde_livret"] = montant
            self.livret_input.text = ""
            modifie = True
    
        # Cas 2 : ajout d'une entrée dans épargne
        elif nom and montant_text:
            try:
                montant = float(montant_text)
            except ValueError:
                return
            nouvelle_entree = {
                "nom": nom,
                "montant": montant
            }
            donnees.setdefault("epargne", []).append(nouvelle_entree)
            self.nom_input.text = ""
            self.montant_input.text = ""
            modifie = True
    
        # Sauvegarde des données seulement si elles ont été modifiées
        if modifie:
            with open(chemin, "w", encoding="utf-8") as f:
                json.dump(donnees, f, ensure_ascii=False, indent=2)
    
            # Mise à jour des affichages après la sauvegarde
            if livret_text:
                self.charger_solde_livret()
            if nom and montant_text:
                if not self.epargnes_visible:
                    self.toggle_epargnes()
                else:
                    self.ajuster_hauteur_tableau()
                self.charger_epargnes()
                self.mettre_a_jour_non_alloue()
    
            # Facultatif : recharge les totaux globaux si nécessaire
            if hasattr(self, "charger_totaux"):
                self.charger_totaux()
                self.mettre_a_jour_non_alloue()
##############################
##############################
##############################                
    def afficher_confirmation_suppression(self, index):
        # Layout principal du popup
        layout = BoxLayout(
            orientation='vertical',
            padding=Window.height * 0.02,
            spacing=Window.height * 0.02
        )
    
        # Message
        message = Label(
            text="Confirmer la suppression de cette épargne ?",
            size_hint=(1, None),
            height=Window.height * 0.08,
            halign="center",
            valign="middle",
            font_size=Window.height * 0.025
        )
        message.bind(size=message.setter('text_size'))
        layout.add_widget(message)
        layout.add_widget(Widget())  # pousse les boutons vers le bas
    
        # Layout pour les boutons
        boutons = BoxLayout(
            size_hint=(1, None),
            height=Window.height * 0.08,
            spacing=Window.width * 0.02
        )
    
        # Boutons frais, jamais ajoutés ailleurs
        btn_annuler = Button(text="Annuler", font_size=Window.height * 0.025)
        btn_confirmer = Button(text="Confirmer", background_color=(1, 0, 0, 1), font_size=Window.height * 0.025)
    
        boutons.add_widget(btn_annuler)
        boutons.add_widget(btn_confirmer)
        layout.add_widget(boutons)
    
        # Création du popup
        popup = Popup(
            title="Confirmation",
            content=layout,
            size_hint=(0.8, 0.3),
            auto_dismiss=False
        )
    
        # Actions des boutons
        btn_annuler.bind(on_press=popup.dismiss)
    
        def confirmer_action(instance):
            popup.dismiss()
            self.supprimer_epargne(index)
            self.on_pre_enter()  # recharge la liste des épargnes
    
        btn_confirmer.bind(on_press=confirmer_action)
    
        popup.open()
##############################
##############################
##############################
            
    def retour_page_precedente(self, instance):
        self.manager.current = "page_principale"