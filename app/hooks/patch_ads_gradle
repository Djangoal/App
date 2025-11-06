from pathlib import Path

def after_build(**kwargs):
    """
    Injecte la dépendance Google Ads dans le build.gradle final de p4a.
    Ce hook est appelé automatiquement après la génération du projet Android.
    """
    dist_dir = Path.home() / ".local/share/python-for-android/dists/monapp_release"
    gradle_file = dist_dir / "build.gradle"
    if not gradle_file.exists():
        print(f"[Hook AdMob] ❌ build.gradle non trouvé dans {dist_dir}")
        return

    content = gradle_file.read_text()
    if "play-services-ads" not in content:
        print("[Hook AdMob] ➕ Ajout de la dépendance AdMob dans build.gradle...")
        content = content.replace(
            "dependencies {",
            "dependencies {\n    implementation 'com.google.android.gms:play-services-ads:23.3.0'"
        )
        gradle_file.write_text(content)
        print("[Hook AdMob] ✅ Dépendance ajoutée avec succès.")
    else:
        print("[Hook AdMob] ✅ Dépendance déjà présente, rien à faire.")
