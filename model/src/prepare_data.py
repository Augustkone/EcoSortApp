"""Télécharge le dataset Kaggle et le répartit en train/val/test.

Prérequis :
    pip install kaggle split-folders
    un fichier kaggle.json valide placé dans ~/.kaggle/ (voir data/README.md)

Usage (depuis le dossier model/) :
    python -m src.prepare_data
"""
import subprocess
import zipfile

import splitfolders

from . import config

KAGGLE_DATASET = "asdasdasasdas/garbage-classification"


def download():
    config.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["kaggle", "datasets", "download", "-d", KAGGLE_DATASET, "-p", str(config.RAW_DATA_DIR)],
        check=True,
    )
    zip_path = next(config.RAW_DATA_DIR.glob("*.zip"))
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(config.RAW_DATA_DIR)
    zip_path.unlink()


def split(source_dir):
    splitfolders.ratio(
        str(source_dir),
        output=str(config.SPLIT_DATA_DIR),
        seed=config.SEED,
        ratio=(0.7, 0.15, 0.15),
    )


if __name__ == "__main__":
    download()
    # Ce dataset se dézippe avec un double dossier imbriqué, voir
    # config.GARBAGE_RAW_SUBDIR.
    split(config.GARBAGE_RAW_SUBDIR)
