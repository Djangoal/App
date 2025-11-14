from pythonforandroid.recipe import Recipe

class AdMobWrapperRecipe(Recipe):
    version = '1.0'
    url = None
    depends = ['android']

    # Indiquer que le Java doit être compilé
    java_src = ['AdMobBridge.java']

    def get_build_dir(self, arch):
        return self.get_recipe_dir()

recipe = AdMobWrapperRecipe()
