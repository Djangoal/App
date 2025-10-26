from kivy.utils import platform

if platform == "android":
    from jnius import autoclass

class AdMobBanner:
    def __init__(self, ad_unit_id=None):
        # ID de test fourni par Google — à remplacer par ton vrai ID plus tard
        self.ad_unit_id = ad_unit_id or "ca-app-pub-3940256099942544/6300978111"
        self.banner_layout = None

    def show_banner(self, position="bottom"):
        if platform != "android":
            print("⚠️ AdMob fonctionne uniquement sur Android")
            return

        try:
            # Import des classes Java
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            AdView = autoclass("com.google.android.gms.ads.AdView")
            AdSize = autoclass("com.google.android.gms.ads.AdSize")
            AdRequestBuilder = autoclass("com.google.android.gms.ads.AdRequest$Builder")
            LinearLayout = autoclass("android.widget.LinearLayout")
            Gravity = autoclass("android.view.Gravity")

            # Récupère l’activité et la vue racine Android
            activity = PythonActivity.mActivity
            root_view = activity.getWindow().getDecorView()

            # Crée un layout pour la bannière
            banner_layout = LinearLayout(activity)
            banner_layout.setOrientation(LinearLayout.VERTICAL)

            if position == "bottom":
                banner_layout.setGravity(Gravity.BOTTOM | Gravity.CENTER_HORIZONTAL)
            elif position == "center":
                banner_layout.setGravity(Gravity.CENTER)
            else:
                banner_layout.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL)

            # Crée et configure la bannière
            ad_view = AdView(activity)
            ad_view.setAdSize(AdSize.BANNER)
            ad_view.setAdUnitId(self.ad_unit_id)

            ad_request = AdRequestBuilder().build()
            ad_view.loadAd(ad_request)
            banner_layout.addView(ad_view)

            # Ajoute la bannière à la vue principale (sur le thread UI Android)
            activity.runOnUiThread(lambda: root_view.addView(banner_layout))

            self.banner_layout = banner_layout
            print("✅ Bannière AdMob test affichée")
        except Exception as e:
            print("❌ Erreur AdMob :", e)
