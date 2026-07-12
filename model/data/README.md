# Configuration de l'accès Kaggle

Le script `src/prepare_data.py` télécharge automatiquement le dataset via l'API Kaggle. Il faut au préalable créer un jeton d'API.

1. Se connecter sur kaggle.com, ouvrir les paramètres du compte, puis "Create New Token" dans la section API. Un fichier `kaggle.json` se télécharge.
2. Placer ce fichier dans `~/.kaggle/kaggle.json` (Linux/Mac) ou `C:\Users\<utilisateur>\.kaggle\kaggle.json` (Windows).
3. Installer le client : `pip install kaggle`.
4. Lancer `python -m src.prepare_data` depuis le dossier `model/`.

Ce dossier `data/` (contenu de `raw/` et `splits/`) ne doit jamais être poussé sur GitHub : il est exclu via le `.gitignore` à la racine du dépôt. Chaque membre de l'équipe régénère les données localement avec les commandes ci-dessus.
