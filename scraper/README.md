# Module Scraping - EcoSort-Search

Recherche des produits sur Jumia CI à partir d'un mot-clé.

## Utilisation

```python
from search_jumia import search_jumia

resultats = search_jumia("shampooing")
```

Retourne une liste de dictionnaires (max 5 par défaut) :
```python
[
    {
        "nom": "Garnier Shampoing Ultra Doux 300Ml",
        "prix": "3,900 FCFA",
        "image": "https://ci.jumia.is/...jpg",
        "note": "2.3 out of 5",
        "lien": "https://www.jumia.ci/garnier-...html"
    },
    ...
]
```

## Installation

```bash
pip install -r requirements.txt
```

## Paramètres

| Paramètre | Type | Description |
|---|---|---|
| `keyword` | str | Mot-clé de recherche (obligatoire) |
| `max_results` | int | Nombre de résultats (défaut: 5) |