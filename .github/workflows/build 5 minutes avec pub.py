- name: Build APK
      run: |
        source venv/bin/activate
        ./venv/bin/p4a apk \
          --private ./app \
          --package=org.example.monapp \
          --name="Mon budget perso" \
          --version=0.1 \
          --bootstrap=sdl2 \
          --icon=logo.png \
          --presplash=app/logo1.png \
          --requirements=python3,kivy,android,pyjnius,setuptools,plyer,requests \
          --permission WRITE_EXTERNAL_STORAGE \
          --permission READ_EXTERNAL_STORAGE \
          --permission INTERNET \
          --permission ACCESS_NETWORK_STATE \
          --arch=arm64-v8a \
          --sdk_dir=$SDK_DIR \
          --ndk_dir=$ANDROID_NDK_HOME \
          --android_api=36 \
          --orientation=portrait \
          --dist-name=monapp \
          --add-gradle-dependency "com.google.android.gms:play-services-ads:23.1.0" \
          --debug