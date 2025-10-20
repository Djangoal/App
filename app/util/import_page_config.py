import os
import csv
import json
import locale
import hashlib
from kivy.app import App
from logger import logger
from datetime import datetime
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.switch import Switch
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.scrollview import ScrollView
from util.gestion_donnees import charger_donnees, sauvegarder_donnees
