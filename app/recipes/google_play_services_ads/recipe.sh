#!/bin/bash
# ===============================================================
# ✅ Recette python-for-android : Intégration AdMob / Google Play Services Ads
# ===============================================================
# Ce script permet d'ajouter la dépendance Gradle requise pour
# charger les annonces AdMob dans une application Kivy Android.
# ===============================================================

set -e

echo "📦 [google_play_services_ads] Injection de la dépendance AdMob..."

# Le dossier de distribution généré par python-for-android
DIST_DIR="$DIST_DIR"
if [ -z "$DIST_DIR" ]; then
    DIST_DIR="$HOME/.local/share/python-for-android/dists/monapp_release"
fi

GRADLE_FILE="$DIST_DIR/build.gradle"

# Vérifie que le fichier existe
if [ ! -f "$GRADLE_FILE" ]; then
    echo "❌ [google_play_services_ads] Fichier build.gradle introuvable dans : $DIST_DIR"
    exit 1
fi

echo "📄 [google_play_services_ads] Fichier trouvé : $GRADLE_FILE"

# Ajout du dépôt Google (nécessaire pour récupérer les libs Play Services)
if ! grep -q "google()" "$GRADLE_FILE"; then
    echo "🧩 Ajout du dépôt Google..."
    sed -i '/repositories {/a \        google()' "$GRADLE_FILE"
fi

# Injection de la dépendance AdMob
if ! grep -q "com.google.android.gms:play-services-ads" "$GRADLE_FILE"; then
    echo "🧩 Injection de la dépendance AdMob..."
    # Compatibilité : certaines versions de Gradle n’acceptent pas "implementation"
    # On teste la syntaxe présente dans le fichier
    if grep -q "compile " "$GRADLE_FILE"; then
        SYNTAX="compile"
    elif grep -q "api " "$GRADLE_FILE"; then
        SYNTAX="api"
    else
        SYNTAX="implementation"
    fi

    sed -i "/dependencies {/a \    $SYNTAX 'com.google.android.gms:play-services-ads:23.3.0'" "$GRADLE_FILE"
    echo "✅ [google_play_services_ads] Dépendance AdMob ajoutée avec $SYNTAX"
else
    echo "✅ [google_play_services_ads] Dépendance déjà présente"
fi

# Vérification post-modification
echo "🧾 Contenu du bloc dependencies :"
grep -A 5 "dependencies {" "$
