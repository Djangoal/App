from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from functools import partial
import os
import json

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
        # Chemin du fichier JSON
        data_file = "donnees_budget.json"
    
        # Réinitialiser le tableau
        self.table_layout.clear_widgets()
        self.table_layout.add_widget(Label(text="Date", bold=True, color=(0, 0, 0, 1)))
        self.table_layout.add_widget(Label(text="Nom", bold=True, color=(0, 0, 0, 1)))
        self.table_layout.add_widget(Label(text="Montant (€)", bold=True, color=(0, 0, 0, 1)))
        self.table_layout.add_widget(Label(text="Action", bold=True, color=(0, 0, 0, 1)))
    
        # Charger les revenus
        revenus = []
        if os.path.exists(data_file):
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    revenus = data.get("revenu", [])
            except json.JSONDecodeError:
                print("Erreur de lecture du fichier JSON.")
    
        # Affichage des lignes
        for index, item in enumerate(revenus):
            self.table_layout.add_widget(Label(text=item.get('date', ''), color=(0, 0, 0, 1)))
            self.table_layout.add_widget(Label(text=item.get('nom', ''), color=(0, 0, 0, 1)))
            self.table_layout.add_widget(Label(text=f"{item.get('montant', 0):.2f} €", color=(0, 0, 0, 1)))
    
            container = BoxLayout(orientation='horizontal', size_hint_x=1)
            container.add_widget(Widget(size_hint_x=1))
    
            btn_suppr = Button(text="Supprimer", size_hint=(None, 1), width=210, background_color=(1, 0, 0, 1))
            btn_suppr.bind(on_press=partial(self.supprimer_revenu, index))  # 🔒 index capturé correctement
    
            container.add_widget(btn_suppr)
            container.add_widget(Widget(size_hint_x=1))
            self.table_layout.add_widget(container)
    
        # Calcul du total
        total_revenus = sum(item.get("montant", 0) for item in revenus)
        self.total_revenus_label.text = f"Total des revenus : {total_revenus:.2f} €"

    def supprimer_revenu(self, index, *args):
    

        data_file = "donnees_budget.json"
    
        if not os.path.exists(data_file):
            return
    
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                donnees = json.load(f)
        except json.JSONDecodeError:
            print("Erreur lors de la lecture du fichier JSON.")
            return
    
        revenus = donnees.get("revenu", [])
    
        if 0 <= index < len(revenus):
            # Supprimer l'élément
            del revenus[index]
            donnees["revenu"] = revenus
    
            # Écriture dans le fichier
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(donnees, f, ensure_ascii=False, indent=4)
    
            # Réafficher la page avec les données mises à jour
            self.on_pre_enter()