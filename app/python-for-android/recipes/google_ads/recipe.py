from pythonforandroid.recipe import JavaRecipe

class GoogleAdsRecipe(JavaRecipe):
    version = "1.0"
    name = "google_ads"
    src_filename = None

    def gradle_dependencies(self):
        return 
["com.google.android.gms:play-services-ads:22.6.0"]

recipe = GoogleAdsRecipe()
