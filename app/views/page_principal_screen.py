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
        self.data_file = "donnees_budget.json"
        self.soldes = []
        self.total = 0

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Titre
        title_box = BoxLayout(size_hint=(1, None), height=120)
        with title_box.canvas.before:
            Color(1, 0, 0, 1)
            self.title_bg = Rectangle(size=title_box.size, pos=title_box.pos)
        title_box.bind(size=lambda w, s: setattr(self.title_bg, 'size', s),
                       pos=lambda w, p: setattr(self.title_bg, 'pos', p))
        title_label = Label(text="Mon Budget Personnel", font_size=84, bold=True,
                            color=(0.2, 0.6, 0.86, 1), halign='center', valign='middle')
        title_label.bind(size=title_label.setter('text_size'))
        title_box.add_widget(title_label)
        main_layout.add_widget(title_box)

        main_layout.add_widget(Label(size_hint=(1, None), height=30))
        
 # Formulaire de saisie
        input_wrapper = BoxLayout(size_hint=(1, None), height=320, padding=2)
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
        checkbox_wrapper = BoxLayout(size_hint=(1, None), height=100, padding=10, spacing=50)
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
        bottom_layout = BoxLayout(size_hint=(1, None), height=160, spacing=10)
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

        self.add_widget(main_layout)

        self.charger_donnees()
        self.mettre_a_jour_labels()
        # Appliquer l'état initial des totaux
        self.update_affichage_revenus(app, app.show_total_revenus)
        self.update_affichage_charges(app, app.show_total_charges)
        self.update_affichage_depenses(app, app.show_total_depenses)

    def champ(self, hint, height=80):
        return TextInput(hint_text=hint, multiline=False, size_hint=(1, None), height=height)

    def update_affichage_revenus(self, instance, value):
        self.label_revenus.opacity = 1 if value else 0

    def update_affichage_charges(self, instance, value):
        self.label_charges.opacity = 1 if value else 0

    def update_affichage_depenses(self, instance, value):
        self.label_depenses.opacity = 1 if value else 0
        
    def changer_ecran(self, nom_ecran, instance):
        self.manager.current = nom_ecran

    def ajouter_valeur(self, instance):
        try:
            montant = float(self.montant_input.text)
            nom = self.nom_input.text.strip()
            date = self.date_input.text.strip()

            if not nom or not date:
                return  # Ne rien faire si nom ou date vide

            if self.revenu_cbox.active:
                type_valeur = "Revenu"
            elif self.charges_fixe_cbox.active:
                type_valeur = "charges_fixe"
                montant = -montant
            elif self.depense_cbox.active:
                type_valeur = "depense"
                montant = -montant
            else:
                return  # Pas de checkbox sélectionnée

            item = {"nom": nom, "date": date, "montant": montant, "type": type_valeur}
            self.soldes.append(item)

            self.sauvegarder_donnees()
            self.mettre_a_jour_labels()

            # Réinitialisation des champs
            self.nom_input.text = ""
            self.date_input.text = ""
            self.montant_input.text = ""
            self.revenu_cbox.active = False
            self.charges_fixe_cbox.active = False
            self.depense_cbox.active = False

        except ValueError:
            pass

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

    def mettre_a_jour_labels(self):
        total_revenus = sum(item["montant"] for item in self.soldes if item["type"] == "Revenu")
        total_charges = sum(item["montant"] for item in self.soldes if item["type"] == "charges_fixe")
        total_depenses = sum(item["montant"] for item in self.soldes if item["type"] == "depense")

        self.label_revenus.text = f"Total Revenus : {total_revenus:.2f} €"
        self.label_charges.text = f"Total Charges Fixes : {abs(total_charges):.2f} €"
        self.label_depenses.text = f"Total Dépenses : {abs(total_depenses):.2f} €"

        solde = total_revenus + total_charges + total_depenses
        self.solde_label.text = f"Solde : {solde:.2f} €"
