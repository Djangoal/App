from pythonforandroid.recipe import Recipe
import os
import shutil

class IncludeAARRecipe(Recipe):
    version = "1.0"
    url = None
    name = "include_aar"

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        return env

    def install(self):
        self.info("Copying AARs to dist/libs/")
        lib_dir = os.path.join(self.ctx.dist_dir, "libs")
        os.makedirs(lib_dir, exist_ok=True)
        for aar in os.listdir(os.path.join(self.ctx.get_python_root(), "app/libs")):
            if aar.endswith(".aar"):
                shutil.copy(os.path.join(self.ctx.get_python_root(), "app/libs", aar), lib_dir)

recipe = IncludeAARRecipe()
