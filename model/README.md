# Modèle de reconnaissance d'image — EcoSort

Ce dossier contient tout ce qui concerne le Jalon 1 du projet : l'entraînement du modèle de deep learning chargé de reconnaître la matière d'un produit à partir de sa photo Jumia.

## Structure

```
model/
├── data/
│   ├── raw/            # dataset Kaggle téléchargé (jamais versionné sur Git)
│   └── splits/         # train/val/test générés par prepare_data.py (jamais versionné)
├── models/              # modele_eco_sort.h5, class_names.json (jamais versionné)
├── src/
│   ├── config.py        # chemins, hyperparamètres, correspondance classes -> poubelles
│   ├── prepare_data.py  # téléchargement Kaggle + split train/val/test
│   ├── dataset.py       # pipelines tf.data + augmentation
│   ├── model.py         # architecture MobileNetV2 (transfer learning)
│   ├── train.py         # entraînement en 2 phases (tête puis fine-tuning)
│   ├── evaluate.py       # rapport de classification + matrice de confusion
│   └── predict.py       # prédiction sur une image unique
└── requirements.txt
```

## Approche retenue

Le choix se porte sur du **transfer learning avec MobileNetV2** plutôt qu'un CNN entraîné from scratch. Avec seulement environ 2 500 images réparties sur 6 classes, un CNN custom sur-apprendrait vite et resterait moins robuste. MobileNetV2 apporte des filtres déjà entraînés sur ImageNet, un temps d'entraînement raisonnable même sans GPU puissant, et un poids de modèle léger, ce qui compte pour l'étape de containerisation Docker au Jalon 2.

L'entraînement se fait en deux temps. On commence par geler la base MobileNetV2 et entraîner uniquement la tête de classification pendant une quinzaine d'époques, puis on dégèle les dernières couches de la base pour un fine-tuning à taux d'apprentissage très bas. Cette approche évite de détruire les poids pré-entraînés tout en adaptant le modèle aux textures spécifiques des matériaux (plastique, verre, carton, etc.).

## Le dataset Kaggle et son écart avec les images Jumia

Le dataset recommandé (`asdasdasasdas/garbage-classification`, dataset utilisé par le notebook Kaggle cité dans le brief) contient des photos de déchets isolés dans six classes : `cardboard`, `glass`, `metal`, `paper`, `plastic`, `trash`. Les images Jumia sont en réalité assez proches de ce type de photo (produit seul, généralement sur fond neutre), donc l'écart de domaine reste modéré comparé à d'autres datasets de déchets pris en extérieur. Il reste malgré tout réel : les produits Jumia sont neufs, parfois emballés dans plusieurs matières à la fois, avec des logos et du texte, alors que le dataset Kaggle montre des objets isolés et souvent usagés.

Pour limiter ce risque, le pipeline applique une augmentation de données assez marquée (rotation, zoom, luminosité, contraste) afin que le modèle ne se fixe pas sur des détails trop spécifiques au dataset d'entraînement. Il est aussi recommandé, une fois un premier modèle entraîné, de le tester manuellement sur une dizaine de vraies captures d'écran Jumia (via `predict.py`) avant de le considérer comme définitif. Si les erreurs sont concentrées sur certaines matières, on pourra enrichir le dataset avec quelques images Jumia annotées à la main.

## Le problème de la catégorie D3E (électronique)

Le dataset Kaggle ne contient aucune classe électronique. Le modèle d'image seul ne peut donc pas reconnaître un smartphone ou un chargeur comme relevant du bac D3E : il les classera probablement dans `plastic` ou `metal` par erreur. Deux options existent pour combler ce trou, à trancher avec l'équipe.

La première consiste à détecter le D3E en amont du modèle d'image, en s'appuyant sur la catégorie du produit telle que renvoyée par le scraping Jumia (rayon "Téléphonie", "Informatique", "Électroménager") ou sur des mots-clés du nom de produit. C'est la solution la plus fiable et la moins coûteuse, puisqu'elle ne demande aucune donnée supplémentaire.

La seconde consiste à collecter une petite banque d'images d'appareils électroniques et à ajouter une septième classe au modèle. C'est plus long à mettre en place mais rend le modèle autonome. Le fichier `config.py` est déjà écrit pour accueillir cette classe supplémentaire le jour où elle existera : il suffira d'ajouter un dossier `electronics/` dans les données et une entrée dans `CLASS_TO_BIN`.

## Images Jumia contenant plusieurs éléments

Certaines fiches produit Jumia peuvent afficher plusieurs objets sur une même photo (lots, accessoires inclus, visuels marketing avec logos et badges promo), une situation que le dataset Kaggle, composé de photos d'un seul déchet isolé, ne représente pas. Trois niveaux de réponse sont possibles, du plus simple au plus coûteux.

Le plus rentable pour ce projet est un seuil de confiance sur la prédiction : `predict.py` renvoie désormais un champ `certain` et classe le résultat en `INCERTAIN` si la probabilité de la classe prédite descend sous `config.CONFIDENCE_THRESHOLD` (0.6 par défaut). Une image ambiguë déclenche donc un résultat explicite plutôt qu'une réponse fausse donnée avec assurance.

Un second niveau, non implémenté pour l'instant, consisterait à recadrer l'image au centre avant redimensionnement pour limiter l'effet des badges et logos en périphérie.

Le niveau le plus robuste, la détection d'objets pour isoler chaque élément avant classification, est hors périmètre de ce projet : le dataset Kaggle ne fournit aucune annotation de position, et le délai ne permet pas d'entraîner un détecteur dédié. À documenter comme piste d'amélioration future.

## Comment reproduire l'entraînement

Toutes les commandes se lancent depuis le dossier `model/`.

```bash
pip install -r requirements.txt
python -m src.prepare_data      # télécharge le dataset Kaggle et le sépare en train/val/test
python -m src.train              # entraîne le modèle, sauvegarde model/models/modele_eco_sort.h5
python -m src.evaluate           # rapport de classification + matrice de confusion
python -m src.predict chemin/vers/une/image.jpg
```

Voir `data/README.md` pour la configuration de l'accès à l'API Kaggle.

## Livrable

Le fichier `models/modele_eco_sort.h5` (jamais versionné sur Git, à fournir séparément à l'équipe ou régénéré par CI/CD) ainsi que `models/class_names.json` sont les deux fichiers attendus par l'application Streamlit pour le Jalon 2.
