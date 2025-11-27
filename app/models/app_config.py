import json
import os
from kivy.resources import resource_find
from logger import logger


class AppConfig:

    def __init__(self, config_path="config.json"):
        self.config_path = config_path

        # Chemin local Android
        self.local_path = os.path.join(os.getcwd(), self.config_path)

        self.defaults = {
            "activer_pin": False,
            "show_total_revenus": True,
            "show_total_charges": True,
            "show_total_depenses": True,
            "show_restant_a_payer": True
        }

        # Valeurs en mémoire
        self.data = self.defaults.copy()

        # Charger correctement
        self.load()

    # -------------------- Chargement --------------------
    def load(self):
        """Charge ou crée un fichier local depuis la ressource APK"""
        if os.path.exists(self.local_path):
            # 📌 Fichier déjà créé → lecture normale
            try:
                with open(self.local_path, "r", encoding="utf-8") as f:
                    contenu = json.load(f)
                self.data.update(contenu)
                logger.info("Configuration locale chargée.")
            except Exception as e:
                logger.error(f"Erreur lecture config locale : {e}")
        else:
            # 📌 Le fichier n'existe pas → on copie celui intégré dans l’APK
            logger.warning("Config locale absente → création à partir de l’APK")
            src = resource_find(self.config_path)

            if src:
                try:
                    with open(src, "r", encoding="utf-8") as f:
                        contenu = json.load(f)
                    self.data.update(contenu)
                except Exception as e:
                    logger.error(f"Erreur lecture config intégrée dans l’APK : {e}")
            else:
                logger.warning("Aucune config intégrée trouvée → utilisation des valeurs par défaut.")

            # Sauvegarde du fichier local
            self.save()

    # -------------------- Sauvegarde --------------------
    def save(self):
        """Sauvegarde la configuration actuelle dans un fichier local"""
        try:
            with open(self.local_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            logger.info("Configuration sauvegardée localement.")
        except Exception as e:
            logger.error(f"Erreur sauvegarde config : {e}")

    # -------------------- Accès simplifié --------------------
    def __getitem__(self, key):
        return self.data.get(key, self.defaults.get(key))

    def __setitem__(self, key, value):
        self.data[key] = value
        self.save()

    # -------------------- Méthodes utilitaires --------------------
    def toggle(self, key):
        if key in self.data:
            self.data[key] = not self.data[key]
            self.save()
            return self.data[key]
        else:
            logger.warning(f"Clé inconnue : {key}")
            return None
