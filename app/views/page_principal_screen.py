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
from kivmob import KivMob
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.utils import platform

# Import de KivMob uniquement si on est sur Android
if platform == "android":
    from kivmob import KivMob

class PagePrincipale(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Exemple d'un bouton pour afficher une pub interstitielle
        bouton_pub = Button(
            text="Voir une pub",
            size_hint=(0.4, 0.1),
            pos_hint={"center_x": 0.5, "y": 0.1}
        )
        bouton_pub.bind(on_release=self.afficher_interstitielle)
        self.add_widget(bouton_pub)

        # Activation de la pub uniquement sur Android
        if platform == "android":
            # ⚠️ Utilise ton APP ID ici quand tu l'auras (actuellement test)
            self.ads = KivMob("ca-app-pub-3940256099942544~3347511713")

            # Bannière - avec ton Unit ID
            self.ads.new_banner("ca-app-pub-6034346911104431/2475013658", top_pos=False)
            self.ads.request_banner()
            self.ads.show_banner()

            # Interstitielle (test)
            self.ads.new_interstitial("ca-app-pub-3940256099942544/1033173712")
            self.ads.request_interstitial()
        else:
            self.ads = None

    def afficher_interstitielle(self, *args):
        if self.ads and self.ads.is_interstitial_loaded():
            self.ads.show_interstitial()
        else:
            print("Pub interstitielle non prête ou non disponible.")
        
    
    def on_pre_enter(self):
        self.appliquer_config()
        
        # Afficher la pub interstitielle si prête
        app = App.get_running_app()
        if hasattr(app, "ads") and app.ads.is_interstitial_loaded():
            app.ads.show_interstitial()
            Clock.schedule_once(lambda dt: app.ads.load_interstitial(), 2)  # recharge après 2 sec
    
        # Mise à jour de l'écran
        _, charges_a_payer, total_a_payer = lire_et_calculer_charges_a_payer()
        self.total_charges_restantes_label.text = f"Total des charges restant à payer : {total_a_payer:.2f} €"
        self.charger_donnees()
        self.mettre_a_jour_labels()
        self.mise_a_jour_economie()
        
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
        self.total_charges_restantes_label.text = f"total charges à payer : {abs(total_restant):.2f} €"
  
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
        self.label_economie.text = f"Économie depense arrondi : {total:.2f} €"
            
    
    def close_app(self, instance):
        App.get_running_app().stop()
        