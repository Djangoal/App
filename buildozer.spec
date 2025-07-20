[app]
# (str) Title of your application
title = Mon budget perso

# (str) Package name
package.name = monapp

# (str) Package domain (unique, usually your own domain)
package.domain = org.example

# (str) Source code where the main.py lives
source.dir = .

# (str) Main .py file to use as the main entry point for your app
source.main = main.py

# (list) Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# Ajout dans le manifeste pour MANAGE_EXTERNAL_STORAGE (Android 11+)
android.extra_manifest_kv = <uses-permission android:name="android.permission.MANAGE_EXTERNAL_STORAGE"/>

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) Application requirements
requirements = python3,kivy

# (str) Android NDK API to use
android.api = 36
android.minapi = 21
android.build_tools_version = 36.0.0

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK version to use
android.sdk = 34

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, supported themes: 'light', 'dark'
android.theme = light

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# ✅ Supprimer l'écran de lancement Kivy
android.presplash_path = 
android.presplash_color = #FFFFFF

# (str) Supported Android architectures
android.archs = armeabi-v7a, arm64-v8a

# (bool) Copy library instead of making a libpymodules.so
copy_libs = 1

# (bool) Enable AndroidX support. Enable when using native android dependencies
android.enable_androidx = True

# (str) Bootstrap to use for android builds
android.bootstrap = sdl2

# (str) Directory to store the APK
bin.dir = bin

# (str) Directory to store the buildozer spec file
buildozer.dir = .

# (str) Package version
version = 1.0

# (str) Application version code (used in Android)
android.version_code = 1

# (str) Application version (used in Android)
android.version_name = 1.0
