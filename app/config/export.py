import os, json, csv
from datetime import datetime
from android.permissions import request_permissions, Permission
from android.storage import app_storage_path
from config.popup import afficher_popup
import locale

def exporter_vers_csv():
    # --- 1. Demander les permissions ---
    try:
        request_permissions([
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
        ])
    except Exception:
        pass

    # --- 2. Déterminer le dossier d'export ---
    # Utilisation du dossier interne (accessible sans restriction)
    dossier_app = os.path.join(app_storage_path(), "BudgetApp")
    os.makedirs(dossier_app, exist_ok=True)

    # Essayer d’utiliser Documents, sinon revenir sur dossier_app
    dossier_export = "/storage/emulated/0/Documents/BudgetApp"
    try:
        os.makedirs(dossier_export, exist_ok=True)
        test_file = os.path.join(dossier_export, "test.txt")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
    except Exception:
        dossier_export = dossier_app  # fallback sécurisé

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
        locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
        nom_fichier = f"compte_{maintenant.strftime('%B')}_{maintenant.year}.csv"
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

        afficher_popup(f"✅ Export réussi dans :\n{fichier_csv}")
    except Exception as e:
        afficher_popup(f"❌ Erreur lors de l'export : {e}")
