"""Construction des pipelines tf.data à partir des dossiers d'images splittées."""
import tensorflow as tf
from tensorflow.keras import layers

from . import config

AUTOTUNE = tf.data.AUTOTUNE


def _augmentation_layer():
    return tf.keras.Sequential(
        [
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.08),
            layers.RandomZoom(0.15),
            layers.RandomContrast(0.1),
            layers.RandomBrightness(0.15),
        ],
        name="augmentation",
    )


def load_datasets(splits_dir=None):
    splits_dir = splits_dir or config.SPLIT_DATA_DIR

    train_ds = tf.keras.utils.image_dataset_from_directory(
        splits_dir / "train",
        image_size=config.IMG_SIZE,
        batch_size=config.BATCH_SIZE,
        label_mode="categorical",
        seed=config.SEED,
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        splits_dir / "val",
        image_size=config.IMG_SIZE,
        batch_size=config.BATCH_SIZE,
        label_mode="categorical",
        seed=config.SEED,
    )
    test_ds = tf.keras.utils.image_dataset_from_directory(
        splits_dir / "test",
        image_size=config.IMG_SIZE,
        batch_size=config.BATCH_SIZE,
        label_mode="categorical",
        seed=config.SEED,
        shuffle=False,
    )

    class_names = train_ds.class_names
    augment = _augmentation_layer()

    train_ds = train_ds.map(lambda x, y: (augment(x, training=True), y), num_parallel_calls=AUTOTUNE)
    train_ds = train_ds.prefetch(AUTOTUNE)
    val_ds = val_ds.prefetch(AUTOTUNE)
    test_ds = test_ds.prefetch(AUTOTUNE)

    return train_ds, val_ds, test_ds, class_names
