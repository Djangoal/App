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


class ChargesFixesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.charges_a_payer = []

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Titre
        title_label = Label(text="Charges Fixes Enregistrées", font_size=32, size_hint=(1, None), height=60,
                            color=(0, 0, 0, 1), markup=True)
        layout.add_widget(title_label)

        # Tableau des charges fixes
        self.table_layout = GridLayout(cols=4, size_hint_y=None, spacing=5,
                                       row_force_default=True, row_default_height=40)
        self.table_layout.bind(minimum_height=self.table_layout.setter('height'))

        scroll1 = ScrollView(size_hint=(1, 0.4))
        scroll1.add_widget(self.table_layout)
        layout.add_widget(scroll1)

        # Total des charges fixes
        self.total_charges_fixes_label = Label(
            text="Total des charges : 0.00 €",
            size_hint=(1, None),
            height=50,
            font_size=28,
            color=(0, 0.5, 0, 1)
        )
        layout.add_widget(self.total_charges_fixes_label)

        # Titre section à payer
        a_payer_label = Label(text="Charges à Payer", font_size=32, size_hint=(1, None), height=60,
                              color=(0.5, 0, 0, 1), markup=True)
        layout.add_widget(a_payer_label)

        # Tableau des charges à payer
        self.payer_layout = GridLayout(cols=2, size_hint_y=None, spacing=5,
                                       row_force_default=True, row_default_height=40)
        self.payer_layout.bind(minimum_height=self.payer_layout.setter('height'))

        scroll2 = ScrollView(size_hint=(1, 0.4))
        scroll2.add_widget(self.payer_layout)
        layout.add_widget(scroll2)

        # Total des charges à payer
        self.total_Charges_à_Payer_label = Label(
            text="Total des charges restant à payer : 0.00 €",
            size_hint=(1, None),
            height=50,
            font_size=28,
            color=(0, 0.5, 0, 1)
        )
        layout.add_widget(self.total_Charges_à_Payer_label)

        # Boutons
        buttons_layout = BoxLayout(size_hint=(1, None), height=60, spacing=10)
        self.btn_voir_revenus = Button(text="Voir Revenus")
        self.btn_voir_revenus.bind(on_press=lambda x: setattr(self.manager, 'current', 'revenus'))
        buttons_layout.add_widget(self.btn_voir_revenus)

        self.btn_voir_depense = Button(text="Voir Dépense")
        self.btn_voir_depense.bind(on_press=lambda x: setattr(self.manager, 'current', 'depense'))
        buttons_layout.add_widget(self.btn_voir_depense)

        self.btn_retour = Button(text="Retour")
        self.btn_retour.bind(on_press=lambda x: setattr(self.manager, 'current', 'principal'))
        buttons_layout.add_widget(self.btn_retour)

        layout.add_widget(buttons_layout)
        self.add_widget(layout)

    def on_pre_enter(self):
        app = App.get_running_app()
        principal_screen = app.root.get_screen('principal')
        soldes = principal_screen.soldes

        charges_fixes = [item for item in soldes if item['type'] == "charges_fixe"]
        depenses = [item for item in soldes if item['type'] == "depense"]
        noms_depenses = {d['nom'] for d in depenses}

        self.charges_a_payer = [item for item in charges_fixes if item['nom'] not in noms_depenses]

        # TABLEAU COMPLET
        self.table_layout.clear_widgets()
        self.table_layout.add_widget(Label(text="[b]Date[/b]", markup=True, color=(0, 0, 0, 1)))
        self.table_layout.add_widget(Label(text="[b]Nom[/b]", markup=True, color=(0, 0, 0, 1)))
        self.table_layout.add_widget(Label(text="[b]Montant (€)[/b]", markup=True, color=(0, 0, 0, 1)))
        self.table_layout.add_widget(Label(text="[b]Action[/b]", markup=True, color=(0, 0, 0, 1)))

        for index, item in enumerate(charges_fixes):
            self.table_layout.add_widget(Label(text=item['date'], color=(0, 0, 0, 1)))
            self.table_layout.add_widget(Label(text=item['nom'], color=(0, 0, 0, 1)))
            self.table_layout.add_widget(Label(text=f"{item['montant']:.2f} €", color=(0, 0, 0, 1)))

            anchor = AnchorLayout(anchor_x='center', anchor_y='center')
            btn_suppr = Button(text="X", size_hint=(0.5, 1), width=30, background_color=(0.8, 0, 0, 1))
            btn_suppr.bind(on_press=lambda btn, idx=index: self.supprimer_charge(idx))
            anchor.add_widget(btn_suppr)
            self.table_layout.add_widget(anchor)

        # CHARGES À PAYER
        self.payer_layout.clear_widgets()
        self.payer_layout.add_widget(Label(text="[b]Nom[/b]", markup=True, color=(0, 0, 0, 1)))
        self.payer_layout.add_widget(Label(text="[b]Montant (€)[/b]", markup=True, color=(0, 0, 0, 1)))

        for item in self.charges_a_payer:
            self.payer_layout.add_widget(Label(text=item['nom'], color=(0, 0, 0, 1)))
            self.payer_layout.add_widget(Label(text=f"{item['montant']:.2f} €", color=(0, 0, 0, 1)))

        # Totaux
        total_charges = sum(item['montant'] for item in charges_fixes)
        self.total_charges_fixes_label.text = f"Total des charges : {total_charges:.2f} €"

        total_a_payer = sum(item['montant'] for item in self.charges_a_payer)
        self.total_Charges_à_Payer_label.text = f"Total des charges restant à payer : {total_a_payer:.2f} €"

        # 🔁 Sauvegarde du total dans le fichier JSON
        self.sauvegarder_total_charges_a_payer(total_a_payer)

    def sauvegarder_total_charges_a_payer(self, total):
        chemin = "donnees_budget.json"

        # Chargement des données existantes
        if os.path.exists(chemin):
            with open(chemin, 'r', encoding='utf-8') as f:
                donnees = json.load(f)
        else:
            donnees = {}

        # Mise à jour de la clé "total_charges_a_payer"
        donnees["total_charges_a_payer"] = total

        # Sauvegarde dans le fichier
        with open(chemin, 'w', encoding='utf-8') as f:
            json.dump(donnees, f, indent=4, ensure_ascii=False)

    def supprimer_charge(self, index):
        app = App.get_running_app()
        principal_screen = app.root.get_screen('principal')
        soldes = principal_screen.soldes
        charges_fixes = [item for item in soldes if item['type'] == "charges_fixe"]

        if 0 <= index < len(charges_fixes):
            item_to_remove = charges_fixes[index]
            if item_to_remove in soldes:
                soldes.remove(item_to_remove)
                principal_screen.sauvegarder_donnees()
                self.on_pre_enter()