[app]
title = Mon budget perso
package.name = monapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1
requirements = python3,kivy
icon.filename = logo.png
presplash.filename = app/logo1.png
orientation = portrait
fullscreen = 1

# Entry point
entrypoint = main.py

# Package name for release
package.name = mon_budget_perso

# Supported architectures
arch = armeabi-v7a

# (str) Android API to use
android.api = 36

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK Build Tools version to use
android.build_tools_version = 36.0.0

# (str) Bootstrap to use (sdl2 or webview)
bootstrap = sdl2

# (list) Permissions
android.permissions = INTERNET

# (bool) Copy library instead of linking (for debugging)
copy_libs = 1

# (str) Supported orientation (portrait, landscape or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Screens to add
# e.g. landscape = 1

[buildozer]
log_level = 2
warn_on_root = 1

# (str) Path to build artifact storage (bin/, .buildozer/, etc.)
build_dir = ./.buildozer

# (bool) Should we overwrite the existing .apk
overwrite = 1
