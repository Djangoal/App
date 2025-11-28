from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.graphics import Color, Line

try:
    from kivmob import KivMob
except ImportError:
    KivMob = None

class AdMobBanner(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from kivy.core.window import Window
        self.height = int(Window.height * 0.08)
        self.size_hint_y = None
        self.orientation = "vertical"

        # Encadrement visible
        with self.canvas.before:
            Color(0, 0, 0, 1)  # noir
            self.border = Line(width=2, rectangle=(self.x, self.y, self.width, self.height))
        self.bind(pos=self.update_border, size=self.update_border)

        # Fallback PC
        if platform != "android" or KivMob is None:
            self.add_widget(Label(
                text="📢 [Zone pub – simulation]",
                size_hint_y=None,
                height=50,
                color=(0,0,0,1)
            ))

        self.ads = None
        self.banner_loaded = False

    def update_border(self, *args):
        self.border.rectangle = (self.x, self.y, self.width, self.height)

    def load_banner(self):
        if self.banner_loaded or platform != "android" or KivMob is None:
            return
        self.banner_loaded = True
        try:
            self.ads = KivMob("ca-app-pub-3940256099942544~3347511713")
            banner_id = "ca-app-pub-3940256099942544/6300978111"
            self.ads.new_banner(banner_id, top_pos=False)
            self.ads.request_banner()
            self.ads.show_banner()
        except Exception as e:
            self.clear_widgets()
            self.add_widget(Label(
                text=f"[Erreur AdMob] {e}",
                size_hint_y=None,
                height=50,
                color=(0,0,0,1)
            ))
