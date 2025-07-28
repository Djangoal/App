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
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup


class ChargesFixesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.charges_a_payer = []

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # === Section "Charges Fixes" ===
        self.btn_toggle_fixes = Button(text='Afficher les Charges Fixes', size_hint_y=None, height=60)
        self.btn_toggle_fixes.bind(on_release=self.toggle_charges_fixes)
        self.layout.add_widget(self.btn_toggle_fixes)

        self.table_fixes_container = ScrollView(size_hint=(1, None), height=0)
        self.table_layout = GridLayout(cols=4, size_hint_y=None, spacing=5,
                                       row_force_default=True, row_default_height=50)
        self.table_layout.bind(minimum_height=self.table_layout.setter('height'))
        self.table_fixes_container.add_widget(self.table_layout)
        self.layout.add_widget(self.table_fixes_container)
        
        
        scrollview = ScrollView()
        contenu = GridLayout(cols=1, size_hint_y=None, spacing=10)
        contenu.bind(minimum_height=contenu.setter('height'))


        self.total_charges_fixes_label = Label(
            text="Total des charges : 0.00 €",
            size_hint=(1, None),
            height=50,
            font_size=28,
            color=(0, 0, 0, 1)
        )
        scrollview.add_widget(contenu)
        self.layout.add_widget(self.total_charges_fixes_label)
        self.layout.add_widget(scrollview)

        # === Section "Charges à Payer" ===
        self.btn_toggle_payer = Button(text='Afficher les Charges à Payer', size_hint_y=None, height=60)
        self.btn_toggle_payer.bind(on_release=self.toggle_charges_a_payer)
        self.layout.add_widget(self.btn_toggle_payer)

        self.table_payer_container = ScrollView(size_hint=(1, None), height=0)
        self.payer_layout = GridLayout(cols=2, size_hint_y=None, spacing=5,
                                       row_force_default=True, row_default_height=50)
        self.payer_layout.bind(minimum_height=self.payer_layout.setter('height'))
        self.table_payer_container.add_widget(self.payer_layout)
        self.layout.add_widget(self.table_payer_container)
        
        # ---- ZONE DE CONTENU (ex: liste, tableau) ----
        scrollview2 = ScrollView()
        contenu = GridLayout(cols=1, size_hint_y=None, spacing=10)
        contenu.bind(minimum_height=contenu.setter('height'))

        self.total_Charges_à_Payer_label = Label(
            text="Total des charges restant à payer : 0.00 €",
            size_hint=(1, None),
            height=50,
            font_size=28,
            color=(0, 0, 0, 1)
        )
        
        scrollview2.add_widget(contenu)
        
        self.layout.add_widget(self.total_Charges_à_Payer_label)
        
        self.layout.add_widget(scrollview2)

        # === Boutons navigation ===
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

        self.layout.add_widget(buttons_layout)
        self.add_widget(self.layout)

        # États d'affichage
        self.fixes_visible = False
        self.payer_visible = False

    def toggle_charges_fixes(self, instance):
        max_height = 900  # hauteur max en pixels
        if self.table_fixes_container.height == 0:
            desired_height = self.table_layout.height
            self.table_fixes_container.height = min(desired_height, max_height)
            self.btn_toggle_fixes.text = 'Masquer les Charges Fixes'
        else:
            self.table_fixes_container.height = 0
            self.btn_toggle_fixes.text = 'Afficher les Charges Fixes'

    def toggle_charges_a_payer(self, *args):
        self.payer_visible = not self.payer_visible
        
        max_height = 900  # limite max en pixels
        desired_height = self.table_layout.height if self.payer_visible else 0
        self.table_payer_container.height = min(desired_height, max_height)
        
        self.btn_toggle_payer.text = (
            'Masquer les Charges à Payer' if self.payer_visible else 'Afficher les Charges à Payer'
        )
    def on_pre_enter(self):
        app = App.get_running_app()
        try:
            with open('donnees_budget.json', 'r', encoding='utf-8') as f:
                donnees = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            donnees = {}

        charges_fixes = donnees.get('charges_fixe', [])
        depenses = donnees.get('depense', [])

        depenses_par_nom = {}
        for d in depenses:
            nom = d['nom']
            montant = d.get('montant', 0)
            depenses_par_nom[nom] = depenses_par_nom.get(nom, 0) + montant

        self.charges_a_payer = []
        for charge in charges_fixes:
            nom = charge['nom']
            montant_charge = charge.get('montant', 0)
            total_depense = depenses_par_nom.get(nom, 0)
            reste_a_payer = montant_charge - total_depense

            if abs(reste_a_payer) > 0.001:
                charge_copie = charge.copy()
                charge_copie['reste_a_payer'] = reste_a_payer
                self.charges_a_payer.append(charge_copie)

        # Remplir tableau Charges Fixes
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
            btn_modifier = Button(text="Modifier", size_hint=(0.8, 1), background_color=(0.2, 0.6, 0.8, 1))
            btn_modifier.bind(on_press=lambda btn, idx=index: self.ouvrir_popup_modification(idx))
            anchor.add_widget(btn_modifier)
            self.table_layout.add_widget(anchor)

        # Remplir tableau Charges à Payer
        self.payer_layout.clear_widgets()
        self.payer_layout.add_widget(Label(text="[b]Nom[/b]", markup=True, color=(0, 0, 0, 1)))
        self.payer_layout.add_widget(Label(text="[b]Reste à payer (€)[/b]", markup=True, color=(0, 0, 0, 1)))

        for item in self.charges_a_payer:
            self.payer_layout.add_widget(Label(text=item['nom'], color=(0, 0, 0, 1)))
            reste = item.get('reste_a_payer', 0)
            if reste < 0:
                lbl = Label(text=f"{abs(reste):.2f} €", color=(0.2, 0.4, 1, 1))
            else:
                lbl = Label(text=f"+{reste:.2f} €", color=(0, 0.5, 0, 1))
            self.payer_layout.add_widget(lbl)

        total_charges = sum(item['montant'] for item in charges_fixes)
        self.total_charges_fixes_label.text = f"Total des charges : {abs(total_charges):.2f} €"

        total_a_payer = sum(item['reste_a_payer'] for item in self.charges_a_payer if item['reste_a_payer'] < 0)
        self.total_Charges_à_Payer_label.text = f"Total des charges restant à payer : {abs(total_a_payer):.2f} €"

        self.sauvegarder_charges_a_payer()
        

    def sauvegarder_charges_a_payer(self):
        chemin = "donnees_budget.json"
        if os.path.exists(chemin):
            with open(chemin, 'r', encoding='utf-8') as f:
                donnees = json.load(f)
        else:
            donnees = {}

        donnees["charges_a_payer"] = self.charges_a_payer
        with open(chemin, 'w', encoding='utf-8') as f:
            json.dump(donnees, f, indent=4, ensure_ascii=False)
            

    def ouvrir_popup_modification(self, index):
        # Placeholder: à implémenter selon ta logique
        
        # Charger données JSON
        chemin = "donnees_budget.json"
        if os.path.exists(chemin):
            with open(chemin, 'r', encoding='utf-8') as f:
                donnees = json.load(f)
        else:
            donnees = {}
    
        charges_fixes = donnees.get('charges_fixe', [])
    
        if index >= len(charges_fixes):
            return  # index hors limite
    
        charge = charges_fixes[index]
    
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
    
        date_input = TextInput(
            text=charge['date'],
            multiline=False,
            hint_text="Date",
            size_hint_y=1,
            background_color=(0.95, 0.95, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
    
        nom_input = TextInput(
            text=charge['nom'],
            multiline=False,
            hint_text="Nom",
            size_hint_y=1,
            background_color=(0.95, 1, 0.95, 1),
            foreground_color=(0, 0, 0, 1)
        )
    
        montant_input = TextInput(
            text=str(charge['montant']),
            multiline=False,
            hint_text="Montant",
            size_hint_y=1,
            background_color=(1, 0.95, 0.95, 1),
            foreground_color=(0, 0, 0, 1)
        )
    
        layout.add_widget(Label(text="Modifier la charge :"))
        layout.add_widget(date_input)
        layout.add_widget(nom_input)
        layout.add_widget(montant_input)
    
        btns = BoxLayout(size_hint_y=1, size_hint_x=1, spacing=1)
        btn_valider = Button(text="Valider", background_color=(0, 0.6, 0, 1))
        btn_supprimer = Button(text="Supprimer", background_color=(0.8, 0, 0, 1))
        btn_annuler = Button(text="Annuler", background_color=(0.5, 0.5, 0.5, 1))
    
        popup = Popup(title="Modifier la charge", content=layout, size_hint=(0.9, 0.7), auto_dismiss=False)
        layout.add_widget(btns)
        btns.add_widget(btn_valider)
        btns.add_widget(btn_supprimer)
        btns.add_widget(btn_annuler)
    
        btn_valider.bind(on_press=lambda x: self.modifier_charge(index, date_input.text, nom_input.text, montant_input.text, popup))
        btn_supprimer.bind(on_press=lambda x: (self.supprimer_charge(index), popup.dismiss()))
        btn_annuler.bind(on_press=popup.dismiss)
    
        popup.open()
    
    
    def modifier_charge(self, index, nouvelle_date, nouveau_nom, nouveau_montant, popup):
        try:
            nouveau_montant = float(nouveau_montant)
        except ValueError:
            return  # montant invalide
    
        chemin = "donnees_budget.json"
        if os.path.exists(chemin):
            with open(chemin, 'r', encoding='utf-8') as f:
                donnees = json.load(f)
        else:
            donnees = {}
    
        charges_fixes = donnees.get('charges_fixe', [])
    
        if 0 <= index < len(charges_fixes):
            charge = charges_fixes[index]
            charge['date'] = nouvelle_date
            charge['nom'] = nouveau_nom
            charge['montant'] = nouveau_montant
    
            donnees['charges_fixe'] = charges_fixes
            with open(chemin, 'w', encoding='utf-8') as f:
                json.dump(donnees, f, indent=4, ensure_ascii=False)
    
            self.on_pre_enter()
            popup.dismiss()
    
    
    def supprimer_charge(self, index):
        chemin = "donnees_budget.json"
        if os.path.exists(chemin):
            with open(chemin, 'r', encoding='utf-8') as f:
                donnees = json.load(f)
        else:
            donnees = {}
    
        charges_fixes = donnees.get('charges_fixe', [])
    
        if 0 <= index < len(charges_fixes):
            charges_fixes.pop(index)
            donnees['charges_fixe'] = charges_fixes
    
            with open(chemin, 'w', encoding='utf-8') as f:
                json.dump(donnees, f, indent=4, ensure_ascii=False)
    
            self.on_pre_enter()