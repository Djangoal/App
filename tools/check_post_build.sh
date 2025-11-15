#!/bin/bash
APK="$1"

if [ ! -f "$APK" ]; then
    echo "❌ Aucun APK trouvé !"
    exit 1
fi

TMP_DIR=$(mktemp -d)
unzip -q "$APK" -d "$TMP_DIR"

echo "=== Vérification AdMob ==="
if grep -qr "com/google/android/gms/ads" "$TMP_DIR"; then
    echo "✅ AdMob SDK détecté"
else
    echo "❌ AdMob SDK introuvable"
    exit 1
fi

echo "=== Vérification Google Play Services ==="
if grep -qr "com/google/android/gms" "$TMP_DIR"; then
    echo "✅ Google Play Services détecté"
else
    echo "❌ Google Play Services introuvables"
    exit 1
fi

echo "=== Vérification AAR embarqués ==="
if grep -qr "classes.dex" "$TMP_DIR"; then
    echo "✅ classes.dex trouvé"
else
    echo "❌ classes.dex manquant !"
    exit 1
fi

echo "🎉 Vérification terminée avec succès."
exit 0
