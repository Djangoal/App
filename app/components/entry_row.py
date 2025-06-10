from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class EntryRow(BoxLayout):
    def __init__(self, date, nom, montant, supprimer_callback, index, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=40, **kwargs)
        self.add_widget(Label(text=date))
        self.add_widget(Label(text=nom))
        self.add_widget(Label(text=f"{montant:.2f} €"))
        btn = Button(text="Supprimer", size_hint_x=0.3)
        btn.bind(on_press=lambda x: supprimer_callback(index))
        self.add_widget(btn)
