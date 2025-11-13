from pythonforandroid.recipe import Recipe

class AdmobRecipe(Recipe):
    version = '24.3.0'
    url = None
    depends = ['android']

    def get_build_dir(self, arch):
        return self.get_recipe_dir()
