from models.budget_model import BudgetModel
from logger import logger

class BudgetController:
    def __init__(self):
        self.model = BudgetModel()

    def ajouter(self, categorie, date, nom, montant):
        self.model.ajouter_entree(categorie, date, nom, montant)

    def supprimer(self, categorie, index):
        self.model.supprimer_entree(categorie, index)

    def get_total(self, categorie):
        return self.model.get_total(categorie)

    def get_solde(self):
        return self.model.get_solde()

    def get_entrees(self, categorie):
        return self.model.data.get(categorie, [])