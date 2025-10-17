from util.import_page_charges import *

class ChargesFixesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # === Attributs ===
        self.charges_a_payer = []
        self.base_width = 1080
        self.scale = Window.width / self.base_width
        self.font_size_label = max(12, Window.height * 0.02)
        self.max_scroll_height = Window.height * 0.5

        # === Layout principal ===
        # structure : header (hauteur fixe) / content (remplit) / nav (hauteur fixe)
        self.root_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.root_layout)

        # --- Header (titre + boutons afficher/masquer) : hauteur FIXE ---
        title_height = Window.height * 0.08
        btn_height = Window.height * 0.06
        header_height = title_height + btn_height * 2 + 10  # +10 pour spacing/padding

        header_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        header_layout.height = header_height  # IMPORTANT : hauteur fixe

        # Titre
        title_font = sp(22)
        title_label = Label(
            text="Liste des charges",
            font_size=title_font,
            size_hint=(1, None),
            height=title_height,
            bold=True,
            color=(0, 0, 0, 1)
        )
        header_layout.add_widget(title_label)

        # Bouton afficher/masquer charges fixes
        self.btn_toggle_fixes = Button(
            text='Afficher les Charges Fixes',
            size_hint_y=None,
            height=btn_height,
            background_color=(0.2, 0.8, 0.6, 1)
        )
        self.btn_toggle_fixes.bind(on_release=self.toggle_charges_fixes)
        header_layout.add_widget(self.btn_toggle_fixes)

        # Bouton afficher/masquer charges à payer
        self.btn_toggle_payer = Button(
            text='Afficher les Charges à Payer',
            size_hint_y=None,
            height=btn_height,
            background_color=(0.2, 0.8, 0.6, 1)
        )
        self.btn_toggle_payer.bind(on_release=self.toggle_charges_a_payer)
        header_layout.add_widget(self.btn_toggle_payer)

        self.root_layout.add_widget(header_layout)

        # --- Content : zone qui remplit l'espace restant (ici se trouvent les tableaux) ---
        self.content = BoxLayout(orientation='vertical', size_hint=(1, 1), spacing=10)
        self.root_layout.add_widget(self.content)

        # Tableaux (initialement cachés : height = 0)
        self._create_table_charges_fixes()
        self._create_table_charges_a_payer()
        self._create_total_charges_fixes_label()
        
        self._create_total_charges_a_payer_label()

        # --- Navigation : toujours en BOTTOM, hauteur FIXE ---
        nav_layout = BoxLayout(size_hint_y=None, height=btn_height, spacing=10)
        self.btn_voir_revenus = Button(text="Revenus")
        self.btn_voir_revenus.bind(on_press=lambda x: setattr(self.manager, 'current', 'revenus'))
        nav_layout.add_widget(self.btn_voir_revenus)

        self.btn_voir_depense = Button(text="Dépense")
        self.btn_voir_depense.bind(on_press=lambda x: setattr(self.manager, 'current', 'depense'))
        nav_layout.add_widget(self.btn_voir_depense)

        self.btn_retour = Button(text="Retour")
        self.btn_retour.bind(on_press=lambda x: setattr(self.manager, 'current', 'principal'))
        nav_layout.add_widget(self.btn_retour)

        self.root_layout.add_widget(nav_layout)

        # États
        self.fixes_visible = False
        self.payer_visible = False

    # -------------------------
    # Création widgets (private helpers)
    # -------------------------
    def _create_table_charges_fixes(self):
        row_height = Window.height * 0.04
        # container dans content : on l'ajoute dans self.content pour rester dans zone centrale
        self.table_fixes_container = ScrollView(size_hint=(1, None), height=0)
        self.table_layout = GridLayout(
            cols=4, size_hint_y=None, spacing=5,
            row_force_default=True, row_default_height=row_height
        )
        self.table_layout.bind(minimum_height=self.table_layout.setter('height'))
        self.table_fixes_container.add_widget(self.table_layout)
        self.content.add_widget(self.table_fixes_container)

    def _create_total_charges_fixes_label(self):
        btn_height = Window.height * 0.06
        self.total_charges_fixes_label = Label(
            text="Total des charges : 0.00 €",
            size_hint=(1, None),
            height=btn_height,
            font_size=sp(15),
            color=(0, 0, 0, 1)
        )
        self.content.add_widget(self.total_charges_fixes_label)

    def _create_table_charges_a_payer(self):
        row_height = Window.height * 0.04
        self.table_payer_container = ScrollView(size_hint=(1, None), height=0)
        self.payer_layout = GridLayout(
            cols=2, size_hint_y=None, spacing=5,
            row_force_default=True, row_default_height=row_height
        )
        self.payer_layout.bind(minimum_height=self.payer_layout.setter('height'))
        self.table_payer_container.add_widget(self.payer_layout)
        self.content.add_widget(self.table_payer_container)

    def _create_total_charges_a_payer_label(self):
        btn_height = Window.height * 0.06
        self.total_Charges_à_Payer_label = Label(
            text="Total restant à payer : 0.00 €",
            size_hint=(1, None),
            height=btn_height,
            font_size=sp(15),
            color=(0, 0, 0, 1)
        )
        self.content.add_widget(self.total_Charges_à_Payer_label)

# -------------------------
    # Toggle (ouverture / fermeture)
    # -------------------------
    def toggle_charges_fixes(self, instance):
        # Fermer les charges à payer si elles sont ouvertes
        if self.table_payer_container.height > 0:
            self.table_payer_container.height = 0
            self.btn_toggle_payer.text = 'Afficher les Charges à Payer'

        # Garde la hauteur maximale limitée et n'affecte pas la nav
        if self.table_fixes_container.height == 0:
            desired = min(self.table_layout.height, self.max_scroll_height)
            self.table_fixes_container.height = desired if desired > 0 else Window.height * 0.25
            self.btn_toggle_fixes.text = 'Masquer les Charges Fixes'
        else:
            self.table_fixes_container.height = 0
            self.btn_toggle_fixes.text = 'Afficher les Charges Fixes'

    def toggle_charges_a_payer(self, instance):
        # Fermer les charges fixes si elles sont ouvertes
        if self.table_fixes_container.height > 0:
            self.table_fixes_container.height = 0
            self.btn_toggle_fixes.text = 'Afficher les Charges Fixes'

        if self.table_payer_container.height == 0:
            desired = min(self.payer_layout.height, self.max_scroll_height)
            self.table_payer_container.height = desired if desired > 0 else Window.height * 0.15
            self.btn_toggle_payer.text = 'Masquer les Charges à Payer'
        else:
            self.table_payer_container.height = 0
            self.btn_toggle_payer.text = 'Afficher les Charges à Payer'    

    # -------------------------
    # Lifecycle et affichage
    # -------------------------
    def on_pre_enter(self):
        charges_fixes, self.charges_a_payer, total_a_payer = lire_et_calculer_charges_a_payer()
        self.afficher_charges_fixes(charges_fixes)
        self.afficher_charges_a_payer()
        total_charges = sum(item['montant'] for item in charges_fixes)
        self.total_charges_fixes_label.text = f"Total des charges : {abs(total_charges):.2f} €"
        self.total_Charges_à_Payer_label.text = f"Total restant à payer : {total_a_payer:.2f} €"

    def afficher_charges_fixes(self, charges_fixes):
        self.table_layout.clear_widgets()
        header_font = dp(18 * self.scale)
        row_font = dp(16 * self.scale)

        # En-têtes avec mêmes proportions
        self.table_layout.add_widget(Label(
            text="[b]Date[/b]", markup=True, color=(0, 0, 0, 1),
            font_size=header_font, size_hint_x=0.25
        ))
        self.table_layout.add_widget(Label(
            text="[b]Nom[/b]", markup=True, color=(0, 0, 0, 1),
            font_size=header_font, size_hint_x=0.4
        ))
        self.table_layout.add_widget(Label(
            text="[b]Montant[/b]", markup=True, color=(0, 0, 0, 1),
            font_size=header_font, size_hint_x=0.25
        ))
        self.table_layout.add_widget(Label(
            text="", markup=True, color=(0, 0, 0, 1),
            font_size=header_font, size_hint_x=0.1
        ))

        for index, item in enumerate(charges_fixes):
            self.table_layout.add_widget(Label(
                text=item['date'],
                color=(0, 0, 0, 1),
                font_size=row_font, size_hint_x=0.25
            ))
            self.table_layout.add_widget(Label(
                text=item['nom'],
                color=(0, 0, 0, 1),
                font_size=row_font, size_hint_x=0.4
            ))
            self.table_layout.add_widget(Label(
                text=f"{item['montant']:.2f} €",
                color=(0, 0, 0, 1),
                font_size=row_font, size_hint_x=0.25
            ))

            container = BoxLayout(orientation='horizontal', size_hint_x=0.1)
            btn_modifier = Button(
                text="->",
                size_hint=(1, 1),
                font_size=row_font,
                background_color=(0.2, 0.6, 0.8, 1)
            )
            btn_modifier.bind(on_press=lambda btn, idx=index: ouvrir_popup_modification(self, index))
            container.add_widget(btn_modifier)
            self.table_layout.add_widget(container)

        # si le tableau est visible, ajuste sa hauteur pour permettre le scroll (sans pousser la nav)
        if self.table_fixes_container.height > 0:
            self.table_fixes_container.height = min(self.table_layout.height, self.max_scroll_height)

    def afficher_charges_a_payer(self):
        self.payer_layout.clear_widgets()
        header_font = dp(18 * self.scale)
        row_font = dp(16 * self.scale)

        self.payer_layout.add_widget(Label(
            text="[b]Nom[/b]", markup=True, color=(0, 0, 0, 1), font_size=header_font
        ))
        self.payer_layout.add_widget(Label(
            text="[b]Reste à payer (€)[/b]", markup=True, color=(0, 0, 0, 1), font_size=header_font
        ))

        for item in self.charges_a_payer:
            self.payer_layout.add_widget(Label(
                text=item['nom'], color=(0, 0, 0, 1), font_size=row_font,
                halign="left", text_size=(Window.width * 0.4, None)
            ))

            reste = item.get('reste_a_payer', 0)
            color = (0.2, 0.4, 1, 1) if reste < 0 else (0, 0.5, 0, 1)
            self.payer_layout.add_widget(Label(
                text=f"{abs(reste):.2f} €", color=color, font_size=row_font,
                halign="right", text_size=(Window.width * 0.4, None)
            ))

        if self.table_payer_container.height > 0:
            self.table_payer_container.height = min(self.payer_layout.height, self.max_scroll_height)

    
