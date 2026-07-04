#dependancies
import tensorflow as tf
import matplotlib.pyplot as plt
import keras_tuner as kt
import os
import json
try:
    from . import evaluator
except ImportError:
    import evaluator

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping 

from sklearn.utils import class_weight
import numpy as np

#params
img_height = 224
img_width = 224
batch_size = 32
eval_dir = "models/evaluation"

def load_data():
    #import data - Use PROCESSED instead of balanced
    data_dir = "data/processed"
    os.makedirs("models", exist_ok=True)
    os.makedirs(eval_dir, exist_ok=True)

    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset='training',
        seed=123,
        image_size=(img_height,img_width),
        batch_size=batch_size
    )
    class_names = train_ds.class_names
    num_classes = len(class_names)
    
    # --- CALCULATE CLASS WEIGHTS ---
    # We get labels from the training dataset to calculate distribution
    y_train = np.concatenate([y for x, y in train_ds], axis=0)
    weights = class_weight.compute_class_weight(
        class_weight='balanced',
        classes=np.unique(y_train),
        y=y_train
    )
    class_weight_dict = dict(enumerate(weights))
    print(f"Calculated Class Weights: {class_weight_dict}")

    # Save class names for the API to use
    with open("models/classes.json", "w") as f:
        json.dump(class_names, f)
    print(f"Saved {num_classes} class labels to models/classes.json")
    
    validate_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset='validation',
        seed=123,
        image_size=(img_height,img_width),
        batch_size=batch_size
    )
    
    #buffered prefetch
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
    validate_ds = validate_ds.cache().prefetch(buffer_size=AUTOTUNE)
    
    return train_ds, validate_ds, class_names, num_classes, class_weight_dict

#model Define
def build_model(hp, num_classes):
  # Tunable hyperparameters
  dropout_rate = hp.Float('dropout', min_value=0.1, max_value=0.5, step=0.1)
  learning_rate = hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])

  # Transfer learning base - EfficientNetV2-B0
  base_model = tf.keras.applications.EfficientNetV2B0(input_shape=(224, 224, 3),
                                                     include_top=False,
                                                     weights='imagenet')
  base_model.trainable = False

  model = tf.keras.Sequential([
    # Data Augmentation Layers
    tf.keras.layers.RandomFlip("horizontal", input_shape=(224, 224, 3)),
    tf.keras.layers.RandomRotation(0.1),
    tf.keras.layers.RandomZoom(0.1),
    tf.keras.layers.RandomBrightness(factor=0.2),
    tf.keras.layers.RandomContrast(factor=0.2),
    
    # Backbone (EfficientNetV2 has built-in normalization layer, so we do not rescale)
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dropout(dropout_rate),
    tf.keras.layers.Dense(num_classes, name='outputs')
  ])

  model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy'])
  
  return model

def run_training():
    train_ds, validate_ds, class_names, num_classes, class_weight_dict = load_data()

    #epoch tune
    early_stopping=tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        min_delta=0,
        patience=3,
        verbose=0,
        mode='auto',
        baseline=None,
        restore_best_weights=True,
        start_from_epoch=0
    )

    # Initialize Tuner
    tuner = kt.Hyperband(
        lambda hp: build_model(hp, num_classes),
        objective='val_accuracy',
        max_epochs=10,
        directory='models/tuner_logs',
        project_name='coral_classification'
    )

    # Execute Tuning
    print("\nStarting Hyperparameter Tuning...")
    tuner.search(train_ds, validation_data=validate_ds, callbacks=[early_stopping])

    # Get best hyperparameters and final train
    best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]
    print(f"\nBest Dropout: {best_hps.get('dropout')}")
    print(f"Best Learning Rate: {best_hps.get('learning_rate')}")

    model = tuner.hypermodel.build(best_hps)

    # Model Checkpoint for best weights
    checkpoint_path = "models/coral_model_best.keras"
    cp_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_path,
        save_best_only=True,
        monitor='val_accuracy',
        mode='max'
    )

    epochs = 15
    print("\n--- Stage 1: Training the Classification Head ---")
    history = model.fit(
      train_ds,
      validation_data=validate_ds,
      epochs=epochs,
      callbacks=[early_stopping, cp_callback],
      class_weight=class_weight_dict
    )

    # Stage 2: Fine-Tuning the Backbone
    base_model = None
    for layer in model.layers:
        if 'efficientnetv2' in layer.name:
            base_model = layer
            break

    if base_model:
        print("\n--- Stage 2: Fine-Tuning the EfficientNetV2 Backbone ---")
        base_model.trainable = True
        
        # Freeze the bottom 200 layers, leaving only the top layers unfrozen for fine-tuning
        # (EfficientNetV2-B0 has ~270 layers total)
        fine_tune_at = 200
        for layer in base_model.layers[:fine_tune_at]:
            layer.trainable = False
        for layer in base_model.layers[fine_tune_at:]:
            layer.trainable = True

        # Recompile with a very low learning rate to avoid destroying pre-trained weights
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy']
        )

        early_stopping_fine = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=3,
            restore_best_weights=True
        )

        fine_tune_epochs = 10
        history_fine = model.fit(
            train_ds,
            validation_data=validate_ds,
            epochs=fine_tune_epochs,
            callbacks=[early_stopping_fine, cp_callback],
            class_weight=class_weight_dict
        )
        history = history_fine # Use fine-tuning history for final evaluations
    else:
        print("\n[WARNING] Could not locate EfficientNetV2 layer for fine-tuning. Skipping Stage 2.")

    model.summary()

    # Load the absolute best weights saved by checkpoint before exporting
    if os.path.exists(checkpoint_path):
        print(f"Loading best weights from {checkpoint_path}...")
        model = tf.keras.models.load_model(checkpoint_path)

    # Export to TFLite for deployment
    print("\nExporting model to TFLite...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    with open('models/coral_model.tflite', 'wb') as f:
        f.write(tflite_model)
    print("Model saved to models/coral_model.tflite")

    # Evaluate model performance
    evaluator.evaluate_model(model, history, validate_ds, class_names, output_dir=eval_dir)

if __name__ == "__main__":
    run_training()
