"""Plant disease image inference service supporting TFLite (low-RAM) and Keras models."""

import io
import json
import os
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
from PIL import Image, ImageOps

BASE_DIR = Path(__file__).resolve().parents[2]
TFLITE_MODEL_PATH = Path(os.getenv("TFLITE_MODEL_PATH", BASE_DIR / "models" / "plant_disease_cnn.tflite"))
KERAS_MODEL_PATH = Path(os.getenv("KERAS_MODEL_PATH", BASE_DIR / "models" / "plant_disease_cnn.keras"))
CLASS_INDICES_PATH = Path(os.getenv("CLASS_INDICES_PATH", BASE_DIR / "class_indices.json"))
TARGET_SIZE = (128, 128)

_model_lock = threading.Lock()
_keras_model = None
_tflite_interpreter = None
_tflite_input_details = None
_tflite_output_details = None
_backend_type = "unloaded"


def _load_class_indices() -> Dict[str, int]:
    with open(CLASS_INDICES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


CLASS_INDICES = _load_class_indices()
INDEX_TO_CLASS = {int(v): k for k, v in CLASS_INDICES.items()}


def _split_class_label(class_name: str) -> Dict[str, str]:
    parts = class_name.split("___", 1)
    raw_crop = parts[0]
    raw_disease = parts[1] if len(parts) > 1 else "Unknown"
    crop_clean = raw_crop.replace("_(including_sour)", "").replace("_(maize)", "").replace(",_bell", " (Bell)").replace("_", " ")
    disease_clean = raw_disease.replace("_", " ").strip()
    return {
        "crop": crop_clean,
        "disease": disease_clean,
        "friendly_name": f"{crop_clean} - {disease_clean}",
    }


def get_supported_crops() -> List[str]:
    crops = sorted({_split_class_label(c)["crop"] for c in CLASS_INDICES.keys()})
    return crops


def _ensure_model_loaded() -> None:
    global _keras_model, _tflite_interpreter, _tflite_input_details, _tflite_output_details, _backend_type
    if _backend_type != "unloaded":
        return

    with _model_lock:
        if _backend_type != "unloaded":
            return

        if TFLITE_MODEL_PATH.exists():
            interpreter = None
            try:
                from ai_edge_litert.interpreter import Interpreter  # type: ignore
                interpreter = Interpreter(model_path=str(TFLITE_MODEL_PATH))
            except ImportError:
                try:
                    from tflite_runtime.interpreter import Interpreter  # type: ignore
                    interpreter = Interpreter(model_path=str(TFLITE_MODEL_PATH))
                except ImportError:
                    import tensorflow as tf
                    interpreter = tf.lite.Interpreter(model_path=str(TFLITE_MODEL_PATH))

            interpreter.allocate_tensors()
            _tflite_interpreter = interpreter
            _tflite_input_details = interpreter.get_input_details()
            _tflite_output_details = interpreter.get_output_details()
            _backend_type = "tflite"
            return

        if KERAS_MODEL_PATH.exists():
            from tensorflow.keras.models import load_model
            _keras_model = load_model(str(KERAS_MODEL_PATH))
            _backend_type = "keras"
            return

        raise FileNotFoundError(
            f"No model found at {TFLITE_MODEL_PATH} or {KERAS_MODEL_PATH}."
        )


def get_model_status() -> Dict[str, Any]:
    try:
        _ensure_model_loaded()
        return {
            "loaded": True,
            "backend": _backend_type,
            "num_classes": len(CLASS_INDICES),
        }
    except Exception as exc:
        return {"loaded": False, "backend": "error", "error": str(exc)}


def _preprocess_image_bytes(image_bytes: bytes) -> np.ndarray:
    img = Image.open(io.BytesIO(image_bytes))
    # Fix phone camera orientation from EXIF before resizing
    img = ImageOps.exif_transpose(img).convert("RGB")
    img = img.resize(TARGET_SIZE, Image.Resampling.BILINEAR)
    arr = np.asarray(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)


def _run_inference(input_tensor: np.ndarray) -> np.ndarray:
    _ensure_model_loaded()
    with _model_lock:
        if _backend_type == "tflite":
            _tflite_interpreter.set_tensor(_tflite_input_details[0]["index"], input_tensor)
            _tflite_interpreter.invoke()
            preds = _tflite_interpreter.get_tensor(_tflite_output_details[0]["index"])[0]
            return preds
        preds = _keras_model.predict(input_tensor, verbose=0)[0]
        return preds


def _crop_matches(class_name: str, crop_hint: str) -> bool:
    hint = crop_hint.lower().strip()
    if not hint:
        return True
    label_crop = _split_class_label(class_name)["crop"].lower()
    return hint in label_crop or label_crop in hint or hint.split()[0] in label_crop


def predict_from_bytes(
    image_bytes: bytes,
    top_k: int = 3,
    crop_hint: Optional[str] = None,
) -> Dict[str, Any]:
    """Run disease classification on uploaded image bytes and return structured predictions."""
    input_tensor = _preprocess_image_bytes(image_bytes)
    probs = _run_inference(input_tensor)

    top_indices = probs.argsort()[-top_k:][::-1]
    predictions: List[Dict[str, Any]] = []
    for idx in top_indices:
        class_name = INDEX_TO_CLASS[int(idx)]
        meta = _split_class_label(class_name)
        predictions.append(
            {
                "class_name": class_name,
                "friendly_name": meta["friendly_name"],
                "crop": meta["crop"],
                "disease": meta["disease"],
                "is_healthy": "___healthy" in class_name,
                "confidence": round(float(probs[idx]), 4),
            }
        )

    best = predictions[0]
    crop_mismatch = bool(crop_hint and not _crop_matches(best["class_name"], crop_hint))

    crop_filtered_best = None
    if crop_mismatch and crop_hint:
        matching_indices = [
            idx for idx, cname in INDEX_TO_CLASS.items() if _crop_matches(cname, crop_hint)
        ]
        if matching_indices:
            best_match_idx = max(matching_indices, key=lambda i: float(probs[i]))
            cname = INDEX_TO_CLASS[best_match_idx]
            meta = _split_class_label(cname)
            crop_filtered_best = {
                "class_name": cname,
                "friendly_name": meta["friendly_name"],
                "crop": meta["crop"],
                "disease": meta["disease"],
                "is_healthy": "___healthy" in cname,
                "confidence": round(float(probs[best_match_idx]), 4),
            }

    return {
        "predictions": predictions,
        "low_confidence": best["confidence"] < 0.60,
        "crop_mismatch": crop_mismatch,
        "crop_filtered_suggestion": crop_filtered_best,
        "model_backend": _backend_type,
    }
