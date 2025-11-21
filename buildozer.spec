[app]

title = Mon budget perso
package.name = monapp
package.domain = org.example

source.dir = app

icon.filename = logo.png
presplash.filename = app/logo1.png

version = 1.0

# Dépendances Python
requirements = python3, kivy==2.2.1, android, jnius, plyer, https://github.com/MichaelStott/KivMob/archive/refs/heads/master.zip

bootstrap = sdl2
orientation = portrait

# Permissions Android
android.permissions = INTERNET, ACCESS_NETWORK_STATE, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# ARCHITECTURES (important)
android.archs = armeabi-v7a, arm64-v8a

# SDK / API
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21

# Manifest personnalisé
android.manifest = app/templates/AndroidManifest.tmpl.xml

# AndroidX obligatoire
android.enable_androidx = True

# Firebase Ads (Google Ads)
android.gradle_dependencies = com.google.android.gms:play-services-ads:22.3.0

android.allow_backup = False
android.compile_options = release

android.dist_name = monapp

# Forcer APK (pas AAB)
android.bundle = False
android.release_artifacts = apk

[buildozer]
log_level = 2
warn_on_root = 0
