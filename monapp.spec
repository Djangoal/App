[app]

# Nom de l'application
title = Mon budget perso

# Nom du package (doit être unique, format inversé de domaine)
package.name = monapp
package.domain = org.example

# Répertoire contenant ton code principal (main.py doit s’y trouver)
source.dir = ./app

# Fichier d'entrée principal
source.main = main.py

# Icône et écran de chargement (optionnels mais recommandés)
icon.filename = logo.png
presplash.filename = app/logo1.png

# Version de ton application
version = 0.1

# Orientation de l’écran
orientation = portrait

# Modules Python requis
requirements = python3,kivy,setuptools,certifi

# Architectures cibles (32 bits + 64 bits ARM)
archs = armeabi-v7a, arm64-v8a

# Nom de la distribution (utile pour le cache entre builds)
dist_name = monapp

# Mode debug (False pour release final)
debug = 1

# Inclure les fichiers de données supplémentaires (optionnel)
# source.include_exts = py,png,jpg,kv,atlas,json

# Pour éviter les erreurs avec certaines dépendances
android.api = 36
android.minapi = 21
android.ndk = 25b
android.ndk_path = ./android-sdk/ndk/25.2.9519653
android.sdk_path = ./android-sdk

# Bootstrap utilisé
bootstrap = sdl2

# Permissions Android (ajoute-en d'autres si besoin)
android.permissions = INTERNET
