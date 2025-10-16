from kivy.app import App

def update_affichage_revenus(ecran, instance, value):
    """Affiche ou masque le total des revenus."""
    ecran.label_revenus.opacity = 1 if value else 0

def update_affichage_charges(ecran, instance, value):
    """Affiche ou masque le total des charges fixes."""
    ecran.label_charges.opacity = 1 if value else 0

def update_affichage_depenses(ecran, instance, value):
    """Affiche ou masque le total des dépenses."""
    ecran.label_depenses.opacity = 1 if value else 0

def update_affichage_restant_a_payer(ecran, instance, value):
    """Affiche ou masque le total des charges restantes à payer."""
    app = App.get_running_app()
    ecran.total_charges_restantes_label.opacity = 1 if value else 0
    ecran.total_charges_restantes_label.height = 50 if value else 0
    app.bind(show_restant_a_payer=lambda inst, val: update_affichage_restant_a_payer(ecran, inst, val))