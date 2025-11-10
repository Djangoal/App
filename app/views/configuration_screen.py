from util.import_page_config import *

class ConfigurationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        app = App.get_running_app()

        # ScrollView principal
        scroll = ScrollView(size_hint=(1, 1))
        self.layout = BoxLayout(
            orientation='vertical',
            padding=Window.height*0.02,
            spacing=Window.height*0.02,
            size_hint_y=None
        )
        self.layout.bind(minimum_height=self.layout.setter('height'))

        # === Titre ===
        titre = Label(
            text="Page de Configuration",
            font_size=Window.height*0.04,
            size_hint=(1, None),
            height=Window.height*0.08,
            bold=True,
            color=(0,0,0,1)
        )
        self.layout.add_widget(titre)

        # === SECTION PIN ===
        pin_section = PinSection()
        self.layout.add_widget(pin_section)

        # === SWITCHES SECTION ===
        switches_section = SwitchesSection(self)
        self.layout.add_widget(switches_section)

        # Widget flexible pour pousser le contenu vers le haut
        self.layout.add_widget(Widget(size_hint_y=1))

        # === BOUTONS D'ACTIONS ===
        # Export CSV
        
        btn_logs = Button(
            text="Voir les logs",
            size_hint=(1, None),
            height=Window.height * 0.04,
            font_size=Window.height * 0.025,
            background_color=(1, 0, 0, 1)
        )
        btn_logs.bind(on_press=self.voir_logs)
        self.layout.add_widget(btn_logs)
        
        btn_export_csv = Button(
            text="Exporter en CSV",
            size_hint=(1, None),
            height=Window.height*0.04,
            font_size=Window.height*0.025
        )
        btn_export_csv.bind(on_press=lambda x: exporter_vers_csv())
        self.layout.add_widget(btn_export_csv)

        # Réinitialiser revenus/dépense
        bouton_reset = Button(
            text="Réinitialiser revenus/dépense",
            size_hint=(1, None),
            height=Window.height*0.04,
            font_size=Window.height*0.025,
            background_color=(1,0.4,0.9,1)
        )
        bouton_reset.bind(on_press=self.confirmer_reinitialisation)
        self.layout.add_widget(bouton_reset)

        # Bouton Retour
        bouton_retour = Button(
            text="Retour",
            size_hint=(1, None),
            height=Window.height*0.04,
            font_size=Window.height*0.025,
            background_color=(0.2,0.6,0.86,1)
        )
        bouton_retour.bind(on_press=self.retour_page_principale)
        self.layout.add_widget(bouton_retour)

        scroll.add_widget(self.layout)
        self.add_widget(scroll)

    # =================== Réinitialisation ===================
    def confirmer_reinitialisation(self, instance):
        from kivy.uix.popup import Popup

        contenu = BoxLayout(orientation='vertical', spacing=Window.height*0.02, padding=Window.height*0.02)
        message = Label(
            text="Voulez-vous vraiment réinitialiser toutes les données ?",
            text_size=(Window.width*0.7, None),
            halign="center",
            valign="middle",
            font_size=Window.height*0.025,
            size_hint=(1,None),
            height=Window.height*0.15
        )
        contenu.add_widget(message)

        boutons = BoxLayout(spacing=Window.width*0.02, size_hint=(1,None), height=Window.height*0.08)
        btn_oui = Button(text="Oui", font_size=Window.height*0.025)
        btn_non = Button(text="Non", font_size=Window.height*0.025)
        boutons.add_widget(btn_oui)
        boutons.add_widget(btn_non)
        contenu.add_widget(boutons)

        popup = Popup(title="Confirmation", content=contenu, size_hint=(0.8,None), height=Window.height*0.35, auto_dismiss=False)
        btn_oui.bind(on_press=lambda *a: (self.reinitialiser_donnees(), popup.dismiss()))
        btn_non.bind(on_press=popup.dismiss)
        popup.open()

    def reinitialiser_donnees(self):
        app = App.get_running_app()
        chemin = "donnees_budget.json"
        if os.path.exists(chemin):
            with open(chemin, "r", encoding="utf-8") as f:
                try:
                    donnees = json.load(f)
                except:
                    donnees = {}
            donnees.pop("revenu", None)
            donnees.pop("depense", None)
            donnees.pop("charges_a_payer", None)
            with open(chemin, "w", encoding="utf-8") as f:
                json.dump(donnees, f, indent=4, ensure_ascii=False)
        # Réinitialiser labels de l'écran principal
        principal = self.manager.get_screen("principal")
        principal.total = 0
        principal.soldes = []
        principal.label_revenus.text = "Revenus : 0.00 €"
        principal.label_depenses.text = "Dépenses : 0.00 €"
        principal.solde_label.text = "Solde actuel : 0.00 €"
        principal.fin_label.text = "Fin de mois : 0.00 €"

    def voir_logs(self, instance):
        logger.info("Navigation vers l'écran Journalisation")
        self.manager.current = 'logs'
    # =================== Retour ===================
    def retour_page_principale(self, instance):
        self.manager.current = "principal"