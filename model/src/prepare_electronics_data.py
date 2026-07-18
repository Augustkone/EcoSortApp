"""Ajoute une septieme classe "electronics" (D3E) au jeu d'entrainement.

Le dataset Kaggle "Garbage Classification" ne contient aucun appareil
electronique. On complete ici avec le dataset Kaggle "Waste Classification
Dataset" (kaanerkez/waste-classfication-dataset), qui couvre 17 categories
dont plusieurs types d'appareils electroniques (voir
config.ELECTRONICS_SOURCE_CATEGORIES). Ces categories sont fusionnees en une
seule classe "electronics", puis sous-echantillonnees pour rester du meme
ordre de grandeur que les 6 classes existantes (equilibrage), avant d'etre
repartie en train/val/test au meme endroit que le reste des donnees.

Prerequis : avoir deja lance `python -m src.prepare_data` au moins une fois,
pour que data/splits/{train,val,test}/<classe>/ existe deja pour les 6
classes de base (utilise comme reference pour calculer la taille cible).

Usage (depuis le dossier model/) :
    python -m src.prepare_electronics_data
"""
import random
import shutil
import subprocess
import zipfile
from pathlib import Path

from . import config


def download():
    config.ELECTRONICS_RAW_DIR.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "kaggle", "datasets", "download",
            "-d", config.ELECTRONICS_KAGGLE_DATASET,
            "-p", str(config.ELECTRONICS_RAW_DIR),
        ],
        check=True,
    )
    zip_path = next(config.ELECTRONICS_RAW_DIR.glob("*.zip"))
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(config.ELECTRONICS_RAW_DIR)
    zip_path.unlink()


def _normalise_nom(nom: str) -> str:
    return "".join(c for c in nom.lower() if c.isalnum())


def _find_category_dir(root: Path, nom_categorie: str) -> Path:
    """Cherche un dossier par nom, insensible a la casse, aux espaces et aux
    underscores (le zip peut nommer les dossiers de plusieurs facons)."""
    cible = _normalise_nom(nom_categorie)
    candidats = [p for p in root.rglob("*") if p.is_dir() and _normalise_nom(p.name) == cible]
    if not candidats:
        raise FileNotFoundError(
            f"Categorie '{nom_categorie}' introuvable sous {root}. "
            "Verifie le nom exact des dossiers avec `ls` (ou dir) une fois "
            "le dataset decompresse, et adapte config.ELECTRONICS_SOURCE_CATEGORIES."
        )
    return candidats[0]


def _taille_moyenne_classes_existantes() -> int:
    """Nombre moyen d'images par classe dans le dataset de base (avant
    split), pour caler la taille de la classe electronics sur le meme ordre
    de grandeur et rester equilibre."""
    if not config.GARBAGE_RAW_SUBDIR.exists():
        raise FileNotFoundError(
            "data/raw introuvable : lance d'abord `python -m src.prepare_data` "
            "pour telecharger les 6 classes de base avant d'ajouter electronics."
        )
    tailles = [
        len(list(d.glob("*")))
        for d in config.GARBAGE_RAW_SUBDIR.iterdir()
        if d.is_dir()
    ]
    return int(sum(tailles) / len(tailles)) if tailles else 400


def build_electronics_class():
    pool_dir = config.DATA_DIR / "electronics_pool"
    if pool_dir.exists():
        shutil.rmtree(pool_dir)
    pool_dir.mkdir(parents=True)

    for categorie in config.ELECTRONICS_SOURCE_CATEGORIES:
        source = _find_category_dir(config.ELECTRONICS_RAW_DIR, categorie)
        prefixe = categorie.replace(" ", "_")
        images_categorie = [p for p in source.glob("*") if p.is_file()]
        for i, image in enumerate(images_categorie):
            shutil.copy(image, pool_dir / f"{prefixe}_{i:04d}{image.suffix}")
        print(f"{categorie} : {len(images_categorie)} images ajoutees au pool.")

    toutes_images = list(pool_dir.glob("*"))
    print(f"Total avant equilibrage : {len(toutes_images)} images electroniques.")

    cible = _taille_moyenne_classes_existantes()
    print(f"Taille moyenne des 6 classes existantes : {cible} images.")

    random.seed(config.SEED)
    if len(toutes_images) > cible:
        toutes_images = random.sample(toutes_images, cible)
        print(f"Sous-echantillonnage a {cible} images pour rester equilibre.")
    else:
        print(
            "Le pool electronics est deja plus petit ou egal a la taille "
            "cible, aucun sous-echantillonnage necessaire."
        )

    # Repartition 70/15/15, coherente avec prepare_data.py
    random.shuffle(toutes_images)
    n = len(toutes_images)
    n_train, n_val = int(n * 0.7), int(n * 0.15)
    repartition = {
        "train": toutes_images[:n_train],
        "val": toutes_images[n_train:n_train + n_val],
        "test": toutes_images[n_train + n_val:],
    }

    for nom_split, images in repartition.items():
        dest_dir = config.SPLIT_DATA_DIR / nom_split / "electronics"
        dest_dir.mkdir(parents=True, exist_ok=True)
        for image in images:
            shutil.copy(image, dest_dir / image.name)
        print(f"{nom_split} : {len(images)} images electronics ajoutees.")

    shutil.rmtree(pool_dir)


if __name__ == "__main__":
    download()
    build_electronics_class()
    print(
        "\nClasse 'electronics' ajoutee dans data/splits/{train,val,test}/electronics/.\n"
        "Relance `python -m src.train` pour reentrainer avec 7 classes."
    )
