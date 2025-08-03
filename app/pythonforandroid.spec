[app]

title = Mon budget perso
package.name = monapp
package.domain = org.example
source.dir = .
source.main = main.py
version = 0.1
icon.filename = logo.png
presplash.filename = logo1.png
requirements=python3,kivy,kivmob,pyjnius,openpyxl,android
orientation = portrait
android.archs = armeabi-v7a
bootstrap = sdl2
android.api = 36
android.ndk = 25.2.9519653
android.permissions = INTERNET, ACCESS_NETWORK_STATE
android.gradle_dependencies = 'com.google.android.gms:play-services-ads:22.3.0'
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713
