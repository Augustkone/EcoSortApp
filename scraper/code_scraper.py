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
        
    #gestion des cas où la requête ne fonctionne pas. cas possibles
    #Pas de connexion internet, timeout, DNS introuvable, etc
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        # Pas de connexion internet, timeout, DNS introuvable, etc.
        return []
    
    #cas où la requête aboutit mais le serveur répond mal
    if response.status_code != 200:
        return []
    
    soup = BeautifulSoup(response.text, "lxml")
    #chaque produit du résultat de recherche se trouve dans une balise "a", de classe "core"
    produits = soup.find_all("a", class_="core")
    
    resultats = []
    
    #parcours de la liste de produits
    for produit in produits:
        """
            Recherche des produits sur Jumia CI à partir d'un mot-clé.

    Structure HTML ciblée sur la page de résultats :

        <a class="core" href="/nom-du-produit-12345.html">
            <div class="img-c">
                <img data-src="URL_IMAGE" src="URL_IMAGE_FALLBACK" />
            </div>
            <div class="info">
                <h3 class="name">Nom du produit</h3>
                <div class="prc">Prix affiché (ex: 3,900 FCFA)</div>
                <div class="rev">
                    <div class="stars _s">Note sur 5 (ex: "2.3 out of 5")</div>
                    "(Nombre d'avis)"
                </div>
            </div>
        </a>

    Args:
        keyword: Mot-clé de recherche saisi par l'utilisateur (ex: "shampooing").
        max_results: Nombre maximum de produits à retourner (défaut: 5).

    Returns:
        Une liste de dictionnaires, un par produit trouvé, avec les clés :
        "nom", "prix", "image", "note", "lien".
        Retourne une liste vide si la requête échoue.
        """
        #ne pas dépasser le nombre de produit à retourner (par défaut 5)
        if len(resultats) >= max_results:
            break
        
        lien = produit.get("href")
        lien_complet = "https://www.jumia.ci" + lien

        nom_tag = produit.find("h3", class_="name")
        nom = nom_tag.text if nom_tag else "Nom inconnu"

        prix_tag = produit.find("div", class_="prc")
        prix = prix_tag.text if prix_tag else "Prix inconnu"

        img_tag = produit.find("img")
        image_url = (img_tag.get("data-src") or img_tag.get("src")) if img_tag else None

        stars_div = produit.find("div", class_="stars _s")
        note = stars_div.text.strip() if stars_div else "Pas de note"

        resultats.append({
            "nom": nom,
            "prix": prix,
            "image": image_url,
            "note": note,
            "lien": lien_complet,
            "categorie": keyword
       })
    return resultats

# Test de la fonction
if __name__ == "__main__":
    resultats = scrap_jumia("POWERBANK", 2)
    for r in resultats:
        print(r)
        print("---")