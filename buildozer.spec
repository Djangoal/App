[app]
title = Mon budget perso
package.name = monbudgetperso
package.domain = org.example
source.dir = app
version = 0.1
icon.filename = logo.png
presplash.filename = app/logo1.png
orientation = portrait
fullscreen = 0
requirements = python3,kivy
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 36
android.arch = armeabi-v7a, arm64-v8a
android.minapi = 21
android.sdk = 36
android.ndk = 25b
log_level = 2

[buildozer]
warn_on_root = 0
