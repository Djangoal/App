import json
import os

class BudgetModel:
    def __init__(self, filepath='data/donnees_budget.json'):
        self.filepath = filepath
        self.data = {"revenu": [], "charges_fixe": [], "depense": []}
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.save_data()

    def save_data(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def ajouter_entree(self, categorie, date, nom, montant):
        self.data[categorie].append({
            "date": date,
            "nom": nom,
            "montant": float(montant)
        })
        self.save_data()

    def supprimer_entree(self, categorie, index):
        if 0 <= index < len(self.data[categorie]):
            del self.data[categorie][index]
            self.save_data()

    def get_total(self, categorie):
        return sum(e["montant"] for e in self.data.get(categorie, []))

    def get_solde(self):
        revenus = self.get_total("revenu")
        charges = self.get_total("charges_fixe")
        depenses = self.get_total("depense")
        return revenus - charges - depenses
