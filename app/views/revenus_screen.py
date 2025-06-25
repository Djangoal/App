from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from functools import partial


class RevenusScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        title_label = Label(text="Liste des Revenus", font_size=48, size_hint=(1, None), height=100, bold=True,
                            color=(0, 0, 0, 1))
        layout.add_widget(title_label)

        self.table_layout = GridLayout(cols=4, size_hint_y=None, spacing=5,
                                       row_force_default=True, row_default_height=40)
        self.table_layout.bind(minimum_height=self.table_layout.setter('height'))

        self.scroll = ScrollView()
        self.scroll.add_widget(self.table_layout)
        layout.add_widget(self.scroll)

        # Label fixe pour afficher le total des revenus
        self.total_revenus_label = Label(
            text="Total des revenus : 0.00 €",
            size_hint=(1, None),
            height=50,
            font_size=48,
            color=(0, 0.5, 0, 1)
        )
        layout.add_widget(self.total_revenus_label)

        buttons_layout = BoxLayout(size_hint=(1, None), height=60, spacing=10)

        self.btn_voir_charges_fixe = Button(text="Voir charges fixe")
        self.btn_voir_charges_fixe.bind(on_press=lambda x: setattr(self.manager, 'current', 'charges_fixe'))
        buttons_layout.add_widget(self.btn_voir_charges_fixe)

        self.btn_voir_depense = Button(text="Voir depense")
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

        self.table_layout.clear_widgets()
        self.table_layout.add_widget(Label(text="Date", bold=True, color=(0, 0, 0, 1)))
        self.table_layout.add_widget(Label(text="Nom", bold=True, color=(0, 0, 0, 1)))
        self.table_layout.add_widget(Label(text="Montant (€)", bold=True, color=(0, 0, 0, 1)))
        self.table_layout.add_widget(Label(text="Action", bold=True, color=(0, 0, 0, 1)))

        revenus = [item for item in soldes if item['type'].lower() == "revenu"]

        for index, item in enumerate(revenus):
            self.table_layout.add_widget(Label(text=item['date'], color=(0, 0, 0, 1)))
            self.table_layout.add_widget(Label(text=item['nom'], color=(0, 0, 0, 1)))
            self.table_layout.add_widget(Label(text=f"{item['montant']:.2f} €", color=(0, 0, 0, 1)))

            container = BoxLayout(orientation='horizontal', size_hint_x=1)
            container.add_widget(Widget(size_hint_x=1))  # espace vide à gauche
            btn_suppr = Button(text="X", size_hint=(None, 1), width=50, background_color=(1, 0, 0, 1))
            btn_suppr.bind(on_press=partial(self.supprimer_revenu, index))
            container.add_widget(btn_suppr)
            container.add_widget(Widget(size_hint_x=1))  # espace vide à droite
            self.table_layout.add_widget(container)

        total_revenus = sum(item['montant'] for item in revenus)
        self.total_revenus_label.text = f"Total des revenus : {total_revenus:.2f} €"

    def supprimer_revenu(self, index, *args):
        import json
        app = App.get_running_app()
        principal_screen = app.root.get_screen('principal')
        soldes = principal_screen.soldes
        revenus = [item for item in soldes if item['type'].lower() == "revenu"]

        if 0 <= index < len(revenus):
            item_to_remove = revenus[index]

            if item_to_remove in soldes:
                soldes.remove(item_to_remove)

                # Mise à jour du fichier JSON (chargement, modification, sauvegarde)
                try:
                    with open('donnees_budget.json', 'r', encoding='utf-8') as f:
                        donnees = json.load(f)
                except FileNotFoundError:
                    donnees = {}

                # Si nécessaire, faire une mise à jour similaire à celle des dépenses (par exemple dans 'a_payer' ou autre)
                # Ici pas d'ajout dans 'a_payer' par défaut (à adapter selon ton besoin)

                with open('donnees_budget.json', 'w', encoding='utf-8') as f:
                    json.dump(donnees, f, ensure_ascii=False, indent=4)

                # Sauvegarde dans l'app
                principal_screen.sauvegarder_donnees()
                principal_screen.charger_donnees()
                principal_screen.mettre_a_jour_labels()
                charges_fixe_screen = app.root.get_screen('charges_fixe')
                charges_fixe_screen.on_pre_enter()

                # Recharge l'affichage
                self.on_pre_enter()