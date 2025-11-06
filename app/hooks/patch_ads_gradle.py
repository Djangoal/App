import time
from pathlib import Path

def after_apk_build(ctx, **kwargs):
    """
    Hook exécuté juste après la génération du projet Android.
    Injecte la dépendance AdMob (Google Ads) dans le build.gradle du projet.
    """
    base_path = Path.home() / ".local/share/python-for-android/dists"
    # Recherche automatique du dossier de build (release ou debug)
    possible_dirs = list(base_path.glob("monapp_*"))
    if not possible_dirs:
        print("[Hook AdMob] ❌ Aucun dossier de build trouvé !")
        return
    dist_dir = possible_dirs[0]
    gradle_file = dist_dir / "build.gradle"

    # ⏳ Attendre que le fichier soit créé
    for i in range(30):
        if gradle_file.exists():
            break
        print(f"[Hook AdMob] ⏳ build.gradle non trouvé (tentative {i+1}/30)...")
        time.sleep(1)
    else:
        print(f"[Hook AdMob] ❌ build.gradle introuvable dans : {dist_dir}")
        return

    print(f"[Hook AdMob] 🔧 Modification de {gradle_file}")
    content = gradle_file.read_text()

    # ✅ Ajoute la dépendance AdMob si absente
    if "com.google.android.gms:play-services-ads" not in content:
        content = content.replace(
            "dependencies {",
            "dependencies {\n    implementation 'com.google.android.gms:play-services-ads:23.3.0'"
        )
        print("[Hook AdMob] ✅ Dépendance AdMob ajoutée à build.gradle")

    # ✅ Ajoute le dépôt Google si manquant
    if "google()" not in content:
        content = content.replace(
            "repositories {",
            "repositories {\n        google()"
        )
        print("[Hook AdMob] ✅ Dépôt Google ajouté dans repositories")

    gradle_file.write_text(content)
    print("[Hook AdMob] ✅ Patch terminé avec succès.")
