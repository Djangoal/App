[app]

# (str) Title of your application
title = MonAppKivy

# (str) Package name
package.name = monappkivy

# (str) Package domain (needed for android/ios packaging)
package.domain = org.monorganisation

# (str) Source code where the main.py is located
source.dir = .

# (str) Main .py file to use as the main entry point
source.main = main.py

# (list) List of inclusions using pattern matching
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (manual or automatic)
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy

# (str) Supported orientation (portrait, landscape or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 1

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Supported platforms
osx.kivy_version = 2.2.1

[buildozer]

# (str) Android SDK directory - path corrigé pour le workflow GitHub
android.sdk_path = $ANDROIDSDK

# (str) Android NDK directory (will be downloaded if empty)
# android.ndk_path =

# (str) Android entry point, default is ok
# android.entrypoint = org.kivy.android.PythonActivity

# (str) Android architecture to use
android.arch = armeabi-v7a

# (str) Android NDK API to use
android.ndk_api = 25b

# (int) Target API for Android
android.api = 31

# (str) Build tool version
android.build_tools_version = 30.0.3

# (bool) Copy library instead of making a libpymodules.so
copy_libs = 1

# (bool) Create a release APK
# android.release = 1

# (bool) Enable logcat on launch
log_level = 2

# (bool) Compress the final APK
android.packaging_mode = apk

# (str) Path to keystore file (if building signed releases)
# android.keystore = mykeystore.keystore

# (str) Custom java package
# android.java_package = org.kivy.myapp

# (bool) Indicate if the app should be signed with a debug key
android.debug = 1
