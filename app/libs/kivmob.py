from jnius import autoclass, cast
from android.runnable import run_on_ui_thread

PythonActivity = autoclass('org.kivy.android.PythonActivity')
AdRequest = autoclass('com.google.android.gms.ads.AdRequest')
AdSize = autoclass('com.google.android.gms.ads.AdSize')
AdView = autoclass('com.google.android.gms.ads.AdView')
AdListener = autoclass('com.google.android.gms.ads.AdListener')
InterstitialAd = autoclass('com.google.android.gms.ads.interstitial.InterstitialAd')
InterstitialAdLoadCallback = autoclass('com.google.android.gms.ads.interstitial.InterstitialAdLoadCallback')

class AndroidBridge:
    def __init__(self, app_id):
        self.activity = PythonActivity.mActivity
        self.app_id = app_id
        self._banner = None
        self._interstitial = None  # Ajouté pour éviter les erreurs
        self._loaded = False

    @run_on_ui_thread
    def new_banner(self, ad_unit_id, ad_size='BANNER'):
        self._banner = AdView(self.activity)
        self._banner.setAdSize(getattr(AdSize, ad_size))
        self._banner.setAdUnitId(ad_unit_id)
        layout = self.activity.findViewById(0x01020002)  # android.R.id.content
        layout.addView(self._banner)
        self._banner.loadAd(AdRequest.Builder().build())

    @run_on_ui_thread
    def show_banner(self):
        if self._banner:
            self._banner.setVisibility(0)  # View.VISIBLE

    @run_on_ui_thread
    def hide_banner(self):
        if self._banner:
            self._banner.setVisibility(8)  # View.GONE

    @run_on_ui_thread
    def new_interstitial(self, ad_unit_id):
        self._loaded = False
        ad_request = AdRequest.Builder().build()
        callback = InterstitialAdLoadCallback()
        
        def on_ad_loaded(ad):
            self._interstitial = ad
            self._loaded = True

        def on_ad_failed_to_load(error):
            self._interstitial = None
            self._loaded = False

        callback.onAdLoaded = on_ad_loaded
        callback.onAdFailedToLoad = on_ad_failed_to_load

        InterstitialAd.load(
            self.activity,
            ad_unit_id,
            ad_request,
            callback
        )

    @run_on_ui_thread
    def _is_interstitial_loaded(self):
        if self._interstitial:
            self._loaded = self._interstitial.isLoaded()
        else:
            self._loaded = False

    def is_interstitial_loaded(self):
        self._is_interstitial_loaded()
        return self._loaded

    @run_on_ui_thread
    def _show_interstitial(self):
        if self._interstitial and self._interstitial.isLoaded():
            self._interstitial.show(self.activity)

    def show_interstitial(self):
        self._show_interstitial()


class TestIds:
    APP = "ca-app-pub-3940256099942544~3347511713"
    BANNER = "ca-app-pub-3940256099942544/6300978111"
    INTERSTITIAL = "ca-app-pub-3940256099942544/1033173712"


class KivMob:
    def __init__(self, app_id):
        self.bridge = AndroidBridge(app_id)

    def new_banner(self, ad_unit_id, ad_size='BANNER'):
        self.bridge.new_banner(ad_unit_id, ad_size)

    def show_banner(self):
        self.bridge.show_banner()

    def hide_banner(self):
        self.bridge.hide_banner()

    def new_interstitial(self, ad_unit_id):
        self.bridge.new_interstitial(ad_unit_id)

    def request_interstitial(self):
        pass  # Optionnel, dépend de ton implémentation

    def is_interstitial_loaded(self):
        return self.bridge.is_interstitial_loaded()

    def show_interstitial(self):
        self.bridge.show_interstitial()
