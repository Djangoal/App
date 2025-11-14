[app]

# Nom et package
title = Mon Budget Perso
package.name = monbudgetperso
package.domain = org.example

# Source
source.dir = app
source.main = main.py
source.include_exts = py,kv,png,jpg,svg,ico,xml,json,ttf,otf,mp3,wav

# Version et affichage
version = 1.0
orientation = portrait
fullscreen = 0

# Icône et splash
icon.filename = logo.png
presplash.filename = app/logo1.png
presplash.keep_ratio = True
presplash.auto_scale = True

# Dépendances et AdMob
requirements = python3,kivy,android,google-play-services,play-services-ads
android.permissions = INTERNET,ACCESS_NETWORK_STATE
# ID test officiel AdMob (pour éviter rejet Play Store)
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

# API et NDK
android.api = 33
android.minapi = 21
android.ndk = 23b
android.archs = arm64-v8a,armeabi-v7a

# Manifest personnalisé
android.manifest = app/templates/AndroidManifest.tmpl.xml
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
# Toujours utiliser venv local
use_venv = True

[android]
# AndroidX et dépendances Gradle
android.enable_androidx = True
android.gradle_dependencies = com.google.android.gms:play-services-ads:22.0.0
android.additional_src = app/java

[ios]
