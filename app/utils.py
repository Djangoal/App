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
   
############################################################
def recalculer_charges_a_payer(chemin="donnees_budget.json"):
    if os.path.exists(chemin):
        with open(chemin, "r", encoding="utf-8") as f:
            try:
                donnees = json.load(f)
            except json.JSONDecodeError:
                donnees = {}
    else:
        donnees = {}

    charges_fixes = donnees.get("charges_fixe", [])
    charges_a_payer = []

    for charge in charges_fixes:
        montant = charge.get("montant", 0)
        paye = charge.get("paye", False)
        reste = 0 if paye else montant
        charges_a_payer.append({
            "nom": charge.get("nom", ""),
            "montant": montant,
            "paye": paye,
            "reste_a_payer": reste
        })

    donnees["charges_a_payer"] = charges_a_payer

    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=4, ensure_ascii=False)
        
############################################################
def lire_et_calculer_charges_a_payer(json_path='donnees_budget.json'):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        donnees = {}

    charges_fixes = donnees.get('charges_fixe', [])
    depenses = donnees.get('depense', [])

    # Calcul des dépenses par nom
    depenses_par_nom = {}
    for d in depenses:
        nom = d['nom']
        montant = d.get('montant', 0)
        depenses_par_nom[nom] = depenses_par_nom.get(nom, 0) + montant

    # Calcul des charges à payer
    charges_a_payer = []
    for charge in charges_fixes:
        nom = charge['nom']
        montant_charge = charge.get('montant', 0)
        total_depense = depenses_par_nom.get(nom, 0)
        reste_a_payer = montant_charge - total_depense

        if abs(reste_a_payer) > 0.001:
            charge_copie = charge.copy()
            charge_copie['reste_a_payer'] = reste_a_payer
            charges_a_payer.append(charge_copie)

    total_a_payer = sum(item['reste_a_payer'] for item in charges_a_payer if item['reste_a_payer'] < 0)

    # Sauvegarder dans le JSON
    sauvegarder_charges_a_payer(charges_a_payer, json_path)

    return charges_fixes, charges_a_payer, abs(total_a_payer)


def sauvegarder_charges_a_payer(charges_a_payer, json_path='donnees_budget.json'):
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
    else:
        donnees = {}

    donnees["charges_a_payer"] = charges_a_payer
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, indent=4, ensure_ascii=False)
