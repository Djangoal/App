import json
import os
from utils.logger import log_error  # 👈 ajout du logger

class BudgetModel:
    def __init__(self, filepath='data/donnees_budget.json'):
        self.filepath = filepath
        self.data = {"revenu": [], "charges_fixe": [], "depense": []}
        self.load_data()

    def load_data(self):
        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            else:
                self.save_data()
        except Exception as e:
            log_error(f"Erreur lors du chargement des données depuis '{self.filepath}' : {e}")
            self.data = {"revenu": [], "charges_fixe": [], "depense": []}

    def save_data(self):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            log_error(f"Erreur lors de la sauvegarde des données dans '{self.filepath}' : {e}")

    def ajouter_entree(self, categorie, date, nom, montant):
        try:
            self.data[categorie].append({
                "date": date,
                "nom": nom,
                "montant": float(montant)
            })
            self.save_data()
        except Exception as e:
            log_error(f"Erreur lors de l'ajout d'une entrée dans la catégorie '{categorie}' : {e}")

    def supprimer_entree(self, categorie, index):
        try:
            if 0 <= index < len(self.data[categorie]):
                del self.data[categorie][index]
                self.save_data()
            else:
                log_error(f"Index invalide lors de la suppression : {index} dans la catégorie '{categorie}'")
        except Exception as e:
            log_error(f"Erreur lors de la suppression dans la catégorie '{categorie}' à l'index {index} : {e}")

    def get_total(self, categorie):
        try:
            return sum(e["montant"] for e in self.data.get(categorie, []))
        except Exception as e:
            log_error(f"Erreur lors du calcul du total pour la catégorie '{categorie}' : {e}")
            return 0.0

    def get_solde(self):
        try:
            revenus = self.get_total("revenu")
            charges = self.get_total("charges_fixe")
            depenses = self.get_total("depense")
            return revenus - charges - depenses
        except Exception as e:
            log_error(f"Erreur lors du calcul du solde : {e}")
            return 0.0