from jnius import autoclass, cast
from android.runnable import run_on_ui_thread

ADS_ENABLED = True  # Passe à True pour activer pubs (en prod Android)

ADMOB_AVAILABLE = False

# Stubs (vides) pour remplacer les classes Android si pas dispo
class AdViewStub:
    def __init__(self, *args, **kwargs): pass
    def setAdSize(self, *args): pass
    def setAdUnitId(self, *args): pass
    def loadAd(self, *args): pass
    def setVisibility(self, *args): pass

class LinearLayoutStub:
    VERTICAL = 1
    def __init__(self, *args, **kwargs): pass
    def setOrientation(self, *args): pass
    def setBackgroundColor(self, *args): pass
    def setLayoutParams(self, *args): pass
    def addView(self, *args): pass

class ColorStub:
    @staticmethod
    def parseColor(color_str):
        return 0xCCCCCC

class LayoutParamsStub:
    MATCH_PARENT = -1
    WRAP_CONTENT = -2
    def __init__(self, width, height): pass

try:
    if ADS_ENABLED:
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        AdRequest = autoclass('com.google.android.gms.ads.AdRequest')
        AdSize = autoclass('com.google.android.gms.ads.AdSize')
        AdView = autoclass('com.google.android.gms.ads.AdView')
        AdListener = autoclass('com.google.android.gms.ads.AdListener')
        InterstitialAd = autoclass('com.google.android.gms.ads.interstitial.InterstitialAd')
        InterstitialAdLoadCallback = autoclass('com.google.android.gms.ads.interstitial.InterstitialAdLoadCallback')

        LinearLayout = autoclass('android.widget.LinearLayout')
        Color = autoclass('android.graphics.Color')
        LayoutParams = autoclass('android.widget.LinearLayout$LayoutParams')

        ADMOB_AVAILABLE = True
    else:
        # pubs désactivées => stubs
        AdView = AdViewStub
        LinearLayout = LinearLayoutStub
        Color = ColorStub
        LayoutParams = LayoutParamsStub
except Exception as e:
    print("⚠️ AdMob ou Android non dispo :", e)
    AdView = AdViewStub
    LinearLayout = LinearLayoutStub
    Color = ColorStub
    LayoutParams = LayoutParamsStub
    ADMOB_AVAILABLE = False


class AndroidBridge:
    def __init__(self, app_id):
        self.activity = None
        if ADMOB_AVAILABLE:
            self.activity = PythonActivity.mActivity
        self.app_id = app_id
        self._banner = None
        self._interstitial = None
        self._loaded = False

    @run_on_ui_thread
    def new_banner(self, ad_unit_id, ad_size='BANNER'):
        if not ADMOB_AVAILABLE:
            print("⚠️ AdMob non disponible, banner non créée")
            return

        self._banner = AdView(self.activity)
        self._banner.setAdSize(getattr(AdSize, ad_size))
        self._banner.setAdUnitId(ad_unit_id)

        layout_parent = LinearLayout(self.activity)
        layout_parent.setOrientation(LinearLayout.VERTICAL)
        layout_parent.setBackgroundColor(Color.parseColor("#CCCCCC"))

        params = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT)
        layout_parent.setLayoutParams(params)

        layout_parent.addView(self._banner)

        root_layout = self.activity.findViewById(0x01020002)  # android.R.id.content
        root_layout.addView(layout_parent)

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
        if not ADMOB_AVAILABLE:
            print("⚠️ AdMob non disponible, interstitiel non créé")
            return

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
        pass  # Implémentation optionnelle

    def is_interstitial_loaded(self):
        return self.bridge.is_interstitial_loaded()

    def show_interstitial(self):
        self.bridge.show_interstitial()
