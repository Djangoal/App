from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

def afficher_popup(message, titre="Info"):
    layout = BoxLayout(
        orientation='vertical',
        padding=Window.height * 0.02,
        spacing=Window.height * 0.02
    )

    label = Label(
        text=message,
        size_hint=(1, None),
        halign="center",
        valign="middle",
        font_size=Window.height * 0.025,
        text_size=(Window.width * 0.7, None)
    )
    label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))

    btn_fermer = Button(
        text="Fermer",
        size_hint=(1, None),
        height=Window.height * 0.06,
        font_size=Window.height * 0.025
    )

    popup = Popup(
        title=titre,
        content=layout,
        size_hint=(0.8, 0.3),
        auto_dismiss=False
    )
    btn_fermer.bind(on_press=popup.dismiss)

    layout.add_widget(label)
    layout.add_widget(btn_fermer)
    popup.open()