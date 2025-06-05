[app]

# (autres paramètres de ton app à compléter ci-dessous)

title = MonApp
package.name = monapp
package.domain = org.monorganisation
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 1

[buildozer]

log_level = 2
warn_on_root = 1

[app]

# --- APIs Android strictement fixées à 34 ---
android.api = 34
android.minapi = 34
android.ndk_api = 34

# --- NDK recommandé compatible ---
android.ndk = 23b

# --- Architecture ---
android.archs = armeabi-v7a, arm64-v8a

# --- Permissions (exemple à adapter) ---
android.permissions = INTERNET

# --- SDK dir personnalisé si besoin ---
# android.sdk_path = /chemin/vers/android-sdk

# --- NDK dir personnalisé si besoin ---
# android.ndk_path = /chemin/vers/android-ndk

# --- Enlever les splash screens si non nécessaires ---
# android.presplash_color = #FFFFFF

# --- Supprimer si non utilisé ---
# android.enable_androidx = 1
