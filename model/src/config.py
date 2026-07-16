"""Configuration centrale du pipeline de reconnaissance d'image EcoSort."""
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"           # dataset Kaggle brut, jamais versionné
SPLIT_DATA_DIR = DATA_DIR / "splits"      # train/val/test générés localement
# Petit jeu complémentaire de vraies photos de catalogue (Jumia, Amazon...)
# organisé en sous-dossiers par classe, voir data/finetune/README.md
FINETUNE_DATA_DIR = DATA_DIR / "finetune"
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Image
IMG_SIZE = (224, 224)          # taille attendue par MobileNetV2
BATCH_SIZE = 32
SEED = 42

# Classes natives du dataset Kaggle "Garbage Classification"
CLASS_NAMES = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]
# Convertit les codes du modèle IA (français, majuscules) vers les codes UI (utils.py)

# Correspondance classes du modèle -> poubelles officielles du projet EcoSort
CLASS_TO_BIN = {
    "plastic": "JAUNE",
    "metal": "JAUNE",
    "cardboard": "JAUNE",
    "glass": "VERTE",
    "paper": "BLEUE",
    "trash": "MARRON",
}
# NB : la catégorie "D3E" (électronique) n'existe pas dans ce dataset.
# Elle doit être détectée en amont (catégorie produit Jumia ou mots-clés du nom
# de produit) avant même d'appeler le modèle d'image. Voir README.md et
# src/upstream_filters.py pour l'implémentation prête à brancher côté app.

# Mots-clés (nom de produit) et catégories Jumia signalant du D3E : à détecter
# avant d'appeler le modèle d'image, jamais après.
D3E_KEYWORDS = [
    "telephone", "téléphone", "smartphone", "ecouteur", "écouteur",
    "chargeur", "batterie", "pile", "mixeur", "montre", "ordinateur",
    "tablette", "casque", "cable", "câble", "console", "imprimante",
    "aspirateur", "bouilloire", "rasoir electrique", "rasoir électrique",
    "ventilateur", "climatiseur", "refrigerateur", "réfrigérateur",
    "television", "télévision", "enceinte", "haut-parleur", "camera",
    "caméra", "manette", "clavier", "souris", "routeur", "powerbank",
]
D3E_CATEGORIES = [
    "telephonie", "téléphonie", "informatique", "electromenager",
    "électroménager", "tv, son & image", "tv son image", "gaming",
]

# Mots-clés signalant de la vaisselle (verre à boire, gobelet...), à distinguer
# du verre d'emballage (bouteille, pot, bocal) qui seul va en poubelle VERTE.
VAISSELLE_KEYWORDS = [
    "verre a boire", "verre à boire", "gobelet", "vaisselle",
    "service de table", "assiette", "tasse", "mug",
]

# Seuil de confiance minimal pour valider une prédiction. En dessous, le résultat
# est considéré comme incertain plutôt que d'imposer une réponse fausse avec
# assurance : cas typique d'une image Jumia contenant plusieurs produits, un
# emballage multi-matières, ou un fort encombrement visuel (logos, badges promo).
CONFIDENCE_THRESHOLD = 0.6

# Entraînement
INITIAL_EPOCHS = 15
FINE_TUNE_EPOCHS = 10
FINE_TUNE_AT_LAYER = 100          # à partir de quelle couche de MobileNetV2 on dégèle
LEARNING_RATE = 1e-3
FINE_TUNE_LEARNING_RATE = 1e-5

# Fine-tuning complémentaire sur les photos de catalogue (voir src/finetune.py).
# Taux d'apprentissage très bas et peu d'époques : le jeu de données est petit,
# le but est d'orienter le modèle, pas de le réentraîner en profondeur.
FINETUNE_CATALOG_EPOCHS = 8
FINETUNE_CATALOG_LEARNING_RATE = 1e-6
