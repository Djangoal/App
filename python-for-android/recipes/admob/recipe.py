from pythonforandroid.recipe import JavaRecipe

class AdMobRecipe(JavaRecipe):
    version = '1.0'
    url = None
    depends = ['android']
    libs = ['play-services-ads.aar', 'play-services-base.aar']
    jni_libraries = []
    java_src_dirs = []

recipe = AdMobRecipe()
