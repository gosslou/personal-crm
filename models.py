"""
models.py - Validation et structure des donnees du CRM.

Ce fichier definit les regles de validation pour les contacts.
Avant de creer ou modifier un contact, on verifie que les donnees
sont correctes (nom non vide, categorie valide, etc.).
"""


CATEGORIES_VALIDES = ["famille", "ami", "pro", "autre"]


class ValidationError(Exception):
    """Erreur levee quand les donnees d'un contact ne sont pas valides."""
    pass


def valider_contact(nom, prenom="", categorie="autre", informations=None):
    """
    Verifie que les donnees d'un contact sont valides.

    Regles :
    - Le nom ne doit pas etre vide
    - La categorie doit etre dans la liste autorisee
    - Les informations doivent etre un dictionnaire (ou None)
    """
    if not nom or not nom.strip():
        raise ValidationError("Le nom est obligatoire.")

    nom = nom.strip()
    prenom = prenom.strip() if prenom else ""

    categorie = categorie.lower().strip()
    if categorie not in CATEGORIES_VALIDES:
        raise ValidationError(
            f"Categorie invalide : '{categorie}'. "
            f"Categories autorisees : {', '.join(CATEGORIES_VALIDES)}"
        )

    if informations is not None and not isinstance(informations, dict):
        raise ValidationError(
            "Les informations doivent etre un dictionnaire (cle: valeur)."
        )

    return {
        "nom": nom,
        "prenom": prenom,
        "categorie": categorie,
        "informations": informations or {}
    }


def valider_note(contenu):
    """Verifie qu'une note n'est pas vide."""
    if not contenu or not contenu.strip():
        raise ValidationError("Le contenu de la note ne peut pas etre vide.")
    return contenu.strip()
