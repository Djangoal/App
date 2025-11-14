from pythonforandroid.recipe import Recipe

class AdMobRecipe(Recipe):
    version = "1.0"
    url = None  # Pas de téléchargement externe
    name = "admob"
    depends = ["python3"]

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        return env

# ⚠ IMPORTANT : P4A cherche exactement cette variable
recipe = AdMobRecipe()
