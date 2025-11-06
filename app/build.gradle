// minimal module-level build.gradle to inject the dependency
buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        // Gradle plugin is not used by p4a but having repositories here helps
        classpath "com.android.tools.build:gradle:7.4.2"
    }
}

apply plugin: 'com.android.application'

android {
    compileSdkVersion 36
    defaultConfig {
        minSdkVersion 24
        targetSdkVersion 36
    }
    // keep config minimal, p4a will merge things
}

repositories {
    google()
    mavenCentral()
}

dependencies {
    // <-- la dépendance AdMob réelle
    implementation 'com.google.android.gms:play-services-ads:23.3.0'
}
