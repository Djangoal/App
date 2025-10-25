# ads.py nouveau
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass, cast

class AdMobBanner:
    def __init__(self, ad_unit_id=None):
        self.ad_unit_id = ad_unit_id or "ca-app-pub-3940256099942544/6300978111"
        self.banner = None

    def show_banner(self):
        if platform != 'android':
            print("⚠️ AdMob fonctionne uniquement sur Android.")
            return

        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            AdView = autoclass('com.google.android.gms.ads.AdView')
            AdSize = autoclass('com.google.android.gms.ads.AdSize')
            AdRequestBuilder = autoclass('com.google.android.gms.ads.AdRequest$Builder')
            LinearLayout = autoclass('android.widget.LinearLayout')
            Gravity = autoclass('android.view.Gravity')

            activity = PythonActivity.mActivity
            # Récupère la racine SDL2
            decorView = activity.getWindow().getDecorView()
            layout = LinearLayout(activity)
            layout.setOrientation(LinearLayout.VERTICAL)

            # Création de la bannière
            ad_view = AdView(activity)
            ad_view.setAdSize(AdSize.BANNER)
            ad_view.setAdUnitId(self.ad_unit_id)

            # Chargement de la pub de test
            ad_request = AdRequestBuilder().build()
            ad_view.loadAd(ad_request)

            # Layout de la bannière en bas
            banner_layout = LinearLayout(activity)
            banner_layout.setOrientation(LinearLayout.VERTICAL)
            banner_layout.setGravity(Gravity.BOTTOM | Gravity.CENTER_HORIZONTAL)
            banner_layout.addView(ad_view)

            # Ajouter le banner layout au layout principal
            layout.addView(banner_layout)
            # Remplacer le contenu de l'activité SDL2
            activity.setContentView(layout)

            self.banner = ad_view
            print("✅ Bannière AdMob affichée.")

        except Exception as e:
            print("❌ Erreur AdMob :", e)

    def hide_banner(self):
        if platform != 'android' or not self.banner:
            return
        try:
            self.banner.setVisibility(8)  # GONE
            self.banner = None
            print("🧹 Bannière masquée.")
        except Exception as e:
            print("❌ Erreur lors du masquage :", e)
