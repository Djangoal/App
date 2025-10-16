from kivy.app import App
from kivy.core.window import Window
Window.clearcolor = (1, 1, 1, 1)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
import json
import os

from util.cercled_checkbox import CercledCheckbox
from date_input import DateInput
from textcheckbox import TextCheckbox
from limited_textinput import LimitedTextInput

from util.ouvrir_menu import ouvrir_menu
from util.economie_utils import calculer_total_economie_arrondi, mise_a_jour_economie
from util.ajout_donnees import ajouter_valeur_ecran
from util.update_affichage import (
    update_affichage_revenus,
    update_affichage_charges,
    update_affichage_depenses,
    update_affichage_restant_a_payer
)
from util.appliquer_config import appliquer_config
from util.mise_a_jour_labels import (
    maj_total_charges_restantes,
    calculer_total_charges_restantes,
    mettre_a_jour_labels
)
from utils import lire_et_calculer_charges_a_payer
from util.gestion_donnees import charger_donnees, sauvegarder_donnees
