import json
import os
from logger import logger


class AppConfig:
    """
    Classe de gestion de la configuration de l'application.
    Charge, sauvegarde et fournit les préférences utilisateur.
    """

    def __init__(self, config_path="config.json"):
        self.config_path = config_path

        # Valeurs par défaut
        self.defaults = {
            "activer_pin": False,
            "show_total_revenus": True,
            "show_total_charges": True,
            "show_total_depenses": True,
            "show_restant_a_payer": True
        }

        self.data = self.defaults.copy()
        self.load()

    # -------------------- Chargement --------------------
    def load(self):
        """Charge la configuration depuis le fichier JSON"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    contenu = json.load(f)
                # Met à jour les valeurs existantes sans supprimer les nouvelles clés
                self.data.update(contenu)
                logger.info("Configuration chargée avec succès.")
            except Exception as e:
                logger.error(f"Erreur lors du chargement de la configuration : {e}")
        else:
            logger.warning("Aucun fichier de configuration trouvé. Utilisation des valeurs par défaut.")
            self.save()

    # -------------------- Sauvegarde --------------------
    def save(self):
        """Sauvegarde la configuration actuelle dans le fichier JSON"""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            logger.info("Configuration sauvegardée avec succès.")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de la configuration : {e}")

    # -------------------- Accès simplifié --------------------
    def __getitem__(self, key):
        return self.data.get(key, self.defaults.get(key))

    def __setitem__(self, key, value):
        self.data[key] = value
        self.save()

    # -------------------- Méthodes utilitaires --------------------
    def toggle(self, key):
        """Inverse un booléen et sauvegarde immédiatement"""
        if key in self.data:
            self.data[key] = not self.data[key]
            self.save()
            return self.data[key]
        else:
            logger.warning(f"Clé inconnue dans la configuration : {key}")
            return None