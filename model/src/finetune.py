"""Fine-tuning complementaire sur un petit jeu de vraies photos de catalogue
(Jumia, Amazon, etc.) pour reduire l'ecart de domaine avec le dataset Kaggle,
qui ne contient que des photos de dechets isoles.

Organisation attendue avant de lancer ce script :
    model/data/finetune/cardboard/*.jpg
    model/data/finetune/glass/*.jpg
    model/data/finetune/metal/*.jpg
    model/data/finetune/paper/*.jpg
    model/data/finetune/plastic/*.jpg
    model/data/finetune/trash/*.jpg

Une quinzaine d'images par classe suffit deja a orienter le modele vers le
style visuel des photos de catalogue (fond neutre, produit neuf, eclairage
studio). Voir data/finetune/README.md pour le detail.

Ce script part du modele deja entraine (modele_eco_sort.h5) et poursuit
l'entrainement quelques epoques a tres faible taux d'apprentissage, pour
eviter de "casser" ce qui a ete appris sur le gros dataset Kaggle. Il ne
remplace pas le modele officiel : il sauvegarde un fichier separe
(modele_eco_sort_v2.h5) a comparer avant de le promouvoir.

Usage (depuis le dossier model/) :
    python -m src.finetune
"""
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping

from . import config


def load_catalog_datasets():
    train_ds = tf.keras.utils.image_dataset_from_directory(
        config.FINETUNE_DATA_DIR,
        image_size=config.IMG_SIZE,
        batch_size=8,
        label_mode="categorical",
        validation_split=0.2,
        subset="training",
        seed=config.SEED,
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        config.FINETUNE_DATA_DIR,
        image_size=config.IMG_SIZE,
        batch_size=8,
        label_mode="categorical",
        validation_split=0.2,
        subset="validation",
        seed=config.SEED,
    )
    return (
        train_ds.prefetch(tf.data.AUTOTUNE),
        val_ds.prefetch(tf.data.AUTOTUNE),
        train_ds.class_names,
    )


def main():
    model = tf.keras.models.load_model(config.MODELS_DIR / "modele_eco_sort.h5")
    train_ds, val_ds, class_names = load_catalog_datasets()

    print(f"Classes detectees dans data/finetune : {class_names}")
    if class_names != config.CLASS_NAMES:
        print(
            "ATTENTION : l'ordre ou le nom des dossiers ne correspond pas exactement "
            f"a config.CLASS_NAMES ({config.CLASS_NAMES}). Verifie l'arborescence."
        )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(config.FINETUNE_CATALOG_LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    callbacks = [EarlyStopping(monitor="val_accuracy", patience=3, restore_best_weights=True)]
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=config.FINETUNE_CATALOG_EPOCHS,
        callbacks=callbacks,
    )

    val_loss, val_acc = model.evaluate(val_ds)
    print(f"Precision sur les images de catalogue tenues a l'ecart : {val_acc:.3f}")
    print("Cette mesure reste indicative : l'echantillon est volontairement petit.")

    output_path = config.MODELS_DIR / "modele_eco_sort_v2.h5"
    model.save(output_path)
    print(f"Modele affine sauvegarde : {output_path}")
    print(
        "Compare ses performances a modele_eco_sort.h5 (evaluate.py, tests manuels "
        "predict.py) avant de le promouvoir en remplacant le fichier officiel."
    )


if __name__ == "__main__":
    main()
