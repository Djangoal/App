import os
import time
from pathlib import Path

def after_apk_build(ctx, **kwargs):
    print("[Hook AdMob] 🚀 Lancement du patch pour ajouter Google Ads...")

    # Chemin du dossier de distribution (dist)
    dist_dir = Path.home() / ".local/share/python-for-android/dists/monapp_release"
    build_gradle = dist_dir / "build.gradle"

    # Attente que le build.gradle soit généré
    for _ in range(30):  # 30 tentatives = ~30 secondes
        if build_gradle.exists():
            break
        print("[Hook AdMob] ⏳ build.gradle non trouvé, nouvelle tentative...")
        time.sleep(1)
    else:
        print(f"[Hook AdMob] ❌ Fichier build.gradle introuvable dans : {dist_dir}")
        return

    print(f"[Hook AdMob] 🎯 Fichier détecté : {build_gradle}")
    content = build_gradle.read_text()

    # Ajout du dépôt Google
    if "google()" not in content:
        content = content.replace("repositories {", "repositories {\n        google()")
        print("[Hook AdMob] ✅ Dépôt Google ajouté")

    # Ajout de la dépendance Google Ads
    if "com.google.android.gms:play-services-ads" not in content:
        content = content.replace(
            "dependencies {",
            "dependencies {\n    implementation 'com.google.android.gms:play-services-ads:23.3.0'"
        )
        print("[Hook AdMob] ✅ Dépendance Ads ajoutée")

    build_gradle.write_text(content)
    print("[Hook AdMob] ✅ Patch appliqué avec succès ✅")
