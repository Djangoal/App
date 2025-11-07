import os
from pathlib import Path

def before_apk_build(ctx, **kwargs):
    """
    Injecte AdMob (Google Ads) dans le modèle Gradle utilisé par python-for-android.
    Compatible avec les nouvelles versions utilisant gradle.build.template.
    """
    base = Path.home() / ".local/lib"
    gradle_template = None

    # 🔍 Recherche étendue (nouveaux modèles Gradle)
    for path in base.rglob("*gradle*.template"):
        if "bootstraps" in str(path) and path.suffix in [".template", ".gradle"]:
            gradle_template = path
            break

    if not gradle_template or not gradle_template.exists():
        print("[Hook AdMob] ❌ Aucun modèle Gradle trouvé (build.tmpl.gradle ou gradle.build.template)")
        return

    print(f"[Hook AdMob] 🔧 Modèle Gradle détecté : {gradle_template}")
    content = gradle_template.read_text(encoding="utf-8")

    modified = False

    # ✅ Ajout de la dépendance Google Ads
    if "play-services-ads" not in content:
        content = content.replace(
            "dependencies {",
            "dependencies {\n    implementation 'com.google.android.gms:play-services-ads:23.3.0'"
        )
        modified = True
        print("[Hook AdMob] ✅ Dépendance AdMob ajoutée au modèle")

    # ✅ Ajout du dépôt Google si manquant
    if "google()" not in content:
        content = content.replace(
            "repositories {",
            "repositories {\n        google()"
        )
        modified = True
        print("[Hook AdMob] ✅ Dépôt Google ajouté")

    if modified:
        gradle_template.write_text(content, encoding="utf-8")
        print("[Hook AdMob] 💾 Modifications appliquées avec succès")
    else:
        print("[Hook AdMob] 👍 Modèle déjà configuré correctement")

    print("[Hook AdMob] ✅ Injection terminée avec succès")
