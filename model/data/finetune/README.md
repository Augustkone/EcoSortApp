# Jeu de fine-tuning sur photos de catalogue

Ce dossier n'est pas versionné (voir `.gitignore`), les images de produits e-commerce pouvant être soumises à droit d'auteur. Chaque membre de l'équipe qui veut relancer `python -m src.finetune` doit reconstituer ce dossier localement.

## Organisation attendue

```
model/data/finetune/
├── cardboard/   (une quinzaine d'images)
├── glass/
├── metal/
├── paper/
├── plastic/
└── trash/
```

Les noms de dossiers doivent correspondre exactement à `config.CLASS_NAMES` (minuscules, sans accent).

## Où trouver les images

L'idée est de récupérer de vraies photos de catalogue e-commerce (Jumia, Amazon, ou équivalent), donc des produits neufs sur fond neutre, à l'opposé des photos de déchets isolés du dataset Kaggle. Quelques pistes :

Sur Jumia directement, chercher des produits emblématiques de chaque matière (une bouteille d'eau pour plastic, une canette pour metal, un magazine ou un carnet pour paper, un colis en carton pour cardboard, un pot en verre ou une bouteille de vin pour glass) et enregistrer l'image principale de la fiche produit.

Pour trash, plus difficile à trouver sur un site de vente puisque ce n'est pas un produit en soi : on peut utiliser des photos de produits jetables multicouches (sachets de chips, emballages de bonbons) ou garder cette classe uniquement alimentée par le dataset Kaggle si aucune image pertinente n'est trouvée.

Une quinzaine d'images par classe est un bon point de départ, pas besoin de viser plus pour un premier essai.

## Lancer le fine-tuning

Une fois le dossier rempli :

```bash
python -m src.finetune
```

Le script sauvegarde un modèle séparé, `models/modele_eco_sort_v2.h5`, à comparer avec `evaluate.py` et `predict.py` avant de décider de le promouvoir en remplaçant le fichier officiel.
