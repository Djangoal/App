from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color, Line


class TextCheckbox(ToggleButton):
    def __init__(self, text="", **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (1, 1, 1, 1)
        self.color = (0, 0, 0, 1)

        # Bordure noire
        with self.canvas.after:
            Color(0, 0, 0, 1)
            self._border = Line(rectangle=(self.x, self.y, self.width, self.height), width=1.5)

        # Mises à jour
        self.bind(pos=self.update_border, size=self.update_border)
        self.bind(state=self.update_color)
        self.bind(size=self.update_font_size)  # 🔑 met à jour la police

        # Taille de police initiale
        self.font_size = self.height * 0.4

    def update_border(self, *args):
        self._border.rectangle = (self.x, self.y, self.width, self.height)

    def update_color(self, instance, value):
        if value == 'down':
            self.background_color = (0.3, 0.8, 0.3, 1)
        else:
            self.background_color = (1, 1, 1, 1)

    def update_font_size(self, *args):
        """ Ajuste la taille du texte en fonction de la hauteur du bouton """
        self.font_size = self.height * 0.4