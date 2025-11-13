from pythonforandroid.recipe import Recipe

class AdMobRecipe(Recipe):
    version = '24.3.0'  # version de play-services-ads que tu veux
    url = None  # pas besoin de télécharger, on utilisera ton AAR local
    depends = ['android']  # dépendance obligatoire pour p4a

    def get_build_dir(self, arch):
        # retourne le répertoire où se trouvent les fichiers extraits (AAR)
        return self.get_recipe_dir()
