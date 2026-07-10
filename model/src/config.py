"""Configuration centrale du pipeline de reconnaissance d'image EcoSort."""
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"           # dataset Kaggle brut, jamais versionné
SPLIT_DATA_DIR = DATA_DIR / "splits"      # train/val/test générés localement
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Image
IMG_SIZE = (224, 224)          # taille attendue par MobileNetV2
BATCH_SIZE = 32
SEED = 42

# Classes natives du dataset Kaggle "Garbage Classification"
CLASS_NAMES = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]

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
# de produit) avant même d'appeler le modèle d'image. Voir README.md.

# Entraînement
INITIAL_EPOCHS = 15
FINE_TUNE_EPOCHS = 10
FINE_TUNE_AT_LAYER = 100          # à partir de quelle couche de MobileNetV2 on dégèle
LEARNING_RATE = 1e-3
FINE_TUNE_LEARNING_RATE = 1e-5
