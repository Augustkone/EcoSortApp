"""
Fonctions FACTICES en attendant les vrais livrables de Personne A (model/) 
et Personne B (scraper/). Signatures identiques aux vraies fonctions pour 
faciliter le remplacement lors de l'intégration finale.
"""

import random
import time


def search_jumia(keyword: str, max_results: int = 5) -> list[dict]:
    """
    MOCK - simule le scraper Jumia de Personne B.
    Retourne une liste de produits factices basés sur le mot-clé.
    """
    time.sleep(0.5)

    fake_catalog = [
        {"titre": f"{keyword.capitalize()} - Bouteille 500ml", 
         "image_url": "https://picsum.photos/seed/produit1/200/200",
         "lien": "#", "prix": "1 500 FCFA"},
        {"titre": f"{keyword.capitalize()} - Pack familial", 
         "image_url": "https://picsum.photos/seed/produit2/200/200",
         "lien": "#", "prix": "3 200 FCFA"},
        {"titre": f"{keyword.capitalize()} - Format standard", 
         "image_url": "https://picsum.photos/seed/produit3/200/200",
         "lien": "#", "prix": "900 FCFA"},
        {"titre": f"{keyword.capitalize()} - Édition premium", 
         "image_url": "https://picsum.photos/seed/produit4/200/200",
         "lien": "#", "prix": "5 000 FCFA"},
        {"titre": f"{keyword.capitalize()} - Lot de 3", 
         "image_url": "https://picsum.photos/seed/produit5/200/200",
         "lien": "#", "prix": "2 100 FCFA"},
    ]
    return fake_catalog[:max_results]

def predict_category(image_url: str) -> dict:
    """
    MOCK - simule le modèle CNN de Personne A.
    Retourne une catégorie de tri aléatoire avec un score de confiance factice.
    """
    time.sleep(0.8)  # simule le temps d'inférence du modèle

    categories = [
        {"code": "jaune", "label": "Poubelle Jaune", "matiere": "Plastique / Métal / Carton"},
        {"code": "vert", "label": "Poubelle Verte", "matiere": "Verre"},
        {"code": "bleu", "label": "Poubelle Bleue", "matiere": "Papier"},
        {"code": "gris", "label": "Bac Électronique (D3E)", "matiere": "Appareil électrique/électronique"},
        {"code": "marron", "label": "Poubelle Marron/Noire", "matiere": "Déchet résiduel non recyclable"},
    ]
    result = random.choice(categories)
    result["confiance"] = round(random.uniform(0.75, 0.98), 2)
    return result