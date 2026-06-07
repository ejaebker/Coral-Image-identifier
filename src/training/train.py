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

#params
img_height = 224
img_width = 224
batch_size = 32
eval_dir = "models/evaluation"

def load_data():
    #import data
    data_dir = "data/balanced" if os.path.exists("data/balanced") else "data/processed"
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
    
    return train_ds, validate_ds, class_names, num_classes

#model Define
def build_model(hp, num_classes):
  # Tunable hyperparameters
  dropout_rate = hp.Float('dropout', min_value=0.1, max_value=0.5, step=0.1)
  learning_rate = hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])

  #TRansfer learning base
  base_model = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3),
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
    
    # Preprocessing & Backbone
    tf.keras.layers.Rescaling(1./127.5, offset=-1),
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
    train_ds, validate_ds, class_names, num_classes = load_data()

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

    epochs = 20
    history = model.fit(
      train_ds,
      validation_data=validate_ds,
      epochs=epochs,
      callbacks=[early_stopping, cp_callback]
    )

    model.summary()

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
