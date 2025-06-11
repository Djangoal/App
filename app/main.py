from views.log_screen import LogScreen
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import BooleanProperty

from views.page_principal_screen import pageprincipalScreen
from views.revenus_screen import RevenusScreen
from views.charges_fixes_screen import ChargesFixesScreen
from views.depenses_screen import DepenseScreen
from views.configuration_screen import ConfigurationScreen


    

class MonApp(App):
    def build(self):
        Logger.info("MonApp: Un log important")
        print("Un message dans stdout")
        # Dans ta fonction de création des écrans :
        sm.add_widget(Screen(name='log', content=LogScreen()))
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
