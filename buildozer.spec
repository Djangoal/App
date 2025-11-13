[app]
# (nom de l'application)
title = Mon budget perso

# (nom du package)
package.name = monapp

# (nom complet du package Java)
package.domain = org.example

# (version)
version = 0.1

# (source du code)
source.dir = app

# (icône)
icon.filename = logo.png

# (écran de démarrage)
presplash.filename = app/logo1.png

# (bootstrap utilisé)
bootstrap = sdl2

# (orientation)
orientation = portrait

# (permissions Android)
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET,ACCESS_NETWORK_STATE

# (modules Python requis)
requirements = python3,kivy,android

# (architecture à compiler)
android.archs = armeabi-v7a, arm64-v8a

# (SDK et NDK)
android.api = 35
android.minapi = 21
android.sdk = 35
android.ndk = 25b

# (nom du répertoire de distribution p4a)
dist_name = monapp

# (nom de la fenêtre sur desktop, facultatif)
fullscreen = 0

# (métadonnée AdMob)
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

# (ajout des AAR Google Play Services)
android.add_aar = app/libs/play-services-basement-18.5.0.aar, app/libs/play-services-tasks-18.3.2.aar, app/libs/play-services-ads-24.3.0.aar

# (si tu veux inclure un manifeste personnalisé)
android.manifest = app/templates/AndroidManifest.tmpl.xml

# (nom de la sortie finale)
android.release_artifact = mon_budget_perso_release.apk
android.debug_artifact = mon_budget_perso_debug.apk

# (support du stockage interne)
android.allow_backup = True

# (version du NDK explicitement utilisée)
android.ndk_path = ~/android-sdk/ndk/25.2.9519653

# (nom d’affichage)
title = Mon budget perso

# (exécution du code principal)
entrypoint = main.py

# (autoriser le multitouch)
android.enable_legacy_external_storage = True

# (support des écrans)
android.presplash_color = #FFFFFF


[buildozer]
# (chemin du SDK)
android.sdk_path = ~/android-sdk

# (chemin du NDK)
android.ndk_path = ~/android-sdk/ndk/25.2.9519653

# (répertoire du SDK tools)
android.accept_sdk_license = True

# (outil de compilation)
log_level = 2

# (répertoires temporaires)
build_dir = .buildozer
bin_dir = bin

# (utiliser le mode release ou debug)
# buildozer android debug
# ou
# buildozer android release

# (auto)
warn_on_root = 1
