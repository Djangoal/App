from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

class AdMobBanner(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = Window.width / 4  # Hauteur responsive

        if platform == 'android':
            self.load_admob()
        else:
            self.creer_placeholder()

    def load_admob(self):
        try:
            from jnius import autoclass, cast
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            AdView = autoclass('com.google.android.gms.ads.AdView')
            AdSize = autoclass('com.google.android.gms.ads.AdSize')
            AdRequestBuilder = autoclass('com.google.android.gms.ads.AdRequest$Builder')
            GoogleApiAvailability = autoclass('com.google.android.gms.common.GoogleApiAvailability')

            # Vérifie la présence de Google Play Services
            result = GoogleApiAvailability.getInstance().isGooglePlayServicesAvailable(PythonActivity.mActivity)
            if result != 0:
                # Services absents → placeholder
                self.creer_placeholder()
                return

            # Crée la vraie pub AdMob
            self.adView = AdView(PythonActivity.mActivity)
            self.adView.setAdSize(AdSize.BANNER)
            self.adView.setAdUnitId("ca-app-pub-3940256099942544/6300978111")  # ID test officiel
            ad_request = AdRequestBuilder().build()
            self.adView.loadAd(ad_request)

            layout = cast('android.view.ViewGroup', PythonActivity.mActivity.findViewById(0x01020002))
            layout.addView(self.adView)

        except Exception as e:
            # Si erreur, affiche placeholder
            self.creer_placeholder()

    def creer_placeholder(self):
        """Affiche un rectangle bleu simulant la bannière pour Pydroid3 ou absence de services."""
        with self.canvas.before:
            Color(0.1, 0.6, 0.9, 1)
            self.bg_rect = Rectangle(size=(Window.width, self.height), pos=self.pos)
        self.bind(size=lambda w, s: setattr(self.bg_rect, 'size', (self.width, self.height)),
                  pos=lambda w, p: setattr(self.bg_rect, 'pos', self.pos))

        label = Label(text="[AdMob Banner Placeholder]", halign='center', valign='middle', color=(1,1,1,1))
        label.bind(size=lambda instance, value: setattr(label, 'text_size', value))
        self.add_widget(label)
