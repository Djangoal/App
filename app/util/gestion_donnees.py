import json
import os
from util.mise_a_jour_labels import mettre_a_jour_labels, maj_total_charges_restantes, calculer_total_charges_restantes


def charger_donnees(ecran):
    """
    Charge les données du fichier JSON et met à jour les labels sur la page principale.
    """
    if os.path.exists(ecran.data_file):
        with open(ecran.data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            ecran.soldes = data.get("soldes", [])

            # 🔹 Mise à jour des affichages
            mettre_a_jour_labels(ecran)
            maj_total_charges_restantes(ecran)
            
            total_restant = calculer_total_charges_restantes()
            ecran.total_charges_restantes_label.text = f"Restant à payer : {abs(total_restant):.2f} €"
    else:
        ecran.soldes = []


def sauvegarder_donnees(ecran):
    """
    Sauvegarde les soldes dans le fichier JSON.
    """
    with open(ecran.data_file, "w", encoding="utf-8") as f:
        json.dump({"soldes": ecran.soldes}, f, ensure_ascii=False, indent=4)