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
android.permissions = INTERNET

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) Application requirements
requirements = python3,kivy

# (str) Custom source folders for requirements
# (Separate multiple paths with commas)
# requirements.source =

# (str) Android NDK API to use (must be set to 34)
android.api = 36
android.minapi = 21
android.build_tools_version = 36.0.0

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK version to use (optional, match api)
android.sdk = 34

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, supported themes: 'light', 'dark'
android.theme = light

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported Android architectures
android.archs = armeabi-v7a, arm64-v8a

# (bool) Copy library instead of making a libpymodules.so
copy_libs = 1

# (bool) Enable AndroidX support. Enable when using native android dependencies
android.enable_androidx = True

# (str) Bootstrap to use for android builds (python3, sdl2 or webview)
android.bootstrap = sdl2

# (str) Directory to store the APK
bin.dir = bin

# (str) Directory to store the buildozer spec file
buildozer.dir = .

# (str) Path to buildozer requirements (e.g. for shared modules)
# buildozer.requirements.path =

# (str) Package version
version = 1.0

# (str) Application version code (used in Android)
android.version_code = 1

# (str) Application version (used in Android)
android.version_name = 1.0

# (str) Command to run before packaging (e.g. clean up, generate assets)
# before_build =

# (str) Command to run after packaging
# after_build =
