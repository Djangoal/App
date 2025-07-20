import json
import os

def calculer_total_charges_restantes():
    try:
        with open('donnees_budget.json', 'r', encoding='utf-8') as f:
            donnees = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0.0

    charges_fixes = donnees.get('charges_fixe', [])
    depenses = donnees.get('depense', [])

    depenses_par_nom = {}
    for d in depenses:
        nom = d['nom']
        montant = d.get('montant', 0)
        depenses_par_nom[nom] = depenses_par_nom.get(nom, 0) + montant

    total_restant = 0.0
    for charge in charges_fixes:
        nom = charge['nom']
        montant_charge = charge.get('montant', 0)
        total_depense = depenses_par_nom.get(nom, 0)
        reste_a_payer = montant_charge - total_depense

        if reste_a_payer < 0:  # Dépassement
            total_restant += reste_a_payer  # Valeur négative
    return total_restant