from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.utils import platform

try:
    from kivmob import KivMob
except ImportError:
    KivMob = None

class AdMobBanner(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        from kivy.core.window import Window
        self.height = int(Window.height * 0.08)  # 8% de la hauteur de l'écran
        self.size_hint_y = None
        self.orientation = "vertical"

        self.ads = None
        self.banner_loaded = False

        # Affichage fallback sur PC ou si KivMob non disponible
        if platform != "android" or KivMob is None:
            self.add_widget(Label(
                text="📢 [Zone pub – simulation]",
                size_hint_y=None,
                height=50,
                color=(0, 0, 0, 1)  # texte en noir
            ))

    def load_banner(self):
        """Charge et affiche la bannière AdMob sur Android."""
        if self.banner_loaded or platform != "android" or KivMob is None:
            return  # déjà chargé ou pas Android
        self.banner_loaded = True

        try:
            self.ads = KivMob("ca-app-pub-3940256099942544~3347511713")
            banner_id = "ca-app-pub-3940256099942544/6300978111"

            # Crée la bannière en bas de l'écran
            self.ads.new_banner(banner_id, top_pos=False)
            self.ads.request_banner()
            self.ads.show_banner()
        except Exception as e:
            # Affiche une erreur en noir si la pub ne peut pas se charger
            self.clear_widgets()
            self.add_widget(Label(
                text=f"[Erreur AdMob] {e}",
                size_hint_y=None,
                height=50,
                color=(0, 0, 0, 1)  # texte en noir
            ))
