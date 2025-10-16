# util/appliquer_config.py

from kivy.app import App

def appliquer_config(ecran):
    """
    Met à jour l'affichage des totaux et du restant à payer
    en fonction des paramètres de configuration de l'application.
    """
    app = App.get_running_app()
    ecran.label_revenus.opacity = 1 if app.show_total_revenus else 0
    ecran.label_charges.opacity = 1 if app.show_total_charges else 0
    ecran.label_depenses.opacity = 1 if app.show_total_depenses else 0
    ecran.total_charges_restantes_label.opacity = 1 if app.show_restant_a_payer else 0