from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import BooleanProperty

from views.page_principal_screen import pageprincipalScreen
from views.revenus_screen import RevenusScreen
from views.charges_fixes_screen import ChargesFixesScreen
from views.depenses_screen import DepenseScreen
from views.configuration_screen import ConfigurationScreen
import sys
import traceback

def global_exception_handler(exctype, value, tb):
    with open("/storage/emulated/0/appl/rapport_erreur.txt", "w") as f:
        f.write("".join(traceback.format_exception(exctype, value, tb)))

sys.excepthook = global_exception_handler

    
class MonApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(pageprincipalScreen(name="principal"))
        sm.add_widget(ChargesFixesScreen(name="charges_fixe"))
        sm.add_widget(RevenusScreen(name="revenus"))
        sm.add_widget(DepenseScreen(name="depense"))
        sm.add_widget(ConfigurationScreen(name="config"))
        return sm
        
        # Propriétés pour afficher/masquer les totaux
    show_total_revenus = BooleanProperty(True)
    show_total_charges = BooleanProperty(True)
    show_total_depenses = BooleanProperty(True)

if __name__ == "__main__":
    MonApp().run()
