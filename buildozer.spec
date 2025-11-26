[app]

title = Mon budget perso
package.name = monapp
package.domain = org.example

source.dir = app

icon.filename = logo.png
presplash.filename = app/logo1.png

version = 1.0

requirements = kivy==2.2.1, jnius, plyer, https://github.com/MichaelStott/KivMob/archive/refs/heads/master.zip

bootstrap = sdl2
orientation = portrait

android.permissions = INTERNET, ACCESS_NETWORK_STATE

android.archs = armeabi-v7a, arm64-v8a

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21

android.build_tools_version = 33.0.2
android.accept_sdk_license = True
android.manifest = app/templates/AndroidManifest.tmpl.xml

android.enable_androidx = True
android.gradle_dependencies = com.google.android.gms:play-services-ads:22.3.0

android.allow_backup = False

android.bundle = False
android.release_artifacts = apk

[buildozer]
log_level = 2
warn_on_root = 0
