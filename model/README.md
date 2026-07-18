# Modèle de reconnaissance d'image — EcoSort

Ce dossier contient tout ce qui concerne le Jalon 1 du projet : l'entraînement du modèle de deep learning chargé de reconnaître la matière d'un produit à partir de sa photo Jumia.

## Structure

```
model/
├── data/
│   ├── raw/            # dataset Kaggle téléchargé (jamais versionné sur Git)
│   └── splits/         # train/val/test générés par prepare_data.py (jamais versionné)
├── models/              # modele_eco_sort.h5, class_names.json (versionnés, voir section Livrable)
├── src/
│   ├── config.py        # chemins, hyperparamètres, correspondance classes -> poubelles
│   ├── prepare_data.py  # téléchargement Kaggle + split train/val/test
│   ├── prepare_electronics_data.py  # ajoute la classe "electronics" (D3E), equilibree
│   ├── dataset.py       # pipelines tf.data + augmentation
│   ├── model.py         # architecture MobileNetV2 (transfer learning)
│   ├── train.py         # entraînement en 2 phases (tête puis fine-tuning)
│   ├── finetune.py      # fine-tuning complémentaire sur photos de catalogue (Jumia, Amazon...)
│   ├── evaluate.py       # rapport de classification + matrice de confusion
│   ├── predict.py       # prédiction sur une image unique
│   └── upstream_filters.py  # detection D3E/vaisselle avant d'appeler le modele
└── requirements.txt
```

## Approche retenue

Le choix se porte sur du **transfer learning avec MobileNetV2** plutôt qu'un CNN entraîné from scratch. Avec seulement environ 2 500 images réparties sur 6 classes, un CNN custom sur-apprendrait vite et resterait moins robuste. MobileNetV2 apporte des filtres déjà entraînés sur ImageNet, un temps d'entraînement raisonnable même sans GPU puissant, et un poids de modèle léger, ce qui compte pour l'étape de containerisation Docker au Jalon 2.

L'entraînement se fait en deux temps. On commence par geler la base MobileNetV2 et entraîner uniquement la tête de classification pendant une quinzaine d'époques, puis on dégèle les dernières couches de la base pour un fine-tuning à taux d'apprentissage très bas. Cette approche évite de détruire les poids pré-entraînés tout en adaptant le modèle aux textures spécifiques des matériaux (plastique, verre, carton, etc.).

## Le dataset Kaggle et son écart avec les images Jumia

Le dataset recommandé (`asdasdasasdas/garbage-classification`, dataset utilisé par le notebook Kaggle cité dans le brief) contient des photos de déchets isolés dans six classes : `cardboard`, `glass`, `metal`, `paper`, `plastic`, `trash`. Les images Jumia sont en réalité assez proches de ce type de photo (produit seul, généralement sur fond neutre), donc l'écart de domaine reste modéré comparé à d'autres datasets de déchets pris en extérieur. Il reste malgré tout réel : les produits Jumia sont neufs, parfois emballés dans plusieurs matières à la fois, avec des logos et du texte, alors que le dataset Kaggle montre des objets isolés et souvent usagés.

Pour limiter ce risque, le pipeline applique une augmentation de données assez marquée (rotation, zoom, luminosité, contraste) afin que le modèle ne se fixe pas sur des détails trop spécifiques au dataset d'entraînement. Il est aussi recommandé, une fois un premier modèle entraîné, de le tester manuellement sur une dizaine de vraies captures d'écran Jumia (via `predict.py`) avant de le considérer comme définitif. Si les erreurs sont concentrées sur certaines matières, on pourra enrichir le dataset avec quelques images Jumia annotées à la main.

## Le problème de la catégorie D3E (électronique)

Le dataset Kaggle de base ne contient aucune classe électronique. Le modèle d'image seul ne pouvait donc pas reconnaître un smartphone ou un chargeur comme relevant du bac D3E : il les classait probablement dans `plastic` ou `metal` par erreur. Deux options existent pour combler ce trou, et les deux sont désormais implémentées, en complément l'une de l'autre plutôt qu'en alternative.

La première détecte le D3E en amont du modèle d'image, en s'appuyant sur la catégorie du produit telle que renvoyée par le scraping Jumia (rayon "Téléphonie", "Informatique", "Électroménager") ou sur des mots-clés du nom de produit. C'est la solution la plus rapide et la moins coûteuse, puisqu'elle ne demande aucune donnée supplémentaire. Elle est implémentée dans `src/upstream_filters.py`, qui expose `classify_before_image_model(nom_produit, categorie_produit, mot_cle_recherche)`, appelée par l'application avant même de charger le modèle.

La seconde apprend au modèle à reconnaître l'électronique comme une septième classe à part entière, via `src/prepare_electronics_data.py`. Ce script télécharge le dataset Kaggle `kaanerkez/waste-classfication-dataset` (17 catégories, dont plusieurs appareils électroniques), fusionne les catégories listées dans `config.ELECTRONICS_SOURCE_CATEGORIES` (battery, keyboard, microwave, mobile, mouse, pcb, player, printer, television, washing machine) en une seule classe `electronics`, puis sous-échantillonne le résultat pour revenir au même ordre de grandeur que la taille moyenne des 6 classes existantes, avant de le répartir en train/val/test au même endroit que le reste des données. Le modèle passe ainsi de 6 à 7 classes sans qu'aucun autre fichier n'ait besoin d'être modifié : `dataset.py` et `train.py` lisent les noms de dossiers réellement présents dans `data/splits/`, pas une liste figée dans le code.

Garder les deux mécanismes actifs en même temps est volontaire. Le filtre en amont reste utile comme premier passage rapide, avant même de charger le modèle ou l'image, et sert de garde-fou si un produit électronique a un nom ou une catégorie explicite. La classe entraînée prend le relais pour les cas où le texte ne suffit pas, en se basant directement sur l'apparence du produit.

## Verre d'emballage contre vaisselle

Un test manuel sur une photo réelle d'un verre à eau Jumia a révélé un second trou du même type que le D3E. Le brief précise explicitement que la poubelle VERTE ne concerne que les "verres d'emballage" (bouteilles, pots, bocaux) et interdit la vaisselle, une distinction qui a un sens réel puisque le verre de vaisselle a une composition chimique différente du verre d'emballage et contamine le circuit de recyclage s'il y est mélangé. Or la classe `glass` du dataset Kaggle ne fait pas cette distinction, donc le modèle ne peut structurellement pas différencier une bouteille en verre d'un verre à boire.

Sur ce test précis, le modèle a répondu `metal` avec seulement 0.41 de confiance, donc classé `INCERTAIN` grâce au seuil de confiance plutôt qu'une réponse fausse assurée, probablement à cause des reflets du verre transparent qui perturbent visuellement le modèle.

La solution recommandée est la même que pour le D3E, et elle est implémentée dans la même fonction : `classify_before_image_model()` renvoie `"MARRON"` si le nom du produit correspond à `config.VAISSELLE_KEYWORDS` ("verre à boire", "gobelet", "vaisselle"...). Le D3E et la vaisselle sont donc deux illustrations du même principe, gérées par le même mécanisme : le modèle d'image couvre bien les catégories représentées dans le dataset Kaggle, mais toute catégorie absente doit être filtrée avant lui, pas après.

## Résultats obtenus sur le premier modèle entraîné

Le premier entraînement complet atteint 85% de précision sur le jeu de test (six classes). Le détail par classe montre un modèle solide sur `cardboard` et `paper` (autour de 0.90 de précision), un peu plus fragile sur `metal` (précision de 0.75, confondu par moments avec `plastic`) et sur `trash` (rappel de 0.77, classe la plus petite et la plus hétérogène visuellement). La matrice de confusion complète est disponible dans `models/matrice_confusion.png`.

Des tests manuels sur de vraies photos Jumia confirment ce diagnostic : une canette a été classée `plastic` au lieu de `metal`, sans conséquence pratique puisque les deux sont mappées vers la même poubelle JAUNE dans `config.py`. Ce regroupement en 5 catégories officielles absorbe une partie des erreurs fines du modèle à 6 classes.

## Adaptation aux photos de catalogue (Jumia, Amazon...)

Le dataset Kaggle reste composé de photos de déchets isolés, pas de fiches produit e-commerce. Pour réduire davantage l'écart de domaine évoqué plus haut, `src/finetune.py` ajoute une étape optionnelle : repartir du modèle déjà entraîné et lui faire faire quelques passages supplémentaires, à très faible taux d'apprentissage, sur un petit jeu de vraies photos de catalogue organisées par classe dans `data/finetune/` (voir `data/finetune/README.md` pour la collecte et l'organisation des images).

Cette étape est volontairement séparée de l'entraînement principal et sauvegarde un fichier distinct, `models/modele_eco_sort_v2.h5`, à comparer avec le modèle officiel avant toute décision de remplacement. Le jeu de photos de catalogue n'est pas versionné sur Git (droit d'auteur des images produit), chaque membre de l'équipe le reconstitue localement en suivant les instructions du README du dossier.

## Images Jumia contenant plusieurs éléments

Certaines fiches produit Jumia peuvent afficher plusieurs objets sur une même photo (lots, accessoires inclus, visuels marketing avec logos et badges promo), une situation que le dataset Kaggle, composé de photos d'un seul déchet isolé, ne représente pas. Trois niveaux de réponse sont possibles, du plus simple au plus coûteux.

Le plus rentable pour ce projet est un seuil de confiance sur la prédiction : `predict.py` renvoie désormais un champ `certain` et classe le résultat en `INCERTAIN` si la probabilité de la classe prédite descend sous `config.CONFIDENCE_THRESHOLD` (0.6 par défaut). Une image ambiguë déclenche donc un résultat explicite plutôt qu'une réponse fausse donnée avec assurance.

Un second niveau, non implémenté pour l'instant, consisterait à recadrer l'image au centre avant redimensionnement pour limiter l'effet des badges et logos en périphérie.

Le niveau le plus robuste, la détection d'objets pour isoler chaque élément avant classification, est hors périmètre de ce projet : le dataset Kaggle ne fournit aucune annotation de position, et le délai ne permet pas d'entraîner un détecteur dédié. À documenter comme piste d'amélioration future.

## Comment reproduire l'entraînement

Toutes les commandes se lancent depuis le dossier `model/`.

```bash
pip install -r requirements.txt
python -m src.prepare_data                # télécharge les 6 classes de base et les sépare en train/val/test
python -m src.prepare_electronics_data    # ajoute la 7e classe "electronics" (D3E), équilibrée
python -m src.train                        # entraîne le modèle, sauvegarde model/models/modele_eco_sort.h5
python -m src.evaluate                     # rapport de classification + matrice de confusion
python -m src.predict chemin/vers/une/image.jpg
```

L'étape `prepare_electronics_data` est optionnelle : sans elle, le modèle s'entraîne normalement sur les 6 classes de base, et le D3E reste géré uniquement par le filtre en amont.

Voir `data/README.md` pour la configuration de l'accès à l'API Kaggle.

## Livrable

Le fichier `models/modele_eco_sort.h5` ainsi que `models/class_names.json` sont les deux fichiers attendus par l'application Streamlit pour le Jalon 2. Contrairement au dataset, ils sont volontairement versionnés sur Git : l'énoncé n'interdit que le dataset Kaggle et les environnements virtuels, et l'application doit pouvoir charger le modèle immédiatement après un `git clone`, sans étape d'entraînement ni téléchargement externe, pour que la commande `docker build` fonctionne du premier coup chez le professeur. Le checkpoint intermédiaire `*_best.keras` produit pendant l'entraînement n'est en revanche pas versionné, il est redondant avec le `.h5` final.
