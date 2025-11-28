from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.uix.label import Label

try:
    from kivmob import KivMob
except ImportError:
    KivMob = None


class AdMobBanner(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint_y = None
        self.height = 60
        self.orientation = "vertical"

        # Mode Android uniquement
        if platform == "android" and KivMob:
            try:
                self.load_banner()
            except Exception as e:
                self.add_widget(Label(
                    text=f"[Erreur pub] {e}",
                    size_hint_y=None,
                    height=50,
                    color=(1, 0.2, 0.2, 1)
                ))
        else:
            # Mode PC ou Pydroid3 → simulation
            self.add_widget(Label(
                text="📢 [Zone pub – simulation]",
                size_hint_y=None,
                height=50,
                color=(1, 1, 1, 1)
            ))

    def load_banner(self):
        # ⚠️ ID APP TEST OFFICIEL
        self.ads = KivMob("ca-app-pub-3940256099942544~3347511713")

        # ⚠️ BANNIÈRE TEST OFFICIELLE (fonctionne parfaitement)
        banner_id = "ca-app-pub-3940256099942544/6300978111"

        # Crée une bannière ↓ en bas ↓
        self.ads.new_banner(banner_id, top_pos=False)
        
        # Charge la bannière
        self.ads.request_banner()

        # Affiche la bannière
        self.ads.show_banner()
