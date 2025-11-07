import os
from pathlib import Path

def before_apk_build(ctx, **kwargs):
    """
    Injecte la dépendance AdMob (Google Ads)
    dans le modèle Gradle utilisé par python-for-android.
    """

    # 🔍 Recherche dynamique du modèle build.tmpl.gradle
    base = Path.home() / ".local/lib"
    gradle_template = None

    for path in base.rglob("build.tmpl.gradle"):
        if "bootstraps/sdl2" in str(path):
            gradle_template = path
            break

    if not gradle_template or not gradle_template.exists():
        print("[Hook AdMob] ❌ Fichier build.tmpl.gradle introuvable, python-for-android peut avoir changé de structure.")
        return

    print(f"[Hook AdMob] 🔧 Fichier trouvé : {gradle_template}")
    content = gradle_template.read_text()

    modified = False

    # ✅ Ajout de la dépendance AdMob
    if "play-services-ads" not in content:
        content = content.replace(
            "dependencies {",
            "dependencies {\n    implementation 'com.google.android.gms:play-services-ads:23.3.0'"
        )
        modified = True
        print("[Hook AdMob] ✅ Dépendance AdMob ajoutée au modèle Gradle")
    else:
        print("[Hook AdMob] ℹ️ Dépendance déjà présente")

    # ✅ Ajout du dépôt Google si manquant
    if "google()" not in content:
        content = content.replace(
            "repositories {",
            "repositories {\n        google()"
        )
        modified = True
        print("[Hook AdMob] ✅ Dépôt Google ajouté")
    else:
        print("[Hook AdMob] ℹ️ Dépôt Google déjà présent")

    if modified:
        gradle_template.write_text(content)
        print("[Hook AdMob] 💾 Modifications sauvegardées avec succès")
    else:
        print("[Hook AdMob] 👍 Aucune modification nécessaire — tout est déjà en place")

    print("[Hook AdMob] ✅ Patch terminé avec succès.")
