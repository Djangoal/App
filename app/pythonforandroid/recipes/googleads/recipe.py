from pythonforandroid.recipe import JavaRecipe
from pythonforandroid.logger import info

class GoogleAdsRecipe(JavaRecipe):
    name = "googleads"
    version = "22.6.0"
    url = None
    depends = []
    python_depends = []

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        return env

    def gradle_dependencies(self):
        # Ajout du SDK Google Mobile Ads
        return [
            "com.google.android.gms:play-services-ads:22.6.0"
        ]

    def get_android_permissions(self):
        # Permissions nécessaires au chargement des annonces
        return [
            "android.permission.INTERNET",
            "android.permission.ACCESS_NETWORK_STATE"
        ]

    def prebuild_arch(self, arch):
        info("GoogleAdsRecipe: prebuild_arch()")
        super().prebuild_arch(arch)

    def build_arch(self, arch):
        info("GoogleAdsRecipe: build_arch()")
        # Pas de compilation native, juste une dépendance Gradle
        pass

# ⚠️ OBLIGATOIRE — p4a charge cette variable globale
recipe = GoogleAdsRecipe()
