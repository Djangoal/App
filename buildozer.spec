[app]
title = Mon budget perso
package.name = monbudgetperso
package.domain = org.example
source.dir = .
version = 0.1
icon.filename = logo.png
presplash.filename = app/logo1.png
orientation = portrait
fullscreen = 0

requirements = python3,kivy

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 36
android.minapi = 21
android.ndk = 25b
android.build_tools = 36.0.0

# Accepte automatiquement les licences SDK/NDK
android.accept_sdk_license = True
android.accept_sdk_ndk_license = True
android.accept_all_sdk_licenses = True

log_level = 2

[buildozer]
warn_on_root = 0
