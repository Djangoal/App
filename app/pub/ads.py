# ads.py
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass

class AdMobBanner:
    def __init__(self, ad_unit_id=None):
        """
        Classe pour afficher un bandeau AdMob (test ou réel).
        ad_unit_id: ID de la bannière. Par défaut, ID de test officiel Google.
        """
        self.ad_unit_id = ad_unit_id or "ca-app-pub-3940256099942544/6300978111"
        self.banner = None

    def show_banner(self, position="bottom"):
        """Affiche une bannière AdMob à la position choisie : top / center / bottom."""
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

            # Récupération de l'activité et du layout principal
            activity = PythonActivity.mActivity
            layout = activity.findViewById(0x01020002)  # android.R.id.content
            if layout is None:
                print("❌ Layout principal introuvable, impossible d'ajouter la bannière.")
                return

            # Création d'un LinearLayout pour la bannière
            banner_layout = LinearLayout(activity)
            banner_layout.setOrientation(LinearLayout.VERTICAL)

            # Position
            if position == "bottom":
                banner_layout.setGravity(Gravity.BOTTOM | Gravity.CENTER_HORIZONTAL)
            elif position == "center":
                banner_layout.setGravity(Gravity.CENTER)
            else:
                banner_layout.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL)

            # Création de la bannière
            ad_view = AdView(activity)
            ad_view.setAdSize(AdSize.BANNER)  # BANNIÈRE standard compatible
            ad_view.setAdUnitId(self.ad_unit_id)

            # Chargement de la pub
            ad_request = AdRequestBuilder().build()
            ad_view.loadAd(ad_request)
            print("📢 AdMob: requête de pub lancée")

            # Ajout au layout Android
            banner_layout.addView(ad_view)
            layout.addView(banner_layout)

            self.banner = ad_view
            print(f"✅ Bannière AdMob affichée en {position}")

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
