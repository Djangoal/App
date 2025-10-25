# ads.py
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass

class AdMobBanner:
    def __init__(self, ad_unit_id=None):
        # ID de test officiel Google AdMob (bannière)
        self.ad_unit_id = ad_unit_id or "ca-app-pub-3940256099942544/6300978111"
        self.banner = None

    def show_banner(self, position="bottom"):
        """Affiche une bannière AdMob (test) à la position choisie : top / center / bottom."""
        if platform != 'android':
            print("⚠️ AdMob fonctionne uniquement sur Android (aucune bannière affichée).")
            return

        try:
            # Import des classes Java nécessaires
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            AdView = autoclass('com.google.android.gms.ads.AdView')
            AdSize = autoclass('com.google.android.gms.ads.AdSize')
            AdRequestBuilder = autoclass('com.google.android.gms.ads.AdRequest$Builder')
            LinearLayout = autoclass('android.widget.LinearLayout')
            Gravity = autoclass('android.view.Gravity')

            activity = PythonActivity.mActivity
            layout = activity.findViewById(0x01020002)  # layout principal
            banner_layout = LinearLayout(activity)
            banner_layout.setOrientation(LinearLayout.VERTICAL)

            # Position de la bannière
            if position == "bottom":
                banner_layout.setGravity(Gravity.BOTTOM | Gravity.CENTER_HORIZONTAL)
            elif position == "center":
                banner_layout.setGravity(Gravity.CENTER)
            else:
                banner_layout.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL)

            # Création de la bannière
            ad_view = AdView(activity)
            ad_view.setAdSize(AdSize.SMART_BANNER)
            ad_view.setAdUnitId(self.ad_unit_id)

            # Chargement de la pub de test
            ad_request = AdRequestBuilder().build()
            ad_view.loadAd(ad_request)

            # Ajout à la vue Android
            banner_layout.addView(ad_view)
            layout.addView(banner_layout)

            self.banner = ad_view
            print(f"✅ Bannière AdMob (test) affichée en {position}")

        except Exception as e:
            print("❌ Erreur lors de l’affichage de la bannière AdMob :", e)

    def hide_banner(self):
        """Masque la bannière actuelle."""
        if platform != 'android' or not self.banner:
            print("ℹ️ Aucune bannière à masquer.")
            return

        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            layout = activity.findViewById(0x01020002)
            layout.removeView(self.banner)
            self.banner = None
            print("🧹 Bannière masquée avec succès")
        except Exception as e:
            print("❌ Erreur lors du masquage de la bannière :", e)
