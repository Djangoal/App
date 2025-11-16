from pythonforandroid.recipe import Recipe
import os

class AdMobRecipe(Recipe):
    version = "1.0"
    url = None  # Pas de téléchargement externe
    name = "admob"
    depends = ["python3", "kivy", "android"]

    # Inclure les AAR automatiquement depuis libs/
    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        return env

    # Optionnel : dossier de build propre
    def get_build_dir(self, arch):
        return os.path.join(self.get_build_container_dir(arch), "admob_build")

# ⚠ Obligatoire pour P4A
recipe = AdMobRecipe()
