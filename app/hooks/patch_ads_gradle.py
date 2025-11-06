import os
import time
from pathlib import Path

def after_apk_build(ctx, **kwargs):
    """
    Hook exécuté juste après la génération du projet Android.
    Injecte la dépendance AdMob (Google Ads) dans le build.gradle.
    """
    dist_dir = Path.home() / ".local/share/python-for-android/dists/monapp_release"
    gradle_file = dist_dir / "build.gradle"

    # 🕒 Attente de la création du fichier
    for _ in range(30):
        if gradle_file.exists():
            break
        print("[Hook AdMob] ⏳ build.gradle introuvable, attente...")
        time.sleep(1)
    else:
        print(f"[Hook AdMob] ❌ Fichier build.gradle introuvable dans : {dist_dir}")
        return

    print(f"[Hook AdMob] 🔧 Modification de {gradle_file}")
    content = gradle_file.read_text()

    # ✅ Ajoute la dépendance Google Ads
    if "com.google.android.gms:play-services-ads" not in content:
        content = content.replace(
            "dependencies {",
            "dependencies {\n    implementation 'com.google.android.gms:play-services-ads:23.3.0'"
        )
        print("[Hook AdMob] ✅ Dépendance AdMob ajoutée à build.gradle")

    # ✅ Ajoute le dépôt Google s’il manque
    if "google()" not in content:
        content = content.replace(
            "repositories {",
            "repositories {\n        google()"
        )
        print("[Hook AdMob] ✅ Dépôt Google ajouté dans repositories")

    gradle_file.write_text(content)
    print("[Hook AdMob] ✅ Patch terminé avec succès.")
