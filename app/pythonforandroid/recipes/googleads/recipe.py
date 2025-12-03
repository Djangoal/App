from pythonforandroid.recipe import GradleRecipe
from pythonforandroid.logger import info

class GoogleAdsRecipe(GradleRecipe):
    name = "googleads"
    version = "22.6.0"
    url = None
    depends = []
    python_depends = []

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        return env

    def gradle_dependencies(self):
        return [
            "com.google.android.gms:play-services-ads:22.6.0"
        ]

    def get_android_permissions(self):
        return [
            "android.permission.INTERNET",
            "android.permission.ACCESS_NETWORK_STATE"
        ]

    def prebuild_arch(self, arch):
        info("GoogleAdsRecipe: prebuild_arch()")
        super().prebuild_arch(arch)

    def build_arch(self, arch):
        info("GoogleAdsRecipe: build_arch()")
        # Pas de compilation native
        pass

recipe = GoogleAdsRecipe()
