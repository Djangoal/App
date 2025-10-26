from kivy.utils import platform

if platform == "android":
    from jnius import autoclass

class StartAppAds:
    def __init__(self, app_id=None):
        self.app_id = app_id or "YOUR_STARTAPP_APP_ID"  # Remplace par ton vrai ID

    def show_banner(self):
        if platform != "android":
            print("⚠️ StartApp fonctionne uniquement sur Android")
            return

        try:
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            activity = PythonActivity.mActivity

            StartAppAd = autoclass("com.startapp.sdk.adsbase.StartAppAd")
            self.banner = StartAppAd(activity)
            self.banner.loadAd()
            self.banner.showAd()
            print("✅ Bannière StartApp affichée")

        except Exception as e:
            print("❌ Erreur StartApp :", e)

    def show_interstitial(self):
        if platform != "android":
            print("⚠️ StartApp fonctionne uniquement sur Android")
            return

        try:
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            activity = PythonActivity.mActivity

            StartAppAd = autoclass("com.startapp.sdk.adsbase.StartAppAd")
            interstitial = StartAppAd(activity)
            interstitial.loadAd()
            interstitial.showAd()
            print("✅ Interstitiel StartApp affiché")

        except Exception as e:
            print("❌ Erreur interstitiel StartApp :", e)