from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.graphics import Color, Rectangle

try:
    from jnius import autoclass
except ImportError:
    autoclass = None


class AdMobBanner(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 600  # Hauteur plus visible

        # 🎨 fond coloré
        with self.canvas.before:
            Color(0.2, 0.6, 1, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        if platform == 'android' and autoclass:
            try:
                self.load_banner()
            except Exception:
                # ➕ message discret si la pub ne peut pas se charger
                self.add_widget(Label(
                    text="📢 [Espace pub AdMob test – mode simulation]",
                    size_hint_y=None,
                    height=50,
                    color=(1, 1, 1, 1),
                    font_size='18sp'
                ))
        else:
            # ✅ Mode test (Pydroid3 ou PC)
            self.add_widget(Label(
                text="📢 [Espace pub AdMob test – mode simulation]",
                size_hint_y=None,
                height=50,
                color=(1, 1, 1, 1),
                font_size='18sp'
            ))

    def _update_rect(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def load_banner(self):
        # Import des classes Google Ads (Android uniquement)
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        AdView = autoclass('com.google.android.gms.ads.AdView')
        AdSize = autoclass('com.google.android.gms.ads.AdSize')
        AdRequest = autoclass('com.google.android.gms.ads.AdRequest')

        activity = PythonActivity.mActivity

        ad_view = AdView(activity)
        ad_view.setAdSize(AdSize.BANNER)
        ad_view.setAdUnitId("ca-app-pub-3940256099942544/6300978111")  # ✅ ID test officiel

        ad_request = AdRequest.Builder().build()
        ad_view.loadAd(ad_request)

        self.add_widget(Label(
            text="[AdMob Banner Initialized]",
            size_hint_y=None,
            height=50,
            color=(1, 1, 1, 1)
        ))