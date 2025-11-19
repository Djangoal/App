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
requirements = python3,kivy,android

# Bootstrap (tu l'utilises déjà)
bootstrap = sdl2

# Orientation
orientation = portrait

# Permissions
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET, ACCESS_NETWORK_STATE

# API, SDK, NDK
android.api = 35
android.minapi = 21
android.sdk = 35
android.ndk = 25b
android.ndk_path = ./android-sdk/ndk/25.2.9519653

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

# Options supplémentaires python-for-android
android.allow_backup = False
android.compile_options = release

# Nom du dossier dist (p4a override déjà, donc juste neutre)
android.dist_name = monapp

# Pas d’ads, pas de modules externes
android.gradle_dependencies =

# --- FIN APP CONFIG ---


[buildozer]

log_level = 2

# Empêche les reconstructions inutiles en local
warn_on_root = 1
