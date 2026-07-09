"""
Il s'agit de ramener les infos suivantes pour les cinq premiers produit du résultat de recherche (mot clé) :
- Nome du produit
- Lien vers la fiche produit
- Prix
- Image du produit (lien)
- Notation (sur 5)

Package utilisé pour le scraping : beautifulsoup (craping), request

"""


from bs4 import BeautifulSoup

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