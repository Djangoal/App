package org.example.admobwrapper;

import android.app.Activity;
import com.google.android.gms.ads.MobileAds;

public class AdMobBridge {
    public static void init(Activity activity) {
        MobileAds.initialize(activity, initializationStatus -> {});
    }
}
