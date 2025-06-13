from models.budget_model import BudgetModel
from utils.logger import log_error  # 👈 ajout du logger

class BudgetController:
    def __init__(self):
        try:
            self.model = BudgetModel()
        except Exception as e:
            log_error(f"Erreur lors de l'initialisation du modèle : {e}")

    def ajouter(self, categorie, date, nom, montant):
        try:
            self.model.ajouter_entree(categorie, date, nom, montant)
        except Exception as e:
            log_error(f"Erreur lors de l'ajout d'une entrée ({categorie}, {date}, {nom}, {montant}) : {e}")

    def supprimer(self, categorie, index):
        try:
            self.model.supprimer_entree(categorie, index)
        except Exception as e:
            log_error(f"Erreur lors de la suppression d'une entrée dans '{categorie}' à l'index {index} : {e}")

    def get_total(self, categorie):
        try:
            return self.model.get_total(categorie)
        except Exception as e:
            log_error(f"Erreur lors du calcul du total pour la catégorie '{categorie}' : {e}")
            return 0.0

    def get_solde(self):
        try:
            return self.model.get_solde()
        except Exception as e:
            log_error(f"Erreur lors du calcul du solde : {e}")
            return 0.0

    def get_entrees(self, categorie):
        try:
            return self.model.data.get(categorie, [])
        except Exception as e:
            log_error(f"Erreur lors de la récupération des entrées pour '{categorie}' : {e}")
            return []