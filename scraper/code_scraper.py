"""
Il s'agit de ramener les infos suivantes pour les cinq premiers produit du résultat de recherche (mot clé) :
- Nome du produit
- Lien vers la fiche produit
- Prix
- Image du produit (lien)
- Notation (sur 5)

Package utilisé pour le scraping : beautifulsoup (craping), request

"""

import requests
from bs4 import BeautifulSoup


#définition de la fonction
def scrap_jumia(keyword: str, max_results: int = 5) -> list[dict]:
    #utile pour se faire passer pour un vrai navigateur au moment du scraping
    #pour éviter des blocages éventuellement prévus par les développeur du site
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    }
    #url de la page du résultat de recherche
    url = f"https://www.jumia.ci/catalog/?q={keyword}"
    


with open("test.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "lxml")

# find_all au lieu de find : on récupère TOUS les produits, pas juste le premier
produits = soup.find_all("a", class_="core")

print(f"Nombre de produits trouvés : {len(produits)}")

resultats = []

for produit in produits:
    lien = produit.get("href")
    lien_complet = "https://www.jumia.ci" + lien

    nom_tag = produit.find("h3", class_="name")
    nom = nom_tag.text if nom_tag else "Nom inconnu"

    prix_tag = produit.find("div", class_="prc")
    prix = prix_tag.text if prix_tag else "Prix inconnu"

    img_tag = produit.find("img")
    image_url = img_tag.get("data-src") or img_tag.get("src") if img_tag else None

    stars_div = produit.find("div", class_="stars _s")
    note = stars_div.text.strip() if stars_div else "Pas de note"

    resultats.append({
        "nom": nom,
        "prix": prix,
        "image": image_url,
        "note": note,
        "lien": lien_complet
    })

# On affiche les 3 premiers pour vérifier
for r in resultats[:3]:
    print(r)
    print("---")