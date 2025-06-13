from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import BooleanProperty

from views.page_principal_screen import pageprincipalScreen
from views.revenus_screen import RevenusScreen
from views.charges_fixes_screen import ChargesFixesScreen
from views.depenses_screen import DepenseScreen
from views.configuration_screen import ConfigurationScreen

from utils.logger import log_crash_info  # ✅ Ajout ici

class MonApp(App):
    # Propriétés pour afficher/masquer les totaux
    show_total_revenus = BooleanProperty(True)
    show_total_charges = BooleanProperty(True)
    show_total_depenses = BooleanProperty(True)

    def build(self):
        try:
            sm = ScreenManager()
            sm.add_widget(pageprincipalScreen(name="principal"))
            sm.add_widget(ChargesFixesScreen(name="charges_fixe"))
            sm.add_widget(RevenusScreen(name="revenus"))
            sm.add_widget(DepenseScreen(name="depense"))
            sm.add_widget(ConfigurationScreen(name="config"))
            return sm
        except Exception as e:
            log_crash_info(f"Erreur dans build() de MonApp : {e}")
            raise e  # Pour que l'erreur reste visible pendant le développement
            from utils.logger import log_error

if __name__ == "__main__":
    try:
        from android.permissions import request_permissions, Permission
        request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
    except:
        pass  # Pas grave si permissions non disponibles

    try:
        MonApp().run()
    except Exception as e:
        log_error(f"Erreur au lancement de l'app : {str(e)}")
