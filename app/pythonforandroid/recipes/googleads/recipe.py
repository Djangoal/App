from pythonforandroid.recipe import Recipe
from pythonforandroid.logger import info

class GoogleAdsRecipe(Recipe):
    name = "googleads"
    version = "22.6.0"
    url = None
    depends = []
    python_depends = []

    # Indique qu'on utilise Gradle pour inclure la dépendance
    gradle_depends = [
        "com.google.android.gms:play-services-ads:22.6.0"
    ]

    def prebuild_arch(self, arch):
        info("GoogleAdsRecipe: prebuild_arch()")

    def build_arch(self, arch):
        info("GoogleAdsRecipe: build_arch()")
        # Pas de compilation native, juste dépendance Gradle
        pass

    def get_android_permissions(self):
        return [
            "android.permission.INTERNET",
            "android.permission.ACCESS_NETWORK_STATE"
        ]

recipe = GoogleAdsRecipe()
