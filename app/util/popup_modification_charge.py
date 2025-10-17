import os
import json
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window

from util.supprimer_charge import supprimer_charge, modifier_charge


def ouvrir_popup_modification(screen_instance, index):
    """Affiche la popup de modification d'une charge fixe."""

    chemin = "donnees_budget.json"
    if os.path.exists(chemin):
        with open(chemin, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
    else:
        donnees = {}

    charges_fixes = donnees.get('charges_fixe', [])
    if index >= len(charges_fixes):
        return

    charge = charges_fixes[index]
    font_size = max(14, Window.height * 0.02)

    layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
    date_input = TextInput(text=charge['date'], multiline=False, hint_text="Date", font_size=font_size, size_hint_y=None, height=font_size * 2)
    nom_input = TextInput(text=charge['nom'], multiline=False, hint_text="Nom", font_size=font_size, size_hint_y=None, height=font_size * 2)
    montant_input = TextInput(text=str(charge['montant']), multiline=False, hint_text="Montant", font_size=font_size, size_hint_y=None, height=font_size * 2)
    layout.add_widget(date_input)
    layout.add_widget(nom_input)
    layout.add_widget(montant_input)

    # Boutons
    btns = BoxLayout(size_hint_y=None, height=font_size * 3, spacing=10)
    btn_valider = Button(text="Valider", font_size=font_size, background_color=(0, 0.6, 0, 1))
    btn_supprimer = Button(text="Supprimer", font_size=font_size, background_color=(0.8, 0, 0, 1))
    btn_annuler = Button(text="Annuler", font_size=font_size, background_color=(0.5, 0.5, 0.5, 1))
    btns.add_widget(btn_valider)
    btns.add_widget(btn_supprimer)
    btns.add_widget(btn_annuler)
    layout.add_widget(btns)

    popup = Popup(
        title="Modifier la charge",
        content=layout,
        size_hint=(0.9, 0.3),
        auto_dismiss=False,
        title_size=font_size * 1.2
    )

    # Actions
    btn_valider.bind(on_press=lambda x: _valider_modification(screen_instance, index, date_input.text, nom_input.text, montant_input.text, popup))
    btn_supprimer.bind(on_press=lambda x: (_supprimer_charge(screen_instance, index), popup.dismiss()))
    btn_annuler.bind(on_press=popup.dismiss)

    popup.open()


def _valider_modification(screen_instance, index, nouvelle_date, nouveau_nom, nouveau_montant, popup):
    if modifier_charge(index, nouvelle_date, nouveau_nom, nouveau_montant):
        screen_instance.on_pre_enter()
        popup.dismiss()


def _supprimer_charge(screen_instance, index):
    if supprimer_charge(index):
        screen_instance.on_pre_enter()