
from pythonforandroid.recipe import Recipe
import os

class AdMobRecipe(Recipe):
    version = "1.0"
    url = None
    name = "admob"
    depends = ["python3", "kivy", "android"]

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        return env

    def get_build_dir(self, arch):
        return os.path.join(self.get_build_container_dir(arch), "admob_build")

recipe = AdMobRecipe()

