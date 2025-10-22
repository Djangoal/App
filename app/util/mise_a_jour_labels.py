import os
import json

def maj_total_charges_restantes(ecran):
    total_restant = calculer_total_charges_restantes()
    ecran.total_charges_restantes_label.text = f"restant à payer : {abs(total_restant):.2f} €"

def calculer_total_charges_restantes():
    chemin_fichier = "donnees_budget.json"
    total_restant = 0.0

    if os.path.exists(chemin_fichier):
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            donnees = json.load(f)
            charges_a_payer = donnees.get("charges_a_payer", [])

            for charge in charges_a_payer:
                montant = charge.get("reste_a_payer", 0.0)
                if montant < 0:
                    total_restant += montant

    return total_restant


def mettre_a_jour_labels(ecran):
    try:
        with open('donnees_budget.json', 'r', encoding='utf-8') as f:
            donnees = json.load(f)
    except Exception as e:
        print("Erreur lors de la lecture du fichier JSON :", e)
        donnees = {}

    # Calculs
    total_revenus = sum(item.get('montant', 0) for item in donnees.get('revenu', []))
    total_charges = sum(item.get('montant', 0) for item in donnees.get('charges_fixe', []))
    total_depenses = sum(item.get('montant', 0) for item in donnees.get('depense', []))
    total_reste_a_payer = sum(item.get('reste_a_payer', 0) for item in donnees.get('charges_a_payer', []))

    # Mise à jour des labels
    ecran.label_revenus.text = f"Revenus : {total_revenus:.2f} €"
    ecran.label_charges.text = f"Charges Fixes : {abs(total_charges):.2f} €"
    ecran.label_depenses.text = f"Dépenses : {abs(total_depenses):.2f} €"

    # Solde
    solde = total_revenus + total_depenses
    ecran.solde_label.text = f"Solde actuel : {solde:.2f} €"
    ecran.solde_label.color = (0.2, 0.4, 1, 1) if solde >= 0 else (1, 0, 0, 1)

    # Fin de mois
    fin_de_mois = total_revenus - abs(total_depenses) - abs(total_reste_a_payer)
    ecran.fin_label.text = f"Fin de mois : {fin_de_mois:.2f} €"
    ecran.fin_label.color = (0.2, 0.6, 0.2, 1) if fin_de_mois >= 0 else (1, 0, 0, 1)
    
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