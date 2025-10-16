from kivy.uix.textinput import TextInput


class LimitedTextInput(TextInput):
    """
    Champ de saisie avec une limite de caractères.
    Exemple :
        champ = LimitedTextInput(max_chars=20)
    """
    def __init__(self, max_chars=13, **kwargs):
        super().__init__(**kwargs)
        self.max_chars = max_chars

    def insert_text(self, substring, from_undo=False):
        if len(self.text) + len(substring) > self.max_chars:
            substring = substring[:self.max_chars - len(self.text)]
        super().insert_text(substring, from_undo=from_undo)