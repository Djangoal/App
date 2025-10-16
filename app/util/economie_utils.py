import os
import json
import math


def calculer_total_economie_arrondi():
    """
    Calcule le total des économies réalisées
    en arrondissant chaque dépense à l'euro supérieur.
    """
    chemin_fichier = "donnees_budget.json"
    total = 0

    if not os.path.exists(chemin_fichier):
        return 0.0

    try:
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            donnees = json.load(f)
            for dep in donnees.get("depense", []):
                montant = abs(float(dep["montant"]))
                economie = math.ceil(montant) - montant
                total += economie
    except Exception as e:
        print(f"Erreur lors du calcul : {e}")
        return 0.0

    return round(total, 2)


def mise_a_jour_economie(label_widget):
    """
    Met à jour le texte d'un Label Kivy avec le total des économies arrondies.
    """
    total = calculer_total_economie_arrondi()
    label_widget.text = f"Économie dépense arrondi : {total:.2f} €"