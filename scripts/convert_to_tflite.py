"""Convert the trained Keras model to a compact float16 TFLite model and verify parity."""

from pathlib import Path
import numpy as np
import tensorflow as tf

BASE_DIR = Path(__file__).resolve().parents[1]
KERAS_PATH = BASE_DIR / "models" / "plant_disease_cnn.keras"
TFLITE_PATH = BASE_DIR / "models" / "plant_disease_cnn.tflite"


def main() -> None:
    model = tf.keras.models.load_model(str(KERAS_PATH))
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]
    tflite_bytes = converter.convert()

    TFLITE_PATH.write_bytes(tflite_bytes)
    keras_mb = KERAS_PATH.stat().st_size / (1024 * 1024)
    tflite_mb = TFLITE_PATH.stat().st_size / (1024 * 1024)
    print(f"Converted {KERAS_PATH.name} ({keras_mb:.2f} MB) -> {TFLITE_PATH.name} ({tflite_mb:.2f} MB)")

    # Parity check on random deterministic input
    rng = np.random.default_rng(42)
    sample = rng.random((1, 128, 128, 3), dtype=np.float32)
    keras_out = model.predict(sample, verbose=0)[0]

    interp = tf.lite.Interpreter(model_path=str(TFLITE_PATH))
    interp.allocate_tensors()
    in_idx = interp.get_input_details()[0]["index"]
    out_idx = interp.get_output_details()[0]["index"]
    interp.set_tensor(in_idx, sample)
    interp.invoke()
    tflite_out = interp.get_tensor(out_idx)[0]

    max_diff = float(np.max(np.abs(keras_out - tflite_out)))
    print(f"Max output diff: {max_diff:.6f}, Top-1 match: {np.argmax(keras_out) == np.argmax(tflite_out)}")


if __name__ == "__main__":
    main()
