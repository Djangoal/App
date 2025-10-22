from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.metrics import dp

def afficher_popup(message, titre="Info"):
    # --- Layout principal ---
    layout = BoxLayout(
        orientation='vertical',
        padding=dp(15),
        spacing=dp(10)
    )

    # --- Label texte centré et ajusté ---
    label = Label(
        text=message,
        halign="center",
        valign="middle",
        size_hint=(1, 1),
        color=(1, 1, 1, 1),
        text_size=(Window.width * 0.7, None)
    )

    # Mise à jour automatique de la taille du texte et du label
    def update_label_size(instance, value):
        instance.text_size = (Window.width * 0.7, popup.height * 0.6)
        instance.texture_update()
        instance.font_size = min(Window.height * 0.028, max(Window.height * 0.018, (Window.height * 0.7) / (len(message) + 20)))

    label.bind(size=update_label_size)

    # --- Bouton Fermer ---
    btn_fermer = Button(
        text="Fermer",
        size_hint=(1, None),
        height=Window.height * 0.06,
        font_size=Window.height * 0.025,
        background_color=(0.2, 0.6, 0.86, 1)
    )

    # --- Popup ---
    popup = Popup(
        title=titre,
        content=layout,
        size_hint=(0.8, None),
        height=Window.height * 0.3,
        auto_dismiss=False
    )

    btn_fermer.bind(on_press=popup.dismiss)

    layout.add_widget(label)
    layout.add_widget(btn_fermer)

    popup.open()

    # Mise à jour finale de la taille du texte
    label.text_size = (Window.width * 0.7, popup.height * 0.6)
    label.texture_update()
