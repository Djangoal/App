import os, json, csv
from datetime import datetime
from jnius import autoclass
from android.permissions import request_permissions, Permission
from config.popup import afficher_popup

def get_android_version():
    """Retourne la version Android en entier, ex: 8, 9, 10, 11, 12, 13."""
    try:
        Build_VERSION = autoclass('android.os.Build$VERSION')
        version_str = Build_VERSION.RELEASE
        return int(version_str.split('.')[0])
    except Exception:
        return 10  # Par défaut Android 10 si erreur

def get_export_path():
    """Retourne un dossier valide selon la version Android."""
    version = get_android_version()
    if version <= 9:
        # Ancien Android : permissions + accès total
        return "/storage/emulated/0/Download/BudgetApp"
    else:
        # Android 10+ : Scoped Storage, pas besoin de permissions
        return "/storage/emulated/0/Download/BudgetApp"

def exporter_vers_csv():
    # --- 1. Déterminer la version ---
    version = get_android_version()

    # --- 2. Permissions si Android ≤ 9 ---
    if version <= 9:
        try:
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])
        except Exception:
            pass

    # --- 3. Dossier d’export ---
    dossier_export = get_export_path()
    os.makedirs(dossier_export, exist_ok=True)

    # --- 4. Charger les données ---
    json_file = "donnees_budget.json"
    if not os.path.exists(json_file):
        afficher_popup("❌ Fichier JSON introuvable.")
        return

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            donnees = json.load(f)
    except json.JSONDecodeError:
        afficher_popup("❌ Erreur de lecture du fichier JSON.")
        return

    # --- 5. Créer le fichier CSV ---
    try:
        mois_fr = [
            "janvier", "février", "mars", "avril", "mai", "juin",
            "juillet", "août", "septembre", "octobre", "novembre", "décembre"
        ]
        maintenant = datetime.now()
        nom_fichier = f"compte_{mois_fr[maintenant.month - 1]}_{maintenant.year}.csv"
        fichier_csv = os.path.join(dossier_export, nom_fichier)

        with open(fichier_csv, mode='w', newline='', encoding='utf-8') as f:
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
