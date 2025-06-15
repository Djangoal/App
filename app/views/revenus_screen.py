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
from kivy.uix.screenmanager import Screen
from logger import logger

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

        # Label fixe pour afficher le total en bas, hors du ScrollView
        self.total_revenus_label = Label(text="Total des revenus : 0.00 €",
                                         size_hint=(1, None),
                                         height=50,
                                         font_size=48,
                                         color=(0, 0.5, 0, 1))
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

        revenus = [item for item in soldes if item['type'] == "Revenu"]

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

        # Met à jour le label total fixe (en dehors du ScrollView)
        total_revenus = sum(item["montant"] for item in revenus)
        self.total_revenus_label.text = f"Total des revenus : {total_revenus:.2f} €"


    def supprimer_revenu(self, index):
        app = App.get_running_app()
        principal_screen = app.root.get_screen('principal')
        revenus = [item for item in principal_screen.soldes if item['type'] == "Revenu"]

        if 0 <= index < len(revenus):
            item_to_remove = revenus[index]
            principal_screen.soldes.remove(item_to_remove)
            principal_screen.total -= item_to_remove['montant']
            principal_screen.solde_label.text = f"Solde: {principal_screen.total:.2f} €"
            principal_screen.sauvegarder_donnees()
            self.on_pre_enter()