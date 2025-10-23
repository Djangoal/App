import os, json, csv
from datetime import datetime
from android.permissions import request_permissions, Permission
from config.popup import afficher_popup

def exporter_vers_csv():
    # --- 1. Demande de permissions (pour Android < 10) ---
    try:
        request_permissions([
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE
        ])
    except Exception:
        pass

    # --- 2. Dossier d’export universel ---
    dossier_export = "/storage/emulated/0/Download/BudgetApp"
    os.makedirs(dossier_export, exist_ok=True)

    # --- 3. Fichier source ---
    json_file = "donnees_budget.json"
    if not os.path.exists(json_file):
        afficher_popup("❌ Fichier JSON introuvable.")
        return

    # --- 4. Charger les données ---
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            donnees = json.load(f)
    except json.JSONDecodeError:
        afficher_popup("❌ Erreur de lecture du fichier JSON.")
        return

    # --- 5. Création du fichier CSV ---
    try:
        mois_fr = [
            "janvier", "février", "mars", "avril", "mai", "juin",
            "juillet", "août", "septembre", "octobre", "novembre", "décembre"
        ]
        maintenant = datetime.now()
        nom_fichier = f"compte_{mois_fr[maintenant.month - 1]}_{maintenant.year}.csv"
        fichier_csv = os.path.join(dossier_export, nom_fichier)

        with open(fichier_csv, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for cat, titre in [("revenu","Revenus"), ("charges_fixe","Charges Fixes"), ("depense","Dépenses")]:
                writer.writerow([titre])
                writer.writerow(["Date", "Nom", "Montant"])
                for item in donnees.get(cat, []):
                    writer.writerow([item.get("date",""), item.get("nom",""), item.get("montant",0)])
                writer.writerow([])

        afficher_popup(f"✅ Export réussi dans :\n{fichier_csv}")
    except Exception as e:
        afficher_popup(f"❌ Erreur lors de l'export : {e}")
