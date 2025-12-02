from pythonforandroid.recipe import Recipe
from pythonforandroid.logger import info

class GoogleAdsRecipe(Recipe):
    version = "1.0"
    url = None
    depends = []      # aucune dépendance
    python_depends = [] 

    def prebuild_arch(self, arch):
        info("Google Ads: prebuild_arch called")

    def build_arch(self, arch):
        info("Google Ads: build_arch called")

    def get_include_dirs(self, arch):
        return []

# ⚠️ IMPORTANT : c’est cette ligne que p4a cherche
recipe = GoogleAdsRecipe()
