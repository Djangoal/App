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

        self.ads = None
        self.banner_loaded = False

        # ---------------------
        # Encadrement noir
        # ---------------------
        with self.canvas.before:
            Color(0, 0, 0, 1)  # noir
            self.border = Line(width=2, rectangle=(self.x, self.y, self.width, self.height))
        self.bind(pos=self.update_border, size=self.update_border)

        # ---------------------
        # Fallback / simulation
        # ---------------------
        self.simulation_label = Label(
            text="📢 [Zone pub – simulation]",
            size_hint_y=None,
            height=50,
            color=(0,0,0,1)
        )
        self.add_widget(self.simulation_label)  # Toujours présent, même sur Android

        # Si Android et KivMob disponible, on tente de charger la vraie bannière
        if platform == "android" and KivMob:
            try:
                self.load_banner()
            except Exception as e:
                # Affiche erreur dans label de simulation
                self.simulation_label.text = f"[Erreur AdMob] {e}"

    def update_border(self, *args):
        self.border.rectangle = (self.x, self.y, self.width, self.height)

    def load_banner(self):
        if self.banner_loaded or platform != "android" or KivMob is None:
            return
        self.banner_loaded = True

        # Crée l’objet AdMob
        self.ads = KivMob("ca-app-pub-3940256099942544~3347511713")
        banner_id = "ca-app-pub-3940256099942544/6300978111"

        # Charge et affiche la bannière
        self.ads.new_banner(banner_id, top_pos=False)
        self.ads.request_banner()
        self.ads.show_banner()

        # Masque le label de simulation une fois la vraie bannière chargée
        self.remove_widget(self.simulation_label)
