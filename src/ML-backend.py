#dependancies
import tensorflow as tf
import matplotlib.pyplot as plt
import evaluator

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping 

#params
img_height =224
img_width = 224
batch_size =32

#import data
data_dir="data/processed"

train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset='training',
    seed=123,
    image_size=(img_height,img_width),
    batch_size=batch_size
)
class_names = train_ds.class_names
validate_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset='validation',
    seed=123,
    image_size=(img_height,img_width),
    batch_size=batch_size
)
#data augmentation
data_augmentation = keras.Sequential(
  [
    layers.RandomFlip("horizontal",
                      input_shape=(img_height,
                                  img_width,
                                  3)),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
    layers.RandomBrightness(factor=0.2),
    layers.RandomContrast(factor=0.2)
  ]
)
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

#buffered prefetch
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
validate_ds = validate_ds.cache().prefetch(buffer_size=AUTOTUNE)

#model Define
num_classes = 4
normalization_layer = tf.keras.layers.Rescaling(1./127.5, offset=-1)

#TRansfer learning
base_model = tf.keras.applications.MobileNetV2(input_shape=(img_height, img_width, 3),
                                               include_top=False,
                                               weights='imagenet')
base_model.trainable = False

model = tf.keras.Sequential([
  data_augmentation,   
  tf.keras.layers.Rescaling(1./127.5, offset=-1),
  base_model,
  tf.keras.layers.GlobalAveragePooling2D(),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(num_classes, name='outputs')
])

model.compile(
  optimizer='adam',
  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
  metrics=['accuracy'])

epochs = 20
history=model.fit(
  train_ds,
  validation_data=validate_ds,
  epochs=epochs,
  callbacks=[early_stopping]
)

model.summary()

# Evaluate model performance
evaluator.evaluate_model(model, history, validate_ds, class_names)