[app]

title = Mon Budget Perso
package.name = monbudgetperso
package.domain = org.example

source.dir = app
source.main = main.py
source.include_exts = py,kv,png,jpg,svg,ico,xml,json,ttf,otf,mp3,wav

version = 1.0
orientation = portrait
fullscreen = 0

icon.filename = logo.png
presplash.filename = app/logo1.png
presplash.keep_ratio = True
presplash.auto_scale = True

requirements = python3,kivy,android,google-play-services,play-services-ads
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-XXXXXXXXXXXXXXXX~YYYYYYYYYY

android.api = 33
android.minapi = 21
android.ndk = 23b
android.archs = arm64-v8a,armeabi-v7a
android.manifest = app/templates/AndroidManifest.tmpl.xml
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.enable_androidx = True
android.gradle_dependencies = com.google.android.gms:play-services-ads:22.0.0
android.additional_src = app/java

[ios]
