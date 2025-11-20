[app]

# Nom affiché sur Android
title = Mon budget perso

# Nom du package interne
package.name = monapp
package.domain = org.example

# Chemin des sources Python
source.dir = app

# Icônes et splash
icon.filename = logo.png
presplash.filename = app/logo1.png

# Version
version = 1.0

# App requirements
requirements = python3, kivy==2.2.1, android, jnius, https://github.com/MichaelStott/KivMob/archive/refs/heads/master.zip

# Bootstrap (tu l'utilises déjà)
bootstrap = sdl2

# Orientation
orientation = portrait

# Permissions
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET, ACCESS_NETWORK_STATE

# API, SDK, NDK
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21

# ARCH (debug utilise armeabi-v7a, release arm64 — ton workflow gère ça)
# buildozer.spec doit accepter les deux
android.archs = armeabi-v7a, arm64-v8a

# Manifest custom → EXACTEMENT ce que ton workflow fait
android.manifest = app/templates/AndroidManifest.tmpl.xml

# Pas d'autosignature → tu signes toi-même plus tard
android.release_keystore =
android.release_keystore_pass =
android.release_keyalias =
android.release_keyalias_pass =
# AndroidX
android.enable_androidx = True



# Accept all SDK licenses automatically
android.accept_sdk_license = True
# Options supplémentaires python-for-android
android.allow_backup = False
android.compile_options = release

# Nom du dossier dist (p4a override déjà, donc juste neutre)
android.dist_name = monapp

# Pas d’ads, pas de modules externes
# Firebase Ads
android.gradle_dependencies = com.google.firebase:firebase-ads:21.4.0

android.release_artifacts = aab,apk

[buildozer]

log_level = 2

# Empêche les reconstructions inutiles en local
warn_on_root = 0
