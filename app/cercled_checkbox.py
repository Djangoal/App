from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.graphics import Color, Line, Ellipse
from kivy.properties import StringProperty, BooleanProperty


class CercledCheckbox(BoxLayout):
    def __init__(self, label_text, **kwargs):
        super().__init__(orientation='horizontal', spacing=15, size_hint=(None, None), height=60, width=300, **kwargs)

        self.checkbox = CheckBox(group='type', size_hint=(None, None), size=(50, 50))
        self.label = Label(
            text=label_text,
            color=(0, 0, 0, 1),
            font_size=28,
            size_hint=(None, None),
            size=(200, 50),
            halign='left',
            valign='middle'
        )
        self.label.bind(size=self.label.setter('text_size'))

        self.add_widget(self.checkbox)
        self.add_widget(self.label)

        with self.checkbox.canvas.before:
            # Fond blanc centré
            self.bg_color = Color(1, 1, 1, 1)
            self.bg_circle = Ellipse(pos=self.checkbox.pos, size=self.checkbox.size)

        with self.checkbox.canvas.after:
            # Cercle noir autour
            Color(0, 0, 0, 1)
            self.circle = Line(circle=(self.checkbox.center_x, self.checkbox.center_y, 25), width=1.8)

        self.checkbox.bind(pos=self.update_circle, size=self.update_circle)

    def update_circle(self, *args):
        # Mettre à jour la position/size du fond blanc
        self.bg_circle.pos = self.checkbox.pos
        self.bg_circle.size = self.checkbox.size

        # Mettre à jour le cercle noir
        c_x = self.checkbox.center_x
        c_y = self.checkbox.center_y
        self.circle.circle = (c_x, c_y, 25)

    @property
    def active(self):
        return self.checkbox.active

    @active.setter
    def active(self, val):
        self.checkbox.active = val