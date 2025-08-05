[app]
# Nom de l'app
title = Mon budget perso
package.name = monapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 1
entrypoint = main.py
icon.filename = logo.png
presplash.filename = app/logo1.png

# Architecture Android ciblée
arch = armeabi-v7a

# API Android et outils
android.api = 36
android.minapi = 21
android.ndk = 25b
android.sdk = 24.4.1
android.ndk_path =
android.sdk_path =
android.build_tools_version = 36.0.0

# Résolution des erreurs AIDL
android.accept_sdk_license = True
android.accept_sdk_license_again = True

# Permissions par défaut
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
