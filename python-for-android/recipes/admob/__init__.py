from pythonforandroid.recipe import Recipe
import os

class AdMobRecipe(Recipe):
    version = "1.0"
    url = None  # Pas de téléchargement externe
    name = "admob"
    depends = ["python3", "kivy", "android"]

    # Si tu as des AAR dans libs/, P4A les prendra automatiquement
    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        return env

    # Optionnel : inclure des fichiers supplémentaires (manifest, res)
    def get_build_dir(self, arch):
        # build_dir spécifique à la recipe
        return os.path.join(self.get_build_container_dir(arch), "admob_build")

# ⚠ La variable 'recipe' est obligatoire pour que P4A reconnaisse la recipe
recipe = AdMobRecipe()
