import json
import os
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen

class pageprincipal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.donnees = []

        # Flags pour afficher ou non les totaux (tu peux lier ça à ta page config)
        self.afficher_revenus = True
        self.afficher_charges = True
        self.afficher_depenses = True

        layout_principal = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Titre
        titre = Label(text="Gestion Budget Personnel", font_size=24, size_hint=(1, 0.1))
        layout_principal.add_widget(titre)

        # Formulaire saisie
        formulaire = GridLayout(cols=2, size_hint=(1, 0.15), spacing=10)

        formulaire.add_widget(Label(text="Nom :"))
        self.nom_input = TextInput(multiline=False)
        formulaire.add_widget(self.nom_input)

        formulaire.add_widget(Label(text="Montant :"))
        self.montant_input = TextInput(multiline=False, input_filter='float')
        formulaire.add_widget(self.montant_input)

        # Choix catégorie via checkbox
        formulaire.add_widget(Label(text="Revenu"))
        self.revenu_checkbox = CheckBox(group='categorie')
        formulaire.add_widget(self.revenu_checkbox)

        formulaire.add_widget(Label(text="Charges Fixes"))
        self.charge_checkbox = CheckBox(group='categorie')
        formulaire.add_widget(self.charge_checkbox)

        formulaire.add_widget(Label(text="Dépense"))
        self.depense_checkbox = CheckBox(group='categorie')
        formulaire.add_widget(self.depense_checkbox)

        layout_principal.add_widget(formulaire)

        # Bouton Valider
        bouton_valider = Button(text="Valider", size_hint=(1, 0.1))
        bouton_valider.bind(on_press=self.ajouter_valeur)
        layout_principal.add_widget(bouton_valider)

        # Totaux
        self.total_revenu_label = Label(text="", size_hint=(1, 0.05))
        self.total_charges_label = Label(text="", size_hint=(1, 0.05))
        self.total_depenses_label = Label(text="", size_hint=(1, 0.05))
        self.solde_label = Label(text="", font_size=20, size_hint=(1, 0.1))

        layout_principal.add_widget(self.total_revenu_label)
        layout_principal.add_widget(self.total_charges_label)
        layout_principal.add_widget(self.total_depenses_label)
        layout_principal.add_widget(self.solde_label)

        # ScrollView pour liste des données
        self.scrollview = ScrollView(size_hint=(1, 0.4))
        self.grid_donnees = GridLayout(cols=4, spacing=10, size_hint_y=None)
        self.grid_donnees.bind(minimum_height=self.grid_donnees.setter('height'))

        # Entêtes colonnes
        self.grid_donnees.add_widget(Label(text="Date", bold=True))
        self.grid_donnees.add_widget(Label(text="Nom", bold=True))
        self.grid_donnees.add_widget(Label(text="Montant", bold=True))
        self.grid_donnees.add_widget(Label(text="Catégorie", bold=True))

        self.scrollview.add_widget(self.grid_donnees)
        layout_principal.add_widget(self.scrollview)

        self.add_widget(layout_principal)

        self.charger_donnees()
        self.afficher_totaux()
        self.afficher_donnees()

    def ajouter_valeur(self, instance):
        nom = self.nom_input.text.strip()
        montant_text = self.montant_input.text.strip()
        if not nom or not montant_text:
            return

        try:
            montant = float(montant_text)
        except ValueError:
            return

        if self.revenu_checkbox.active:
            categorie = 'revenu'
        elif self.charge_checkbox.active:
            categorie = 'charges_fixe'
        elif self.depense_checkbox.active:
            categorie = 'depense'
        else:
            return

        nouvelle_entree = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'nom': nom,
            'montant': montant,
            'categorie': categorie
        }

        self.donnees.append(nouvelle_entree)
        self.sauvegarder_donnees()
        self.afficher_totaux()
        self.afficher_donnees()

        self.nom_input.text = ''
        self.montant_input.text = ''
        self.revenu_checkbox.active = False
        self.charge_checkbox.active = False
        self.depense_checkbox.active = False

    def sauvegarder_donnees(self):
        with open('donnees_budget.json', 'w', encoding='utf-8') as f:
            json.dump(self.donnees, f, ensure_ascii=False, indent=4)

    def charger_donnees(self):
        if os.path.exists('donnees_budget.json'):
            with open('donnees_budget.json', 'r', encoding='utf-8') as f:
                self.donnees = json.load(f)

    def afficher_totaux(self):
        total_revenu = sum(item['montant'] for item in self.donnees if item['categorie'] == 'revenu')
        total_charges = sum(item['montant'] for item in self.donnees if item['categorie'] == 'charges_fixe')
        total_depenses = sum(item['montant'] for item in self.donnees if item['categorie'] == 'depense')
        solde = total_revenu - total_charges - total_depenses

        self.total_revenu_label.text = f"Total Revenus : {total_revenu:.2f} €" if self.afficher_revenus else ""
        self.total_charges_label.text = f"Total Charges Fixes : {total_charges:.2f} €" if self.afficher_charges else ""
        self.total_depenses_label.text = f"Total Dépenses : {total_depenses:.2f} €" if self.afficher_depenses else ""
        self.solde_label.text = f"Solde : {solde:.2f} €"

    def afficher_donnees(self):
        # Supprime toutes les données affichées sauf la ligne d'entêtes (les 4 premiers widgets)
        self.grid_donnees.clear_widgets()
        self.grid_donnees.add_widget(Label(text="Date", bold=True))
        self.grid_donnees.add_widget(Label(text="Nom", bold=True))
        self.grid_donnees.add_widget(Label(text="Montant", bold=True))
        self.grid_donnees.add_widget(Label(text="Catégorie", bold=True))

        for item in self.donnees:
            self.grid_donnees.add_widget(Label(text=item['date']))
            self.grid_donnees.add_widget(Label(text=item['nom']))
            self.grid_donnees.add_widget(Label(text=f"{item['montant']:.2f} €"))
            self.grid_donnees.add_widget(Label(text=item['categorie']))

class BudgetApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(PagePrincipale(name='page_principale'))
        return sm

if __name__ == '__main__':
    BudgetApp().run()