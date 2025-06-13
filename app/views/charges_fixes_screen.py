from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.app import App

class ChargesFixesScreen(Screen):
    def __init__(self, **kwargs):
        super(ChargesFixesScreen, self).__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical')

        # Tableau
        self.table_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.table_layout.bind(minimum_height=self.table_layout.setter('height'))

        self.layout.add_widget(self.table_layout)

        # Label du total
        self.total_charges_fixes_label = Label(text="Total des charges : 0.00 €", size_hint=(1, 0.1))
        self.layout.add_widget(self.total_charges_fixes_label)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        print("[ChargesFixesScreen] => Entrée dans l'écran")

        app = App.get_running_app()
        principal_screen = app.root.get_screen('principal')
        soldes = principal_screen.soldes

        print(f"[ChargesFixesScreen] => Chargement des soldes (total: {len(soldes)})")

        self.table_layout.clear_widgets()

        # En-têtes
        self.table_layout.add_widget(Label(text="Date"))
        self.table_layout.add_widget(Label(text="Nom"))
        self.table_layout.add_widget(Label(text="Montant (€)"))
        self.table_layout.add_widget(Label(text="Action"))

        # Filtrage des charges fixes
        charges_fixes = [item for item in soldes if item['type'] == "charges_fixe"]
        print(f"[ChargesFixesScreen] => Nombre de charges fixes trouvées : {len(charges_fixes)}")

        for index, item in enumerate(charges_fixes):
            print(f"[ChargesFixesScreen] => Ajout de l'entrée : {item}")
            self.table_layout.add_widget(Label(text=item['date']))
            self.table_layout.add_widget(Label(text=item['nom']))
            self.table_layout.add_widget(Label(text=f"{item['montant']:.2f} €"))

            # Bouton Supprimer
            container = BoxLayout(orientation='horizontal', size_hint_x=1)
            container.add_widget(Widget(size_hint_x=1))

            btn_suppr = Button(text="Supprimer", size_hint=(None, 1), width=210, background_color=(1, 0, 0, 1))
            btn_suppr.bind(on_press=lambda btn, idx=index: self.supprimer_charge_fixe(idx))
            container.add_widget(btn_suppr)
            container.add_widget(Widget(size_hint_x=1))
            self.table_layout.add_widget(container)

        # Recalcul du total
        total_charges = sum(item['montant'] for item in charges_fixes)
        print(f"[ChargesFixesScreen] => Total recalculé : {total_charges:.2f} €")
        self.total_charges_fixes_label.text = f"Total des charges : {total_charges:.2f} €"

    def supprimer_charge_fixe(self, index):
        print(f"[ChargesFixesScreen] => Suppression demandée à l'index : {index}")

        app = App.get_running_app()
        principal_screen = app.root.get_screen('principal')
        charges_fixes = [item for item in principal_screen.soldes if item['type'] == "charges_fixe"]

        if 0 <= index < len(charges_fixes):
            item_to_remove = charges_fixes[index]
            print(f"[ChargesFixesScreen] => Suppression de : {item_to_remove}")
            principal_screen.soldes.remove(item_to_remove)

            principal_screen.total -= item_to_remove['montant']
            print(f"[ChargesFixesScreen] => Nouveau solde principal : {principal_screen.total:.2f} €")

            principal_screen.solde_label.text = f"Solde: {principal_screen.total:.2f} €"
            principal_screen.sauvegarder_donnees()

            self.on_pre_enter()
        else:
            print(f"[ChargesFixesScreen] => Index {index} invalide pour suppression")