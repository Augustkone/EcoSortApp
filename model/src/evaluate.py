"""Évalue le modèle entraîné sur le jeu de test et génère une matrice de confusion.

Usage (depuis le dossier model/) :
    python -m src.evaluate
"""
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

from . import config
from .dataset import load_datasets


def main():
    _, _, test_ds, class_names = load_datasets()

    model = tf.keras.models.load_model(config.MODELS_DIR / "modele_eco_sort.h5")

    y_true, y_pred = [], []
    for images, labels in test_ds:
        preds = model.predict(images, verbose=0)
        y_true.extend(np.argmax(labels.numpy(), axis=1))
        y_pred.extend(np.argmax(preds, axis=1))

    print(classification_report(y_true, y_pred, target_names=class_names))

    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(len(class_names)))
    ax.set_yticks(range(len(class_names)))
    ax.set_xticklabels(class_names, rotation=45, ha="right")
    ax.set_yticklabels(class_names)
    ax.set_xlabel("Prédit")
    ax.set_ylabel("Réel")
    for i in range(len(class_names)):
        for j in range(len(class_names)):
            ax.text(j, i, cm[i, j], ha="center", va="center")
    fig.colorbar(im)
    fig.tight_layout()
    fig.savefig(config.MODELS_DIR / "matrice_confusion.png")
    print(f"Matrice de confusion sauvegardée dans {config.MODELS_DIR / 'matrice_confusion.png'}")


if __name__ == "__main__":
    main()
