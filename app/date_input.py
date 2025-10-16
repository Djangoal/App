# date_input.py

from kivy.uix.textinput import TextInput

class DateInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        # Garde uniquement les chiffres
        substring = ''.join(c for c in substring if c.isdigit())

        # Retirer les '/' existants dans le texte courant
        text = self.text.replace('/', '')

        # Limiter la longueur à 8 caractères (JJMMAAAA)
        if len(text) >= 8:
            return

        new_text = text + substring
        if len(new_text) > 4:
            new_text = new_text[:2] + '/' + new_text[2:4] + '/' + new_text[4:]
        elif len(new_text) > 2:
            new_text = new_text[:2] + '/' + new_text[2:]
        else:
            new_text = new_text

        self.text = new_text
        # Positionner le curseur à la fin
        self.cursor = (len(self.text), 0)