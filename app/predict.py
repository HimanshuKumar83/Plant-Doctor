import os
import json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Resolve correct path
BASE_DIR = os.path.dirname(__file__)  # /app folder
MODEL_PATH = os.path.join(BASE_DIR, "../models/plant_disease_cnn.keras")
CLASS_INDICES_PATH = os.path.join(BASE_DIR, "../class_indices.json")

# Load model
model = load_model(MODEL_PATH)

# Load class indices
with open(CLASS_INDICES_PATH, "r") as f:
    class_indices = json.load(f)

index_to_class = {v: k for k, v in class_indices.items()}

def predict_leaf_image(img_path, target_size=(128, 128), top_k=3):
    img = image.load_img(img_path, target_size=target_size)
    img_arr = image.img_to_array(img) / 255.0
    img_arr = np.expand_dims(img_arr, axis=0)

    predictions = model.predict(img_arr)[0]
    top_indices = predictions.argsort()[-top_k:][::-1]

    result = []
    for idx in top_indices:
        class_name = index_to_class[idx]
        friendly_name = class_name.replace("___", " - ").replace("_", " ")
        confidence = float(predictions[idx])
        result.append({"class_name": class_name, "friendly_name": friendly_name, "confidence": confidence})

    return result
