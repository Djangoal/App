from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from components.entry_row import EntryRow
from controllers.budget_controller import BudgetController

class ChargesFixesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        title_label = Label(text="Liste des charges fixes", font_size=48, size_hint=(1, None), height=100, bold=True,
                            color=(0, 0, 0, 1))
        layout.add_widget(title_label)

        self.table_layout = GridLayout(cols=4, size_hint_y=None, spacing=5,
                                       row_force_default=True, row_default_height=40)
        self.table_layout.bind(minimum_height=self.table_layout.setter('height'))

        self.scroll = ScrollView()
        self.scroll.add_widget(self.table_layout)
        layout.add_widget(self.scroll)

        self.total_charges_fixes_label = Label(
            text="Total des charges : 0.00 €",
            size_hint=(1, None),
            height=50,
            font_size=48,
            color=(0, 0.5, 0, 1)
        )
        layout.add_widget(self.total_charges_fixes_label)

        buttons_layout = BoxLayout(size_hint=(1, None), height=60, spacing=10)

        self.btn_voir_revenus = Button(text="Voir Revenus")
        self.btn_voir_revenus.bind(on_press=lambda x: setattr(self.manager, 'current', 'revenus'))
        buttons_layout.add_widget(self.btn_voir_revenus)

        self.btn_voir_depense = Button(text="Voir Depense")
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

        charges_fixes = [item for item in soldes if item['type'] == "charges_fixe"]

        for index, item in enumerate(charges_fixes):
            self.table_layout.add_widget(Label(text=item['date'], color=(0, 0, 0, 1)))
            self.table_layout.add_widget(Label(text=item['nom'], color=(0, 0, 0, 1)))
            self.table_layout.add_widget(Label(text=f"{item['montant']:.2f} €", color=(0, 0, 0, 1)))

            container = BoxLayout(orientation='horizontal', size_hint_x=1)
            container.add_widget(Widget(size_hint_x=1))  # espace vide à gauche
            btn_suppr = Button(text="Supprimer", size_hint=(None, 1), width=210, background_color=(1, 0, 0, 1))
            btn_suppr.bind(on_press=lambda btn, idx=index: self.supprimer_charge_fixe(idx))
            container.add_widget(btn_suppr)
            container.add_widget(Widget(size_hint_x=1))  # espace vide à droite
            self.table_layout.add_widget(container)

        total_charges = sum(item['montant'] for item in charges_fixes)
        self.total_charges_fixes_label.text = f"Total des charges : {total_charges:.2f} €"

    def supprimer_charge_fixe(self, index):
        app = App.get_running_app()
        principal_screen = app.root.get_screen('principal')
        charges_fixes = [item for item in principal_screen.soldes if item['type'] == "charges_fixe"]

        if 0 <= index < len(charges_fixes):
            item_to_remove = charges_fixes[index]
            principal_screen.soldes.remove(item_to_remove)
            principal_screen.total -= item_to_remove['montant']
            principal_screen.solde_label.text = f"Solde: {principal_screen.total:.2f} €"
            principal_screen.sauvegarder_donnees()
            self.on_pre_enter()

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

        self.total_revenus_label = Label(text="Total des revenus : 0.00 €",
                                         size_hint=(1, None),
                                         height=50,
                                         font_size=48,
                                         color=(0, 0.5, 0, 1))
        layout.add_widget(self.total_revenus_label)

        buttons_layout = BoxLayout(size_hint=(1, None), height=60, spacing=10)

        self.btn_voir_charges_fixes = Button(text="Voir Charges Fixes")
        self.btn_voir_charges_fixes.bind(on_press=lambda x: setattr(self.manager, 'current', 'charges_fixe'))
        buttons_layout.add_widget(self.btn_voir_charges_fixes)

        self.btn_voir_depense = Button(text="Voir Depense")
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

        revenus = [item for item in soldes if item['type'] == "revenu"]

        for index, item in enumerate(revenus):
            self.table_layout.add_widget(Label(text=item['date'], color=(0, 0, 0, 1)))
            self.table_layout.add_widget(Label(text=item['nom'], color=(0, 0, 0, 1)))
            self.table_layout.add_widget(Label(text=f"{item['montant']:.2f} €", color=(0, 0, 0, 1)))

            container = BoxLayout(orientation='horizontal', size_hint_x=1)
            container.add_widget(Widget(size_hint_x=1))  # espace vide à gauche
            btn_suppr = Button(text="Supprimer", size_hint=(None, 1), width=210, background_color=(1, 0, 0, 1))
            btn_suppr.bind(on_press=lambda btn, idx=index: self.supprimer_revenu(idx))
            container.add_widget(btn_suppr)
            container.add_widget(Widget(size_hint_x=1))  # espace vide à droite
            self.table_layout.add_widget(container)

        total_revenus = sum(item["montant"] for item in revenus)
        self.total_revenus_label.text = f"Total des revenus : {total_revenus:.2f} €"

    def supprimer_revenu(self, index):
        app = App.get_running_app()
        principal_screen = app.root.get_screen('principal')
        revenus = [item for item in principal_screen.soldes if item['type'] == "revenu"]

        if 0 <= index < len(revenus):
            item_to_remove = revenus[index]
            principal_screen.soldes.remove(item_to_remove)
            principal_screen.total -= item_to_remove['montant']
            principal_screen.solde_label.text = f"Solde: {principal_screen.total:.2f} €"
            principal_screen.sauvegarder_donnees()
            self.on_pre_enter()
