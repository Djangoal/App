import json
import os


class DataManager:
    def __init__(self, fichier):
        self.fichier = fichier
        self.donnees = []
        self.charger_donnees()

    def charger_donnees(self):
        if os.path.exists(self.fichier):
            try:
                with open(self.fichier, 'r', encoding='utf-8') as f:
                    self.donnees = json.load(f)
            except json.JSONDecodeError:
                self.donnees = []
        else:
            self.donnees = []

    def sauvegarder_donnees(self):
        with open(self.fichier, 'w', encoding='utf-8') as f:
            json.dump(self.donnees, f, indent=4, ensure_ascii=False)

    def ajouter_entree(self, entree):
        self.donnees.append(entree)
        self.sauvegarder_donnees()

    def supprimer_entree(self, index):
        if 0 <= index < len(self.donnees):
            del self.donnees[index]
            self.sauvegarder_donnees()

    def filtrer_par_categorie(self, categorie):
        return [e for e in self.donnees if e.get('categorie') == categorie]

    def calculer_total(self, categorie):
        return sum(e.get("montant", 0) for e in self.donnees if e.get("categorie") == categorie)

    def get_donnees(self):
        return self.donnees