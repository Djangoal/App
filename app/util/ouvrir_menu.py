from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.core.window import Window


def ouvrir_menu(instance):
    """Ouvre un menu popup de navigation."""
    # Layout vertical pour les boutons du menu
    menu_layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

    # Création du popup
    popup_menu = Popup(
        title="Menu de navigation",
        content=menu_layout,
        size_hint=(None, None),
        size=(Window.width * 0.8, Window.height * 0.32),
        auto_dismiss=True
    )

    buttons_data = [
        ("Charge", "charges_fixe"),
        ("Revenu", "revenus"),
        ("Dépense", "depense"),
        ("Épargne", "epargne"),
        ("Configuration", "config")
    ]

    def changer_ecran_depuis_menu(screen_name):
        popup_menu.dismiss()
        try:
            instance.manager.current = screen_name
        except Exception:
            if hasattr(instance, 'changer_ecran'):
                instance.changer_ecran(None, screen_name)

    for text, screen_name in buttons_data:
        btn = Button(text=text, size_hint_y=None, height=80)
        btn.bind(on_press=lambda _, s=screen_name: changer_ecran_depuis_menu(s))
        menu_layout.add_widget(btn)

    popup_menu.open()
