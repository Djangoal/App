import json
import os

def supprimer_charge(index, chemin="donnees_budget.json"):
    """
    Supprime une charge fixe du fichier JSON selon son index.
    Retourne True si la suppression a réussi, False sinon.
    """
    if not os.path.exists(chemin):
        return False

    # Lecture du fichier JSON
    with open(chemin, 'r', encoding='utf-8') as f:
        donnees = json.load(f)

    charges_fixes = donnees.get('charges_fixe', [])
    if 0 <= index < len(charges_fixes):
        charges_fixes.pop(index)
        donnees['charges_fixe'] = charges_fixes

        # Réécriture du fichier JSON
        with open(chemin, 'w', encoding='utf-8') as f:
            json.dump(donnees, f, indent=4, ensure_ascii=False)
        return True

    return False


def modifier_charge(index, nouvelle_date, nouveau_nom, nouveau_montant, chemin="donnees_budget.json"):
    """
    Modifie une charge fixe dans le fichier JSON.
    Retourne True si la modification a réussi, False sinon.
    """
    if not os.path.exists(chemin):
        return False

    # Vérifie que le montant est bien un nombre
    try:
        nouveau_montant = float(nouveau_montant)
    except ValueError:
        return False

    with open(chemin, 'r', encoding='utf-8') as f:
        donnees = json.load(f)

    charges_fixes = donnees.get('charges_fixe', [])
    if 0 <= index < len(charges_fixes):
        charge = charges_fixes[index]
        charge['date'] = nouvelle_date
        charge['nom'] = nouveau_nom
        charge['montant'] = nouveau_montant

        donnees['charges_fixe'] = charges_fixes
        with open(chemin, 'w', encoding='utf-8') as f:
            json.dump(donnees, f, indent=4, ensure_ascii=False)
        return True

    return False