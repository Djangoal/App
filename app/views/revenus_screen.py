from util.import_page_revenu import*

class RevenusScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 📐 Taille d'écran dynamique
        self.base_width = 1080
        self.scale = Window.width / self.base_width

        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Titre
        title_label = Label(
            text="Liste des Revenus",
            font_size=dp(24 * self.scale),
            size_hint=(1, None),
            height=dp(50 * self.scale),
            bold=True,
            color=(0, 0, 0, 1)
        )
        layout.add_widget(title_label)

        # Tableau
        self.table_layout = GridLayout(
            cols=4,
            size_hint_y=None,
            spacing=dp(5),
            row_force_default=True,
            row_default_height=dp(20 * self.scale)
        )
        self.table_layout.bind(minimum_height=self.table_layout.setter('height'))

        self.scroll = ScrollView()
        self.scroll.add_widget(self.table_layout)
        layout.add_widget(self.scroll)

        # Total revenus
        self.total_revenus_label = Label(
            text="Total des revenus : 0.00 €",
            size_hint=(1, None),
            height=dp(30 * self.scale),
            font_size=dp(20 * self.scale),
            color=(0, 0.5, 0, 1)
        )
        layout.add_widget(self.total_revenus_label)

        # Boutons navigation
        buttons_layout = BoxLayout(size_hint=(1, None), height=dp(50 * self.scale), spacing=dp(10))

        self.btn_voir_charges_fixe = Button(text="charges fixe", font_size=dp(16 * self.scale))
        self.btn_voir_charges_fixe.bind(on_press=lambda x: setattr(self.manager, 'current', 'charges_fixe'))
        buttons_layout.add_widget(self.btn_voir_charges_fixe)

        self.btn_voir_depense = Button(text="depense", font_size=dp(16 * self.scale))
        self.btn_voir_depense.bind(on_press=lambda x: setattr(self.manager, 'current', 'depense'))
        buttons_layout.add_widget(self.btn_voir_depense)

        self.btn_retour = Button(text="Retour", font_size=dp(16 * self.scale))
        self.btn_retour.bind(on_press=lambda x: setattr(self.manager, 'current', 'principal'))
        buttons_layout.add_widget(self.btn_retour)

        layout.add_widget(buttons_layout)
        self.add_widget(layout)

    def on_pre_enter(self):
        data_file = "donnees_budget.json"
    
        # Nettoyer le tableau
        self.table_layout.clear_widgets()
        header_font = dp(18 * self.scale)
    
        # --- En-têtes avec proportions ---
        self.table_layout.add_widget(Label(
            text="[b]Date[/b]", markup=True, color=(0, 0, 0, 1),
            font_size=header_font, size_hint_x=0.35
        ))
        self.table_layout.add_widget(Label(
            text="[b]Nom[/b]", markup=True, color=(0, 0, 0, 1),
            font_size=header_font, size_hint_x=0.4
        ))
        self.table_layout.add_widget(Label(
            text="[b]Montant[/b]", markup=True, color=(0, 0, 0, 1),
            font_size=header_font, size_hint_x=0.3
        ))
        self.table_layout.add_widget(Label(
            text="", markup=True, color=(0, 0, 0, 1),
            font_size=header_font, size_hint_x=0.05
        ))
    
        # --- Charger les revenus ---
        revenus = []
        if os.path.exists(data_file):
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    revenus = data.get("revenu", [])
            except json.JSONDecodeError:
                print("Erreur de lecture du fichier JSON.")
    
        row_font = dp(16 * self.scale)
    
        # --- Afficher chaque revenu ---
        for index, item in enumerate(revenus):
            self.table_layout.add_widget(Label(
                text=item.get('date', ''), color=(0, 0, 0, 1),
                font_size=row_font, size_hint_x=0.2
            ))
            self.table_layout.add_widget(Label(
                text=item.get('nom', ''), color=(0, 0, 0, 1),
                font_size=row_font, size_hint_x=0.4
            ))
            self.table_layout.add_widget(Label(
                text=f"{item.get('montant', 0):.2f} €", color=(0, 0, 0, 1),
                font_size=row_font, size_hint_x=0.3
            ))
    
            # Colonne action (bouton X)
            container = BoxLayout(orientation='horizontal', size_hint_x=0.1)
            btn_suppr = Button(
                text="X",
                size_hint=(1, 1),
                font_size=dp(14 * self.scale),
                background_color=(1, 0, 0, 1)
            )
            btn_suppr.bind(on_press=partial(self.afficher_confirmation_suppression, index))
            container.add_widget(btn_suppr)
    
            self.table_layout.add_widget(container)
    
        # --- Mettre à jour le total ---
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

    def afficher_confirmation_suppression(self, index, *args):
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))

        message = Label(
            text="Confirmer la suppression de ce revenu ?",
            size_hint=(1, 1),  # occupe tout l’espace disponible
            halign="center",
            valign="middle",
            font_size=dp(18 * self.scale)
        )
        message.bind(size=lambda inst, val: setattr(inst, "text_size", val))

        boutons = BoxLayout(size_hint=(1, None), height=dp(60 * self.scale), spacing=dp(20))
        btn_annuler = Button(text="Annuler", font_size=dp(16 * self.scale))
        btn_confirmer = Button(text="Confirmer", background_color=(1, 0, 0, 1), font_size=dp(16 * self.scale))

        popup = Popup(
            title="Confirmation",
            content=layout,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )

        def confirmer_action(instance):
            popup.dismiss()
            self.supprimer_revenu(index)
            self.on_pre_enter()

        btn_annuler.bind(on_press=popup.dismiss)
        btn_confirmer.bind(on_press=confirmer_action)

        boutons.add_widget(btn_annuler)
        boutons.add_widget(btn_confirmer)

        layout.add_widget(message)
        layout.add_widget(Widget())
        layout.add_widget(boutons)

        popup.open()
        