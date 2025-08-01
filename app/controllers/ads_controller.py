from libs.kivmob import KivMob, TestIds

class AdsController:
    def __init__(self):
        self.ads = KivMob(TestIds.APP)
        self.ads.new_banner(TestIds.BANNER)
        self.ads.new_interstitial(TestIds.INTERSTITIAL)

    def show_banner(self):
        self.ads.show_banner()

    def hide_banner(self):
        self.ads.hide_banner()

    def show_interstitial(self):
        if self.ads.is_interstitial_loaded():
            self.ads.show_interstitial()

# Singleton à importer partout
ads_controller = AdsController()