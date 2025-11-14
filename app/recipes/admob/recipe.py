from pythonforandroid.recipe import Recipe

class AdmobRecipe(Recipe):
    version = '24.3.0'
    url = None
    depends = ['android']

    # Indique à p4a que ton AAR doit être inclus
    android_libs = ['play-services-ads-24.3.0.aar']

    def get_build_dir(self, arch):
        return self.get_recipe_dir()

recipe = AdmobRecipe()
