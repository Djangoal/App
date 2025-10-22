from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
import json
import os
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from utils import lire_et_calculer_charges_a_payer
from kivy.core.window import Window
from kivy.metrics import sp
from kivy.metrics import dp
from util.supprimer_charge import supprimer_charge, modifier_charge
from util.popup_modification_charge import ouvrir_popup_modification