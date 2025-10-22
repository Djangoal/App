import os
import json
from util.economie_utils import mise_a_jour_economie  # si tu l’utilises
from util.limiteur_texte import limiter_longueur
from util.mise_a_jour_labels import (
    maj_total_charges_restantes,
    calculer_total_charges_restantes,
    mettre_a_jour_labels
)
from util.gestion_donnees import charger_donnees, sauvegarder_donnees


def ajouter_valeur_ecran(ecran):
    """Gère l'ajout de valeurs dans le fichier JSON depuis la page principale."""
    try:
        montant = float(ecran.montant_input.text)
        nom = ecran.nom_input.text.strip()
        ecran.nom_input.bind(text=lambda instance, value: limiter_longueur(instance, value))
        date = ecran.date_input.text.strip()

        if not nom or not date:
            return

        # --- Détermination de la catégorie ---
        if ecran.revenu_testbox.state == 'down':
            categorie = 'revenu'
        elif ecran.charges_fixe_testbox.state == 'down':
            categorie = 'charges_fixe'
            montant = -abs(montant)
        elif ecran.depense_testbox.state == 'down':
            categorie = 'depense'
            montant = -abs(montant)
        else:
            return

        # --- Lecture ou création du fichier JSON ---
        data = {}
        if os.path.exists(ecran.data_file):
            with open(ecran.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

        for cat in ['revenu', 'charges_fixe', 'depense']:
            if cat not in data:
                data[cat] = []

        # --- Ajout de la nouvelle entrée ---
        nouvelle_entree = {"nom": nom, "date": date, "montant": montant}
        data[categorie].append(nouvelle_entree)

        # --- Mise à jour des charges à payer ---
        if categorie == 'charges_fixe':
            charges_a_payer = data.get("charges_a_payer", [])
            charges_a_payer.append({
                "nom": nom,
                "date": date,
                "montant": abs(montant),
                "reste_a_payer": montant  # négatif
            })
            data["charges_a_payer"] = charges_a_payer

        elif categorie == 'depense':
            charges_a_payer = data.get("charges_a_payer", [])
            montant_restant = abs(montant)

            for charge in charges_a_payer:
                if charge["nom"].lower() == nom.lower() and montant_restant > 0:
                    if abs(charge["reste_a_payer"]) >= montant_restant:
                        charge["reste_a_payer"] += montant_restant  # vers 0
                        montant_restant = 0
                    else:
                        montant_restant -= abs(charge["reste_a_payer"])
                        charge["reste_a_payer"] = 0

            data["charges_a_payer"] = charges_a_payer

        # --- Sauvegarde dans le fichier ---
        with open(ecran.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        # --- Réinitialisation des champs ---
        ecran.nom_input.text = ""
        ecran.date_input.text = ""
        ecran.montant_input.text = ""
        ecran.revenu_testbox.state = 'normal'
        ecran.charges_fixe_testbox.state = 'normal'
        ecran.depense_testbox.state = 'normal'

        # --- Mise à jour de l’interface ---
        charger_donnees(ecran)
        mettre_a_jour_labels(ecran)
        
        total_restant = calculer_total_charges_restantes()
        
        mise_a_jour_economie(ecran.label_economie)

    except ValueError:
        print("Montant invalide")