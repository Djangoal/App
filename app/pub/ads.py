from kivy.utils import platform

if platform == "android":
    from jnius import autoclass, cast

class AdMobBanner:
    def __init__(self, ad_unit_id=None):
        self.ad_unit_id = ad_unit_id or "ca-app-pub-3940256099942544/6300978111"
        self.banner = None

    def show_banner(self, position="bottom"):
        if platform != "android":
            print("⚠️ AdMob fonctionne uniquement sur Android")
            return
        try:
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            AdView = autoclass("com.google.android.gms.ads.AdView")
            AdSize = autoclass("com.google.android.gms.ads.AdSize")
            AdRequestBuilder = autoclass("com.google.android.gms.ads.AdRequest$Builder")
            LinearLayout = autoclass("android.widget.LinearLayout")
            Gravity = autoclass("android.view.Gravity")

            activity = PythonActivity.mActivity
            root_view = activity.getWindow().getDecorView().findViewById(0x01020002)

            banner_layout = LinearLayout(activity)
            banner_layout.setOrientation(LinearLayout.VERTICAL)

            if position == "bottom":
                banner_layout.setGravity(Gravity.BOTTOM | Gravity.CENTER_HORIZONTAL)
            elif position == "center":
                banner_layout.setGravity(Gravity.CENTER)
            else:
                banner_layout.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL)

            ad_view = AdView(activity)
            ad_view.setAdSize(AdSize.SMART_BANNER)
            ad_view.setAdUnitId(self.ad_unit_id)

            ad_request = AdRequestBuilder().build()
            ad_view.loadAd(ad_request)

            banner_layout.addView(ad_view)
            root_view.addView(banner_layout)
            print("✅ Bannière test affichée")

        except Exception as e:
            print("❌ Erreur AdMob :", e)
