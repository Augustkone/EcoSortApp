"""Filtres a appliquer AVANT le modele d'image.

Certaines categories de produits ne peuvent pas etre reconnues correctement
par le modele de reconnaissance d'image, parce que le dataset Kaggle utilise
pour l'entrainement ne les represente pas (D3E) ou parce que le brief exige
une distinction que la seule photo ne permet pas de trancher de facon fiable
(verre d'emballage contre vaisselle). Ces cas doivent etre detectes en amont,
a partir du nom et de la categorie du produit tels que renvoyes par le
scraping Jumia, avant meme d'appeler predict_image().

Usage cote application (pseudo-code) :

    from src.upstream_filters import classify_before_image_model

    filtre = classify_before_image_model(nom_produit, categorie_produit)
    if filtre is not None:
        poubelle = filtre  # "D3E" ou "MARRON", pas besoin du modele
    else:
        poubelle = predict_image(chemin_image)["poubelle"]

Usage (depuis le dossier model/) pour un test rapide en ligne de commande :
    python -m src.upstream_filters "Ecouteurs Bluetooth JBL" "Telephonie"
"""
import sys
import unicodedata

from . import config


def _normalise(texte: str) -> str:
    """Minuscules et sans accents, pour une comparaison robuste aux mots-cles."""
    texte = texte.lower()
    texte = unicodedata.normalize("NFKD", texte)
    return "".join(c for c in texte if not unicodedata.combining(c))


def is_d3e(nom_produit: str, categorie_produit: str = "") -> bool:
    texte = _normalise(f"{nom_produit} {categorie_produit}")
    mots_cles = [_normalise(m) for m in config.D3E_KEYWORDS + config.D3E_CATEGORIES]
    return any(mot in texte for mot in mots_cles)


def is_vaisselle(nom_produit: str, categorie_produit: str = "") -> bool:
    texte = _normalise(f"{nom_produit} {categorie_produit}")
    mots_cles = [_normalise(m) for m in config.VAISSELLE_KEYWORDS]
    return any(mot in texte for mot in mots_cles)


def classify_before_image_model(nom_produit: str, categorie_produit: str = ""):
    """Retourne "D3E" ou "MARRON" si le produit doit etre tranche sans le
    modele d'image, sinon None (le modele d'image doit alors etre appele)."""
    if is_d3e(nom_produit, categorie_produit):
        return "D3E"
    if is_vaisselle(nom_produit, categorie_produit):
        return "MARRON"
    return None


if __name__ == "__main__":
    nom = sys.argv[1] if len(sys.argv) > 1 else ""
    categorie = sys.argv[2] if len(sys.argv) > 2 else ""
    resultat = classify_before_image_model(nom, categorie)
    if resultat is None:
        print("Aucun filtre en amont ne s'applique, appeler le modele d'image.")
    else:
        print(f"Filtre en amont applique, poubelle = {resultat}, modele non appele.")
