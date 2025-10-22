from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

def ouvrir_menu(self):
    """Ouvre un menu popup responsive avec des boutons proportionnels."""

    # Layout principal du menu (vertical)
    menu_layout = BoxLayout(
        orientation='vertical',
        spacing=Window.height * 0.015,  # espacement proportionnel à la hauteur
        padding=[Window.width * 0.05, Window.height * 0.02]  # marges internes
    )

    # Liste des boutons du menu
    buttons_data = [
        ("Charge", "charges_fixe"),
        ("Revenu", "revenus"),
        ("Dépense", "depense"),
        ("Épargne", "epargne"),
        ("Configuration", "config")
    ]

    # Fonction locale pour changer d’écran depuis le popup
    def changer_ecran_depuis_menu(screen_name):
        popup_menu.dismiss()
        try:
            self.manager.current = screen_name
        except Exception:
            if hasattr(self, 'changer_ecran'):
                self.changer_ecran(screen_name)

    # Création des boutons du menu
    for label, screen_name in buttons_data:
        btn = Button(
            text=label,
            size_hint=(1, None),  # largeur = 100% du layout
            height=Window.height * 0.035,  # hauteur responsive (7% de la hauteur écran)
            font_size=f"{int(Window.height * 0.01)}sp",  # texte responsive
            background_color=(0.2, 0.6, 0.86, 1),  # bleu clair
            color=(1, 1, 1, 1),  # texte blanc
            bold=True
        )
        btn.bind(on_release=lambda _, s=screen_name: changer_ecran_depuis_menu(s))
        menu_layout.add_widget(btn)

    # Création du popup responsive
    popup_menu = Popup(
        title="Menu de navigation",
        content=menu_layout,
        size_hint=(None, None),
        size=(Window.width * 0.8, Window.height * 0.35),  # popup = 80% largeur, 50% hauteur
        auto_dismiss=True
    )

    popup_menu.open()