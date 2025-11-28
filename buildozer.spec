[app]

title = Mon budget perso
package.name = monbudgetperso
package.domain = org.example
package.version = 1.0
source.dir = ./app
source.include_exts = py,png,jpg,kv,atlas,json

# Utiliser ton icône & presplash
icon.filename = logo.png
presplash.filename = app/logo1.png

orientation = portrait
fullscreen = 0

# Utiliser SDL2 (obligatoire pour Android moderne)
bootstrap = sdl2

# ❗ MODULES KIVY/PYTHON
requirements = python3,kivy,kivmob,android,pyjnius

# ❗ INTÉGRATION ADMOB KIVMOB
android.gradle_dependencies = com.google.android.gms:play-services-ads:19.7.0

# Permet à Kivy d’utiliser le SDK Google
android.api = 35
android.minapi = 21
android.ndk = 25.2.9519653

# Pour GitHub Actions : on laisse Buildozer choisir la toolchain NDK
android.ndk_api = 21
android.sdk = 35

# Permissions obligatoires pour AdMob
android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE

# Autoriser trafic HTTP si nécessaire
android.manifest.application.android:usesCleartextTraffic = true

# Charger ton manifest personnalisé (celui que tu m'as envoyé)
android.custom_manifest = app/templates/AndroidManifest.tmpl.xml

# Pour signés DEV ou Release
android.release_artifact = apk
android.debug_artifact = apk

# Architecture(s)
android.archs = armeabi-v7a, arm64-v8a

# Compiler en debug/release sans te demander
p4a.local_recipes = ./p4a-recipes

# Activer accélération Kivy
android.enable_androidx = True


[buildozer]
warn_on_root = 0
log_level = 2
