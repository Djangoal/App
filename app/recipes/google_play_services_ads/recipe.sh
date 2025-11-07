#!/bin/bash
set -e

# Récupération du dossier Android
BUILD_DIR="$1"
GRADLE_FILE="$BUILD_DIR/build.gradle"

echo "🔧 Ajout de la dépendance Google Play Services Ads au projet Gradle"

# Remplacement sécurisé de 'compile' par 'implementation' si nécessaire
if grep -q "compile 'com.google.android.gms:play-services-ads" "$GRADLE_FILE"; then
    sed -i "s/compile 'com.google.android.gms:play-services-ads/implementation 'com.google.android.gms:play-services-ads/g" "$GRADLE_FILE"
else
    # Si elle n'existe pas, on l'ajoute proprement
    sed -i "/dependencies {/a\    implementation 'com.google.android.gms:play-services-ads:23.3.0'" "$GRADLE_FILE"
fi

echo "✅ Dépendance Google Ads ajoutée avec succès"
