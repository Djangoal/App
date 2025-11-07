#!/bin/bash
VERSION=23.3.0
URL="https://repo1.maven.org/maven2/com/google/android/gms/play-services-ads/$VERSION/play-services-ads-$VERSION.aar"
BUILD_DIR=$BUILD_PATH/java/libs

echo "[AdMob Recipe] Téléchargement de $URL..."
mkdir -p $BUILD_DIR
wget -q -O "$BUILD_DIR/play-services-ads.aar" "$URL"

echo "[AdMob Recipe] ✅ Dépendance AdMob ajoutée à $BUILD_DIR"
