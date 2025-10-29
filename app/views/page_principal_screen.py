from util.import_page_principale import *
from pub.admob import AdMobBanner  # Import de la classe bannière
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.app import App

class pageprincipalScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        app = App.get_running_app()
        self.data_file = "donnees_budget.json"
        self.soldes = []
        self.total = 0

        # ⚙️ Layout principal vertical
        self.main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.add_widget(self.main_layout)

        # 🧩 Organisation des éléments
        self.configurer_bindings(app)
        self.creer_header()
        self.creer_formulaire()
        self.creer_categorie_checkboxes()
        self.creer_bouton_valider()
        self.creer_labels()
        self.creer_menu_bouton()

        # 🔄 Initialisation de l’affichage
        self.initialiser_affichage(app)

    # =====================================================
    # 🔹 Sous-méthodes de construction
    # =====================================================

    def configurer_bindings(self, app):
        app.bind(show_total_revenus=lambda i, v: update_affichage_revenus(self, i, v))
        app.bind(show_total_charges=lambda i, v: update_affichage_charges(self, i, v))
        app.bind(show_total_depenses=lambda i, v: update_affichage_depenses(self, i, v))

    def creer_header(self):
        layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=5, spacing=5)
        with layout.canvas.before:
            Color(1, 0, 0, 1)
            self.header_bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=lambda w, s: setattr(self.header_bg, 'size', s),
                    pos=lambda w, p: setattr(self.header_bg, 'pos', p))

        title = Label(
            text='[b]Mon Budget Perso[/b]',
            markup=True,
            halign='center',
            valign='middle',
            color=(1, 1, 1, 1)
        )
        title.bind(size=lambda instance, value: setattr(title, 'text_size', (title.width, title.height)))

        close_button = Button(
            text='X',
            size_hint=(None, 1),
            width=Window.width * 0.1,
            background_color=(1, 1, 1, 1),
            color=(1, 0, 0, 1),
            background_normal=''
        )
        close_button.bind(on_release=self.close_app)

        layout.add_widget(title)
        layout.add_widget(close_button)
        self.main_layout.add_widget(layout)

    def creer_formulaire(self):
        input_wrapper = BoxLayout(size_hint=(1, None), height=0.15 * Window.height, padding=2)
        with input_wrapper.canvas.before:
            Color(0, 0, 0, 1)
            self.border_rect = Rectangle(size=input_wrapper.size, pos=input_wrapper.pos)
        input_wrapper.bind(size=lambda w, s: setattr(self.border_rect, 'size', s),
                           pos=lambda w, p: setattr(self.border_rect, 'pos', p))

        inner_layout = BoxLayout(orientation='vertical', spacing=5, padding=10)
        with inner_layout.canvas.before:
            Color(0.2, 0.8, 0.6, 1)
            self.bg_rect = Rectangle(size=inner_layout.size, pos=inner_layout.pos)
        inner_layout.bind(size=lambda w, s: setattr(self.bg_rect, 'size', s),
                          pos=lambda w, p: setattr(self.bg_rect, 'pos', p))

        self.nom_input = LimitedTextInput(hint_text="Nom", multiline=False)
        self.date_input = DateInput(hint_text="Date (jj/mm/aaaa)", multiline=False)
        self.montant_input = TextInput(hint_text="Montant", multiline=False)

        inner_layout.add_widget(self.nom_input)
        inner_layout.add_widget(self.date_input)
        inner_layout.add_widget(self.montant_input)
        input_wrapper.add_widget(inner_layout)

        self.main_layout.add_widget(input_wrapper)

    def creer_categorie_checkboxes(self):
        checkbox_wrapper = BoxLayout(size_hint=(1, None), height=0.06 * Window.height, padding=2)
        checkbox_container = BoxLayout(
            orientation='horizontal',
            spacing=40,
            size_hint=(0.5, 0.5),
            height=0.06 * Window.height,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.revenu_testbox = TextCheckbox(text="Revenu", group="categorie", allow_no_selection=True)
        self.charges_fixe_testbox = TextCheckbox(text="Charge", group="categorie", allow_no_selection=True)
        self.depense_testbox = TextCheckbox(text="Dépense", group="categorie", allow_no_selection=True)

        checkbox_container.add_widget(self.revenu_testbox)
        checkbox_container.add_widget(self.charges_fixe_testbox)
        checkbox_container.add_widget(self.depense_testbox)
        checkbox_wrapper.add_widget(checkbox_container)
        self.main_layout.add_widget(checkbox_wrapper)

    def creer_bouton_valider(self):
        self.valider_btn = Button(
            text="Valider",
            size_hint=(1, 0.1),
            height=50,
            background_color=(0.2, 0.6, 0.86, 1),
            background_normal=''
        )
        self.valider_btn.bind(on_press=self.ajouter_valeur)
        self.main_layout.add_widget(self.valider_btn)

    def creer_labels(self):
        scroll = ScrollView(size_hint=(1, 0.5))
        labels_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=10)
        labels_container.bind(minimum_height=labels_container.setter('height'))

        labels_data = [
            ("Restant à payer : 0.00 €", "total_charges_restantes_label"),
            ("Revenus : 0.00 €", "label_revenus"),
            ("Charges Fixes : 0.00 €", "label_charges"),
            ("Dépenses : 0.00 €", "label_depenses"),
            ("Économie dépense arrondi : 0.00 €", "label_economie")
        ]

        for text, attr_name in labels_data:
            label = Label(text=text, font_size=28, size_hint_y=None, height=40, halign='center', valign='middle', color=(0, 0, 0, 1))
            label.bind(size=label.setter('text_size'))
            setattr(self, attr_name, label)
            labels_container.add_widget(label)

        labels_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=20)
        self.solde_label = Label(text="Solde actuel : 0.00 €", font_size=30, halign='left', valign='middle', color=(1, 0, 0, 1))
        self.solde_label.bind(size=self.solde_label.setter('text_size'))
        self.fin_label = Label(text="Fin de mois : 0.00 €", font_size=30, halign='right', valign='middle', color=(1, 0, 0, 1))
        self.fin_label.bind(size=self.fin_label.setter('text_size'))

        labels_row.add_widget(self.solde_label)
        labels_row.add_widget(self.fin_label)
        labels_container.add_widget(labels_row)
        scroll.add_widget(labels_container)
        self.main_layout.add_widget(scroll)

    def creer_menu_bouton(self):
        """Ajoute la bannière AdMob puis le bouton Menu."""
        # ⚡ Bannière responsive
        # juste avant le bouton Menu
        self.banner = AdMobBanner()
        self.main_layout.add_widget(self.banner)

        # Bouton Menu
        menu_button = Button(
            text="Menu",
            size_hint=(0.5, 0.1),
            height=40,
            pos_hint={'center_x': 0.5}
        )
        menu_button.bind(on_press=lambda instance: ouvrir_menu(self))
        self.main_layout.add_widget(menu_button)

    # =====================================================
    # 🔹 Initialisation et logique
    # =====================================================
    def initialiser_affichage(self, app):
        charger_donnees(self)
        maj_total_charges_restantes(self)
        mettre_a_jour_labels(self)
        total_restant = calculer_total_charges_restantes()
        self.total_charges_restantes_label.text = f"Restant à payer : {abs(total_restant):.2f} €"

        update_affichage_revenus(self, app, app.show_total_revenus)
        update_affichage_charges(self, app, app.show_total_charges)
        update_affichage_depenses(self, app, app.show_total_depenses)

    def ajouter_valeur(self, instance):
        ajouter_valeur_ecran(self)
    
    def on_pre_enter(self):
        appliquer_config(self)
        _, charges_a_payer, total_a_payer = lire_et_calculer_charges_a_payer()
        self.total_charges_restantes_label.text = f"Total des charges restant à payer : {total_a_payer:.2f} €"
        charger_donnees(self)        
        maj_total_charges_restantes(self)
        mettre_a_jour_labels(self)
        mise_a_jour_economie(self.label_economie)
        
    def close_app(self, instance):
        App.get_running_app().stop()