"""Entraînement du modèle de reconnaissance d'image EcoSort.

Usage (depuis le dossier model/) :
    python -m src.train
"""
import json

import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

from . import config
from .dataset import load_datasets
from .model import build_model


def main():
    train_ds, val_ds, test_ds, class_names = load_datasets()
    num_classes = len(class_names)
    print(f"Classes détectées : {class_names}")

    checkpoint_path = config.MODELS_DIR / "modele_eco_sort_best.keras"
    callbacks = [
        EarlyStopping(monitor="val_accuracy", patience=4, restore_best_weights=True),
        ModelCheckpoint(str(checkpoint_path), monitor="val_accuracy", save_best_only=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2),
    ]

    print("Phase 1 : entraînement de la tête de classification (base MobileNetV2 gelée)")
    model = build_model(num_classes)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(config.LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    model.fit(train_ds, validation_data=val_ds, epochs=config.INITIAL_EPOCHS, callbacks=callbacks)

    print("Phase 2 : fine-tuning des dernières couches de MobileNetV2")
    fine_tuned = build_model(num_classes, fine_tune_at=config.FINE_TUNE_AT_LAYER)
    fine_tuned.set_weights(model.get_weights())
    fine_tuned.compile(
        optimizer=tf.keras.optimizers.Adam(config.FINE_TUNE_LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    fine_tuned.fit(train_ds, validation_data=val_ds, epochs=config.FINE_TUNE_EPOCHS, callbacks=callbacks)

    test_loss, test_acc = fine_tuned.evaluate(test_ds)
    print(f"Précision sur le jeu de test : {test_acc:.3f}")

    final_path = config.MODELS_DIR / "modele_eco_sort.h5"
    fine_tuned.save(final_path)
    with open(config.MODELS_DIR / "class_names.json", "w", encoding="utf-8") as f:
        json.dump(class_names, f, ensure_ascii=False, indent=2)

    print(f"Modèle sauvegardé : {final_path}")


if __name__ == "__main__":
    main()
