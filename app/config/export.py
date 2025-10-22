import os, json, csv
from datetime import datetime
import locale
from config.popup import afficher_popup
from android.permissions import request_permissions, Permission

def exporter_vers_csv():
    request_permissions([
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE
    ])

    json_file = "donnees_budget.json"
    dossier_export = os.path.join("/storage/emulated/0/Documents", "BudgetApp")
    os.makedirs(dossier_export, exist_ok=True)

    if not os.path.exists(json_file):
        afficher_popup("Fichier JSON introuvable.")
        return

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            donnees = json.load(f)
    except json.JSONDecodeError:
        afficher_popup("Erreur de lecture du fichier JSON.")
        return

    try:
        maintenant = datetime.now()
        nom_fichier = f"compte_{maintenant.strftime('%B')}_{maintenant.year}.csv"
        fichier_csv = os.path.join(dossier_export, nom_fichier)

        with open(fichier_csv, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            for cat, titre in [("revenu","Revenus"), ("charges_fixe","Charges Fixes"), ("depense","Dépenses")]:
                writer.writerow([titre])
                writer.writerow(["Date", "Nom", "Montant"])
                for item in donnees.get(cat, []):
                    writer.writerow([item.get("date",""), item.get("nom",""), item.get("montant",0)])
                writer.writerow([])

        afficher_popup(f"Exporté dans :\n{fichier_csv}")
    except Exception:
        afficher_popup("Erreur lors de l'export")