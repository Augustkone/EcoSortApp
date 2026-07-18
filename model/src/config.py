"""Configuration centrale du pipeline de reconnaissance d'image EcoSort."""
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"           # dataset Kaggle brut, jamais versionné
# Sous-dossier reel une fois le zip "Garbage Classification" decompresse
# (double dossier imbrique propre a ce dataset).
GARBAGE_RAW_SUBDIR = RAW_DATA_DIR / "Garbage classification" / "Garbage classification"
SPLIT_DATA_DIR = DATA_DIR / "splits"      # train/val/test générés localement
# Dataset Kaggle complementaire pour la classe "electronics" (D3E), voir
# src/prepare_electronics_data.py
ELECTRONICS_RAW_DIR = DATA_DIR / "raw_electronics"
# Petit jeu complémentaire de vraies photos de catalogue (Jumia, Amazon...)
# organisé en sous-dossiers par classe, voir data/finetune/README.md
FINETUNE_DATA_DIR = DATA_DIR / "finetune"
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Image
IMG_SIZE = (224, 224)          # taille attendue par MobileNetV2
BATCH_SIZE = 32
SEED = 42

# Classes natives du dataset Kaggle "Garbage Classification", plus
# "electronics" ajoutee via src/prepare_electronics_data.py (dataset Kaggle
# "Waste Classification Dataset" de kaanerkez). Cette liste documente les
# classes attendues, mais l'entrainement (dataset.py/train.py) lit les noms
# de dossiers reellement presents dans data/splits/, donc pas besoin de
# modifier train.py quand une classe est ajoutee ou retiree ici.
CLASS_NAMES = ["cardboard", "glass", "metal", "paper", "plastic", "trash", "electronics"]
# Convertit les codes du modèle IA (français, majuscules) vers les codes UI (utils.py)

# Correspondance classes du modèle -> poubelles officielles du projet EcoSort
CLASS_TO_BIN = {
    "plastic": "JAUNE",
    "metal": "JAUNE",
    "cardboard": "JAUNE",
    "glass": "VERTE",
    "paper": "BLEUE",
    "trash": "MARRON",
    "electronics": "D3E",
}
# NB : la classe "electronics" est desormais entrainee (voir
# src/prepare_electronics_data.py), en complement du filtre en amont
# src/upstream_filters.py qui reste utile comme premier passage rapide,
# sans attendre le chargement du modele ni l'image.

# Dataset Kaggle "Waste Classification Dataset" (kaanerkez), utilise pour
# ajouter des exemples reels d'appareils electroniques (D3E) au dataset de
# base, qui n'en contient aucun. Les categories listees sont fusionnees en
# une seule classe "electronics", puis sous-echantillonnees pour rester du
# meme ordre de grandeur que les 6 autres classes (equilibrage).
ELECTRONICS_KAGGLE_DATASET = "kaanerkez/waste-classfication-dataset"
ELECTRONICS_SOURCE_CATEGORIES = [
    "battery", "keyboard", "microwave", "mobile", "mouse", "pcb",
    "player", "printer", "television", "washing machine",
]

# Mots-clés (nom de produit) et catégories Jumia signalant du D3E : à détecter
# avant d'appeler le modèle d'image, jamais après.
D3E_KEYWORDS = [
    "telephone", "téléphone", "smartphone", "gsm",
    "ecouteur", "écouteur", "earbuds", "airpods",
    "chargeur", "batterie", "powerbank", "power bank",
    "mixeur", "blender", "smartwatch",
    "ordinateur portable", "laptop", "pc portable", "tablette", "tablet",
    "casque audio", "cable usb", "câble usb", "cable hdmi",
    "console de jeu", "manette", "playstation", "xbox", "nintendo",
    "imprimante", "scanner",
    "aspirateur", "bouilloire electrique", "bouilloire électrique",
    "grille-pain", "micro-onde",
    "rasoir electrique", "rasoir électrique", "epilateur", "épilateur",
    "ventilateur electrique", "ventilateur électrique",
    "climatiseur", "refrigerateur", "réfrigérateur",
    "congelateur", "congélateur",
    "television", "télévision", "ecran pc", "écran pc", "moniteur",
    "enceinte bluetooth", "haut-parleur bluetooth",
    "camera", "caméra", "appareil photo", "webcam",
    "clavier", "souris", "routeur", "modem wifi",
    "fer a repasser", "fer à repasser",
    "friteuse electrique", "friteuse électrique",
    "cafetiere", "cafetière", "machine a cafe", "machine à café",
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
