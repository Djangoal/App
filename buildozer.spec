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
requirements = python3,kivy==2.2.1

# (str) Supported orientation (portrait, landscape or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 1

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Supported platforms
osx.kivy_version = 2.2.1

[buildozer]

# (int) Target API for Android
android.api = 31

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android SDK Build Tools version to use
android.build_tools_version = 31.0.0

# (str) Android NDK version to use
android.ndk = 23b

# (str) Android architecture to use
android.arch = armeabi-v7a

# (bool) Copy library instead of making a libpymodules.so
copy_libs = 1

# (bool) Enable logcat on launch
log_level = 2

# (bool) Compress the final APK
android.packaging_mode = apk

# (bool) Indicate if the app should be signed with a debug key
android.debug = 1
