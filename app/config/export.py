import os, json, csv, io
from datetime import datetime
from config.popup import afficher_popup

try:
    from jnius import autoclass, cast
except ImportError:
    autoclass = None

MOIS_FR = {
    "January": "janvier", "February": "février", "March": "mars",
    "April": "avril", "May": "mai", "June": "juin",
    "July": "juillet", "August": "août", "September": "septembre",
    "October": "octobre", "November": "novembre", "December": "décembre"
}


def exporter_vers_csv():
    """Export CSV compatible Android 8 → 14"""
    json_file = "donnees_budget.json"
    if not os.path.exists(json_file):
        afficher_popup("❌ Le fichier 'donnees_budget.json' est introuvable.")
        return

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            donnees = json.load(f)
    except json.JSONDecodeError:
        afficher_popup("❌ Erreur de lecture du fichier JSON.")
        return

    # Création du contenu CSV
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

    # Nom de fichier
    mois_en = datetime.now().strftime("%B")
    mois_fr = MOIS_FR.get(mois_en, mois_en).capitalize()
    nom_fichier = f"compte_{mois_fr}_{datetime.now().year}.csv"

    try:
        if autoclass:
            # === Android ===
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            VERSION = autoclass("android.os.Build$VERSION")  # ✅ correction ici
            version_android = int(VERSION.SDK_INT)
            activity = PythonActivity.mActivity

            if version_android >= 30:
                # Android 11+
                Environment = autoclass("android.os.Environment")
                MediaStore = autoclass("android.provider.MediaStore$Downloads")
                ContentValues = autoclass("android.content.ContentValues")

                resolver = activity.getContentResolver()
                values = ContentValues()
                values.put("_display_name", nom_fichier)
                values.put("mime_type", "text/csv")
                values.put("relative_path", "Download/BudgetApp")

                uri = resolver.insert(MediaStore.EXTERNAL_CONTENT_URI, values)
                output_stream = resolver.openOutputStream(uri)
                output_stream.write(contenu_csv)
                output_stream.close()

                afficher_popup("✅ Export réussi dans :\nTéléchargements/BudgetApp")
            else:
                # Android 10 ou moins → écriture directe
                dossier = "/storage/emulated/0/Download/BudgetApp"
                os.makedirs(dossier, exist_ok=True)
                chemin = os.path.join(dossier, nom_fichier)
                with open(chemin, "wb") as f:
                    f.write(contenu_csv)
                afficher_popup(f"✅ Exporté dans :\n{chemin}")
        else:
            # Mode PC / Pydroid
            dossier = os.path.join(os.path.expanduser("~"), "Downloads", "BudgetApp")
            os.makedirs(dossier, exist_ok=True)
            chemin = os.path.join(dossier, nom_fichier)
            with open(chemin, "wb") as f:
                f.write(contenu_csv)
            afficher_popup(f"✅ Exporté dans :\n{chemin}")

    except Exception as e:
        afficher_popup(f"❌ Erreur lors de l’export :\n{e}")
