[app]

# Infos de l'application
title = Mon budget perso
package.name = monapp
package.domain = org.example

source.dir = app
icon.filename = logo.png
presplash.filename = app/logo1.png
version = 1.0

# Librairies Python requises
requirements = kivy==2.2.1, kivmob, jnius, plyer, python3, android

bootstrap = sdl2
orientation = portrait

# Permissions Android
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# Architectures supportées
android.archs = armeabi-v7a, arm64-v8a

# Versions Android / SDK / NDK
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21
android.build_tools_version = 33.0.2
android.accept_sdk_license = True

# Manifest et compatibilité
android.manifest = app/templates/AndroidManifest.tmpl.xml
android.enable_androidx = False
android.allow_backup = False

# Dépendances Gradle pour Ads (KivMob compatible)

# Génération APK
android.bundle = False
android.release_artifacts = apk

[buildozer]
log_level = 2
warn_on_root = 0
