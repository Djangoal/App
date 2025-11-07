import os
from pathlib import Path

def before_apk_build(ctx, **kwargs):
    """
    Injecte AdMob directement dans le modèle Gradle de python-for-android
    AVANT la génération du projet Android.
    """
    base = Path.home() / ".local/lib"
    candidates = list(base.glob("python*/site-packages/pythonforandroid/bootstraps/sdl2/build.tmpl.gradle"))

    if not candidates:
        print("[Hook AdMob] ❌ Impossible de trouver build.tmpl.gradle")
        return

    gradle_template = candidates[0]
    content = gradle_template.read_text()

    # ✅ Ajoute la dépendance Ads
    if "play-services-ads" not in content:
        print("[Hook AdMob] ✅ Injection de la dépendance Google Ads dans build.tmpl.gradle")
        content = content.replace(
            "dependencies {",
            "dependencies {\n    implementation 'com.google.android.gms:play-services-ads:23.3.0'"
        )
        gradle_template.write_text(content)
    else:
        print("[Hook AdMob] ℹ️ Dépendance Ads déjà présente")

    # ✅ Ajoute le dépôt Google si manquant
    if "google()" not in content:
        print("[Hook AdMob] ✅ Ajout du dépôt Google() dans repositories")
        content = content.replace(
            "repositories {",
            "repositories {\n        google()"
        )
        gradle_template.write_text(content)
    else:
        print("[Hook AdMob] ℹ️ Dépôt google() déjà présent")

    print(f"[Hook AdMob] ✅ Patch terminé sur {gradle_template}")
