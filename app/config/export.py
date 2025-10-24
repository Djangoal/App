import os, json, csv
from datetime import datetime
from jnius import autoclass, cast
from android.permissions import request_permissions, Permission
from config.popup import afficher_popup

def get_context():
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    return PythonActivity.mActivity

def get_safe_internal_path():
    """Retourne un chemin interne accessible à l'app."""
    context = get_context()
    path = context.getExternalFilesDir(None).getAbsolutePath() + "/exports"
    os.makedirs(path, exist_ok=True)
    return path
    
def get_android_version():
    try:
        Build_VERSION = autoclass('android.os.Build$VERSION')
        version_str = Build_VERSION.RELEASE
        return int(version_str.split('.')[0])
    except Exception:
        return 10

def copy_to_downloads_modern(fichier_source, nom_fichier):
    """Copie le fichier dans /Download via MediaStore (Android 10+)."""
    try:
        MediaStore = autoclass('android.provider.MediaStore$Downloads')
        ContentValues = autoclass('android.content.ContentValues')
        context = get_context()

        resolver = context.getContentResolver()
        values = ContentValues()
        values.put("_display_name", nom_fichier)
        values.put("mime_type", "text/csv")
        values.put("relative_path", "Download/BudgetApp")

        uri = resolver.insert(MediaStore.EXTERNAL_CONTENT_URI, values)
        output_stream = resolver.openOutputStream(uri)

        with open(fichier_source, "rb") as input_file:
            data = input_file.read()
            output_stream.write(data)
            output_stream.close()

        return True
    except Exception as e:
        print("Erreur MediaStore (Android 10+):", e)
        return False

def copy_to_downloads_legacy(fichier_source, nom_fichier):
    """Copie directe dans /storage/emulated/0/Download/BudgetApp (Android 8–9)."""
    try:
        dossier_export = "/storage/emulated/0/Download/BudgetApp"
        os.makedirs(dossier_export, exist_ok=True)
        fichier_dest = os.path.join(dossier_export, nom_fichier)
        with open(fichier_source, "rb") as src, open(fichier_dest, "wb") as dst:
            dst.write(src.read())
        return True
    except Exception as e:
        print("Erreur copie legacy:", e)
        return False

def exporter_vers_csv():
    version = get_android_version()
    try:
        request_permissions([
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE
        ])
    except Exception:
        pass

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

    try:
        mois_fr = [
            "janvier", "février", "mars", "avril", "mai", "juin",
            "juillet", "août", "septembre", "octobre", "novembre", "décembre"
        ]
        maintenant = datetime.now()
        nom_fichier = f"compte_{mois_fr[maintenant.month - 1]}_{maintenant.year}.csv"

        dossier_temp = get_safe_internal_path()
        fichier_temp = os.path.join(dossier_temp, nom_fichier)

        # --- Création du CSV ---
        with open(fichier_temp, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for cat, titre in [("revenu","Revenus"), ("charges_fixe","Charges Fixes"), ("depense","Dépenses")]:
                writer.writerow([titre])
                writer.writerow(["Date", "Nom", "Montant"])
                for item in donnees.get(cat, []):
                    writer.writerow([item.get("date",""), item.get("nom",""), item.get("montant",0)])
                writer.writerow([])

        # --- Export selon version Android ---
        if version >= 10:
            ok = copy_to_downloads_modern(fichier_temp, nom_fichier)
        else:
            ok = copy_to_downloads_legacy(fichier_temp, nom_fichier)

        if ok:
            afficher_popup("Export réussi !\nLe fichier a été enregistré dans le dossier Téléchargements.")
        else:
            afficher_popup("Export créé mais non copié.\nVérifie le dossier interne de l'application.")

    except Exception as e:
        afficher_popup(f"Erreur lors de l'export : {e}")
