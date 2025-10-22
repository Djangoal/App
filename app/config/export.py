import os, json, csv
from datetime import datetime
from config.popup import afficher_popup

# Dictionnaire pour traduire les mois en français
MOIS_FR = {
    "January": "janvier",
    "February": "février",
    "March": "mars",
    "April": "avril",
    "May": "mai",
    "June": "juin",
    "July": "juillet",
    "August": "août",
    "September": "septembre",
    "October": "octobre",
    "November": "novembre",
    "December": "décembre"
}

def get_downloads_path():
    """Retourne le dossier de téléchargement de l'utilisateur."""
    downloads_dir = "/storage/emulated/0/Download/BudgetApp"
    os.makedirs(downloads_dir, exist_ok=True)
    return downloads_dir


def exporter_vers_csv():
    """Exporte les données JSON vers un fichier CSV dans Download/BudgetApp/."""
    json_file = "donnees_budget.json"
    dossier_export = get_downloads_path()

    # --- Vérifier le fichier JSON ---
    if not os.path.exists(json_file):
        afficher_popup("❌ Le fichier 'donnees_budget.json' est introuvable.")
        return

    # --- Charger les données ---
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            donnees = json.load(f)
    except json.JSONDecodeError:
        afficher_popup("❌ Erreur de lecture du fichier JSON.")
        return

    # --- Nom du fichier CSV avec mois en français ---
    mois_en = datetime.now().strftime("%B")
    mois_fr = MOIS_FR.get(mois_en, mois_en).capitalize()
    annee = datetime.now().year
    nom_fichier = f"compte_{mois_fr}_{annee}.csv"
    fichier_csv = os.path.join(dossier_export, nom_fichier)

    # --- Création du CSV ---
    try:
        with open(fichier_csv, mode="w", newline="", encoding="utf-8") as f:
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

        afficher_popup(f"✅ Export réussi !\n\nFichier enregistré dans :\n{fichier_csv}")

    except PermissionError:
        afficher_popup("⚠️ Accès refusé.\n\nAutorisez l’accès au stockage dans les paramètres Android.")
    except Exception as e:
        afficher_popup(f"❌ Erreur lors de l'export :\n{e}")
