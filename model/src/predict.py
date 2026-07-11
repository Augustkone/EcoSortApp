"""Prédit la catégorie de tri pour une image donnée.

Usage (depuis le dossier model/) :
    python -m src.predict chemin/vers/image.jpg
"""
import json
import sys

import numpy as np
import tensorflow as tf

from . import config


def load_class_names():
    with open(config.MODELS_DIR / "class_names.json", encoding="utf-8") as f:
        return json.load(f)


def predict_image(image_path: str, model=None, class_names=None) -> dict:
    if model is None:
        model = tf.keras.models.load_model(config.MODELS_DIR / "modele_eco_sort.h5")
    if class_names is None:
        class_names = load_class_names()

    img = tf.keras.utils.load_img(image_path, target_size=config.IMG_SIZE)
    arr = tf.keras.utils.img_to_array(img)
    arr = np.expand_dims(arr, axis=0)  # le prétraitement MobileNetV2 est intégré au modèle

    predictions = model.predict(arr, verbose=0)[0]
    idx = int(np.argmax(predictions))
    predicted_class = class_names[idx]
    confidence = float(predictions[idx])
    is_certain = confidence >= config.CONFIDENCE_THRESHOLD

    if is_certain:
        bin_color = config.CLASS_TO_BIN.get(predicted_class, "INCONNU (probablement D3E)")
    else:
        # Confiance trop faible : probablement une image ambiguë (plusieurs
        # produits, matières mélangées). On ne force pas une réponse fausse.
        bin_color = "INCERTAIN"

    return {
        "classe": predicted_class,
        "confiance": round(confidence, 4),
        "poubelle": bin_color,
        "certain": is_certain,
    }


if __name__ == "__main__":
    result = predict_image(sys.argv[1])
    print(result)
