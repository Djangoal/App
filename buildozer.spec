[app]
title = MonBudget
package.name = monbudget
package.domain = org.kivy
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 33
android.ndk = 23b
android.sdk = 24
# Ne pas utiliser ndk_path ou sdk_path ici sur GitHub
