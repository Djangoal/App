import os
from pathlib import Path

def before_apk_build(ctx, **kwargs):
    """
    Hook exécuté juste avant la compilation de l'APK.
    Injecte AdMob (Google Ads) dans le build.gradle du projet Android généré.
    """
    dist_dir = Path.home() / ".local/share/python-for-android/dists/monapp_release"
    gradle_file = dist_dir / "build.gradle"

    if not gradle_file.exists():
        print(f"[Hook AdMob] ❌ Fichier build.gradle introuvable dans : {dist_dir}")
        return

    print(f"[Hook AdMob] 🔧 Modification de {gradle_file}")
    content = gradle_file.read_text()

    # ✅ Ajoute la dépendance Google Ads si absente
    if "com.google.android.gms:play-services-ads" not in content:
        content = content.replace(
            "dependencies {",
            "dependencies {\n    implementation 'com.google.android.gms:play-services-ads:23.3.0'"
        )
        gradle_file.write_text(content)
        print("[Hook AdMob] ✅ Dépendance AdMob ajoutée à build.gradle")
    else:
        print("[Hook AdMob] ✅ Dépendance déjà présente")

    # ✅ Ajoute le dépôt Google s’il manque
    if "google()" not in content:
        content = content.replace(
            "repositories {",
            "repositories {\n        google()"
        )
        gradle_file.write_text(content)
        print("[Hook AdMob] ✅ Dépôt Google ajouté dans repositories")

    print("[Hook AdMob] ✅ Patch terminé.")
