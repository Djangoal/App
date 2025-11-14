[app]

title = Mon Budget Perso
package.name = monbudgetperso
package.domain = org.example

source.dir = .
source.include_exts = py,kv,png,jpg,svg,ico,xml,json,ttf,otf,mp3,wav

version = 1.0

orientation = portrait

fullscreen = 0

# Icône
icon.filename = logo.png

# Splash facultatif
presplash.filename = app/logo1.png
presplash.keep_ratio = True
presplash.auto_scale = True

# ---- GOOGLE PLAY SERVICES + ADMOB ----
# Nécessaire pour affichage des pubs
requirements = python3,kivy,android,google-play-services,play-services-ads

android.permissions = INTERNET,ACCESS_NETWORK_STATE

# ⚠️ Mets ton vrai App ID AdMob ici :
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-XXXXXXXXXXXXXXXX~YYYYYYYYYY

# API Android testée
android.api = 33
android.minapi = 21

# Version NDK compatible
android.ndk = 25b

# Laisser Buildozer gérer automatiquement le SDK
android.sdk = 25.2.5

# ABI compatibles (64 bits obligatoire pour Play Store)
android.archs = arm64-v8a,armeabi-v7a

# Ajout d'un Manifest personnalisé
android.manifest = app/templates/AndroidManifest.tmpl.xml

# Fix build
p4a.branch = master


[buildozer]

log_level = 2
warn_on_root = 1

[dependencies]

[android]
android.enable_androidx = True
android.gradle_dependencies = com.google.android.gms:play-services-ads:22.0.0
android.additional_src = app/java

[ios]
