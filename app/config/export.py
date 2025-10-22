import os, json, csv
from datetime import datetime
from android.permissions import request_permissions, Permission
from android.storage import app_storage_path
from config.popup import afficher_popup

def exporter_vers_csv():
    # --- 1. Demander les permissions Android ---
    try:
        request_permissions([
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
        ])
    except Exception:
        pass

    # --- 2. Déterminer le dossier de destination ---
    dossier_externe = "/storage/emulated/0/Documents/BudgetApp"
    dossier_interne = os.path.join(app_storage_path(), "BudgetApp")

    # On tente d’utiliser le dossier Documents
    try:
        os.makedirs(dossier_externe, exist_ok=True)
        test_file = os.path.join(dossier_externe, "test.txt")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        dossier_export = dossier_externe
        dossier_utilise = "Documents"
    except Exception:
        # Si Android bloque l’accès, on utilise le stockage interne
        os.makedirs(dossier_interne, exist_ok=True)
        dossier_export = dossier_interne
        dossier_utilise = "Interne"
        afficher_popup(
            "⚠️ Impossible d’écrire dans le dossier Documents.\n"
            "Le fichier sera enregistré dans le dossier interne de l’application."
        )

    # --- 3. Charger le fichier JSON ---
    json_file = "donnees_budget.json"
    if not os.path.exists(json_file):
        afficher_popup("Fichier JSON introuvable.")
        return

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            donnees = json.load(f)
    except json.JSONDecodeError:
        afficher_popup("Erreur de lecture du fichier JSON.")
        return

    # --- 4. Créer le fichier CSV ---
    try:
        maintenant = datetime.now()
        mois_fr = [
            "janvier", "février", "mars", "avril", "mai", "juin",
            "juillet", "août", "septembre", "octobre", "novembre", "décembre"
        ]
        mois_nom = mois_fr[maintenant.month - 1]

        nom_fichier = f"compte_{mois_nom}_{maintenant.year}.csv"
        fichier_csv = os.path.join(dossier_export, nom_fichier)

        with open(fichier_csv, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for cat, titre in [
                ("revenu", "Revenus"),
                ("charges_fixe", "Charges Fixes"),
                ("depense", "Dépenses")
            ]:
                writer.writerow([titre])
                writer.writerow(["Date", "Nom", "Montant"])
                for item in donnees.get(cat, []):
                    writer.writerow([
                        item.get("date", ""),
                        item.get("nom", ""),
                        item.get("montant", 0)
                    ])
                writer.writerow([])

        afficher_popup(f"✅ Export réussi dans :\n{fichier_csv}\n\n(Dossier : {dossier_utilise})")

    except Exception as e:
        afficher_popup(f"❌ Erreur lors de l'export : {e}")
