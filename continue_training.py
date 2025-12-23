import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Paths
MODEL_PATH = "models/plant_disease_cnn.keras"
DATASET_PATH = "dataset"

IMAGE_SIZE = (128, 128)
BATCH_SIZE = 32

# Load model
model = tf.keras.models.load_model(MODEL_PATH)
print("Loaded saved model successfully!")

# Data generators
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True,
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_gen = train_datagen.flow_from_directory(
    f"{DATASET_PATH}/train",
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

val_gen = val_datagen.flow_from_directory(
    f"{DATASET_PATH}/valid",
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

# Continue training for more epochs
EPOCHS_TO_ADD = 2   # ⬅ Change this number (2 more epochs)
history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS_TO_ADD
)

# Save again
model.save(MODEL_PATH)
print("Model retrained and saved!")
