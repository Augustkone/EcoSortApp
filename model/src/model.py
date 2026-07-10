"""Définition du modèle par transfer learning (MobileNetV2)."""
from typing import Optional

from tensorflow.keras import layers, Model
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

from . import config


def build_model(num_classes: int, fine_tune_at: Optional[int] = None) -> Model:
    """Construit le modèle. fine_tune_at=None -> base gelée (phase 1).
    fine_tune_at=<int> -> dégèle les couches à partir de cet index (phase 2)."""
    base_model = MobileNetV2(
        input_shape=config.IMG_SIZE + (3,),
        include_top=False,
        weights="imagenet",
    )

    if fine_tune_at is None:
        base_model.trainable = False
    else:
        base_model.trainable = True
        for layer in base_model.layers[:fine_tune_at]:
            layer.trainable = False

    inputs = layers.Input(shape=config.IMG_SIZE + (3,))
    x = preprocess_input(inputs)
    x = base_model(x)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(128, activation="relu")(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    return Model(inputs, outputs, name="ecosort_mobilenetv2")
