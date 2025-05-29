[app]
title = MonApp
package.name = monapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 1
osx.python_version = 3
osx.kivy_version = 2.1.0
icon.filename = %(source.dir)s/icon.png
permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1

[python]
# (Optionnel) encodage
# utf8_string_encoding = 1

[android]
android.api = 33
android.sdk = 24
android.ndk = 23b
android.ndk_path = 
android.sdk_path = 
# Indique à buildozer d'utiliser le SDK déjà installé via GitHub Actions
android.accept_sdk_license = True
android.minapi = 21
android.permissions = INTERNET

# Architecture cible (arm64-v8a est recommandée pour les appareils récents)
android.arch = arm64-v8a

# (Optionnel) pour signer automatiquement l’APK release
# release.keystore = my.keystore
# release.keystore_pass = mypass
# release.keyalias = myalias
# release.keyalias_pass = mypass

[android.packaging_args]
# Pour éviter certaines erreurs de compression
# (utile si tu as des fichiers .so ou .dll)
# --ignore-assets=public/assets/*

[android.gradle_dependencies]
# Laisse vide sauf si tu ajoutes Firebase ou des libs Android spécifiques

[ios]
# Tu peux laisser par défaut

[buildozer.android]
# Déconseillé, laisse vide sauf si besoin spécifique
