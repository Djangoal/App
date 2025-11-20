[app]

# Nom affiché sur Android
title = Mon budget perso

# Nom du package interne
package.name = monapp
package.domain = org.example

# Chemin vers ton dossier source
source.dir = app

# Icone et splash
icon.filename = logo.png
presplash.filename = app/logo1.png

# Version
version = 1.0

# Dépendances Python
requirements = python3, kivy==2.2.1, android, jnius, https://github.com/MichaelStott/KivMob/archive/refs/heads/master.zip

# Bootstrap Kivy
bootstrap = sdl2

# Orientation
orientation = portrait

# Permissions Android
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET, ACCESS_NETWORK_STATE

# SDK / API
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21

# Manifest personnalisé
android.manifest = app/templates/AndroidManifest.tmpl.xml

# Signature AUTOMATIQUE (compatible GitHub Secrets)
android.signing_key = release.keystore
android.signing_key_password = {env:KEYSTORE_PASSWORD}
android.keyalias = {env:KEY_ALIAS}
android.keyalias_password = {env:KEY_ALIAS_PASSWORD}

# Activer AndroidX
android.enable_androidx = True

# Accepter licences SDK
android.accept_sdk_license = True

# Options supplémentaires
android.allow_backup = False
android.compile_options = release

# Nom du dossier dist
android.dist_name = monapp

# Firebase Ads
android.gradle_dependencies = com.google.firebase:firebase-ads:21.4.0

# Build final : APK + AAB
android.release_artifacts = aab, apk


[buildozer]
log_level = 2
warn_on_root = 0
