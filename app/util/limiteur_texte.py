def limiter_longueur(instance, value, max_length=13):
    """
    Limite la longueur du texte d'un champ de saisie.
    :param instance: le champ TextInput
    :param value: texte actuel
    :param max_length: longueur maximale autorisée (par défaut 13)
    """
    if len(value) > max_length:
        instance.text = value[:max_length]