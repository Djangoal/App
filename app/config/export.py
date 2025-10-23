import os, json, csv, io
from datetime import datetime
from config.popup import afficher_popup

try:
    from jnius import autoclass
except ImportError:
    autoclass = None  # si on teste sur PC

MOIS_FR = {
    "January": "janvier", "February": "février", "March": "mars",
    "April": "avril", "May": "mai", "June": "juin",
    "July": "juillet", "August": "août", "September": "septembre",
    "October": "octobre", "November": "novembre", "December": "décembre"
}


def exporter_vers_csv():
    """Export CSV universel (Android 8–14) vers le dossier Téléchargements/BudgetApp"""
    json_file = "donnees_budget.json"
    if not os.path.exists(json_file):
        afficher_popup("Le fichier 'donnees_budget.json' est introuvable.")
        return

    # Charger les données JSON
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            donnees = json.load(f)
    except json.JSONDecodeError:
        afficher_popup(" Erreur de lecture du fichier JSON.")
        return

    # Construire le contenu CSV en mémoire
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    for cat, titre in [("revenu", "Revenus"), ("charges_fixe", "Charges Fixes"), ("depense", "Dépenses")]:
        writer.writerow([titre])
        writer.writerow(["Date", "Nom", "Montant"])
        for item in donnees.get(cat, []):
            writer.writerow([item.get("date", ""), item.get("nom", ""), item.get("montant", 0)])
        writer.writerow([])

    contenu_csv = buffer.getvalue().encode("utf-8")
    buffer.close()

    # Nom du fichier (avec mois français)
    mois_en = datetime.now().strftime("%B")
    mois_fr = MOIS_FR.get(mois_en, mois_en).capitalize()
    annee = datetime.now().year
    nom_fichier = f"compte_{mois_fr}_{annee}.csv"

    try:
        if autoclass:  # --- Exécution sur Android ---
            Environment = autoclass("android.os.Environment")
            MediaStore = autoclass("android.provider.MediaStore$Downloads")
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            ContentValues = autoclass("android.content.ContentValues")

            resolver = PythonActivity.mActivity.getContentResolver()
            values = ContentValues()
            values.put("_display_name", nom_fichier)
            values.put("mime_type", "text/csv")
            values.put("relative_path", "Download/BudgetApp")

            uri = resolver.insert(MediaStore.EXTERNAL_CONTENT_URI, values)
            output_stream = resolver.openOutputStream(uri)

            # Écrire le contenu CSV directement dans le flux Java
            output_stream.write(contenu_csv)
            output_stream.close()

            afficher_popup(f" Export réussi !\n\nFichier : {nom_fichier}\nDossier : Téléchargements/BudgetApp")
        else:
            # --- Mode fallback (ordinateur ou Pydroid) ---
            dossier_export = os.path.join(os.path.expanduser("~"), "Downloads", "BudgetApp")
            os.makedirs(dossier_export, exist_ok=True)
            fichier_csv = os.path.join(dossier_export, nom_fichier)
            with open(fichier_csv, "wb") as f:
                f.write(contenu_csv)
            afficher_popup(f" Exporté dans : {fichier_csv}")

    except Exception as e:
        afficher_popup(f" Erreur lors de l’export :\n{e}")
