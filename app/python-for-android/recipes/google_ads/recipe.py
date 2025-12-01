from pythonforandroid.recipe import JavaRecipe

class GoogleAdsRecipe(JavaRecipe):
    name = "google_ads"
    version = "1.0"
    src_filename = None

    def gradle_dependencies(self):
        return [
            "com.google.android.gms:play-services-ads:22.6.0"
        ]

recipe = GoogleAdsRecipe()
