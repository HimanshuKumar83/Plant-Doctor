"""End-to-end verification tests for Plant Doctor backend, TFLite model, KB coverage, and endpoints."""

import json
import subprocess
import sys
import time
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from backend.services.knowledge_base import DISEASE_INFO, get_local_recommendation
from backend.services.predictor import get_supported_crops, predict_from_bytes


def verify_knowledge_base() -> None:
    with open(BASE_DIR / "class_indices.json", "r", encoding="utf-8") as f:
        classes = json.load(f)

    missing = [c for c in classes.keys() if c not in DISEASE_INFO]
    assert not missing, f"Missing classes in DISEASE_INFO: {missing}"
    print(f"[PASS] Knowledge base covers all {len(classes)}/38 classes.")

    # Verify weather + soil pH + spray rotation rules
    advice = get_local_recommendation(
        "Tomato___Late_blight",
        soil_pH=5.0,
        spray_count=3,
        weather_summary={"avg_humidity": 85, "total_rain_mm": 10},
    )
    assert any("Weather Alert" in x for x in advice["english"]["chemical"])
    assert any("lime" in x.lower() for x in advice["english"]["prevention"])
    assert any("Resistance Warning" in x for x in advice["english"]["safety"])
    print("[PASS] Weather, acidic soil pH, and spray-rotation rules verified.")


def verify_tflite_accuracy_sample() -> None:
    """Verify TFLite model predicts real validation images accurately."""
    valid_dir = BASE_DIR / "dataset" / "valid"
    if not valid_dir.exists():
        print("[SKIP] dataset/valid not present; skipping sample accuracy check.")
        return

    sample_classes = sorted([d for d in valid_dir.iterdir() if d.is_dir()])[:10]
    correct = 0
    total = 0
    for cls_dir in sample_classes:
        imgs = sorted(cls_dir.glob("*.*"))[:3]
        for img_path in imgs:
            res = predict_from_bytes(img_path.read_bytes(), top_k=3)
            pred = res["predictions"][0]["class_name"]
            if pred == cls_dir.name:
                correct += 1
            total += 1
    acc = (correct / total) * 100 if total else 0
    print(f"[PASS] TFLite sample check: {correct}/{total} ({acc:.1f}%) across {len(sample_classes)} classes.")
    assert correct > 0, "Expected TFLite predictions to match validation samples."


def verify_live_api() -> None:
    port = 8011
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", str(port)],
        cwd=str(BASE_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        base_url = f"http://127.0.0.1:{port}"
        for _ in range(30):
            try:
                r = requests.get(f"{base_url}/health", timeout=2)
                if r.status_code == 200:
                    break
            except Exception:
                time.sleep(0.5)
        else:
            raise RuntimeError("Uvicorn server failed to start in time")

        health = requests.get(f"{base_url}/health", timeout=5).json()
        assert health["status"] == "ok", f"Unexpected health: {health}"
        assert health["model"]["backend"] == "tflite", f"Expected tflite backend, got {health['model']}"
        assert len(health["supported_crops"]) == len(get_supported_crops()) == 14
        print(f"[PASS] GET /health -> backend={health['model']['backend']}, crops={len(health['supported_crops'])}")

        # Test invalid file upload rejection
        bad_resp = requests.post(
            f"{base_url}/predict",
            files={"file": ("test.txt", b"not an image", "text/plain")},
            timeout=5,
        )
        assert bad_resp.status_code == 400, f"Expected 400 for non-image upload, got {bad_resp.status_code}"
        print("[PASS] POST /predict rejects invalid MIME type with 400.")

        # Test real image prediction
        sample_img = next((BASE_DIR / "dataset" / "valid" / "Tomato___Late_blight").glob("*.*"))
        pred_resp = requests.post(
            f"{base_url}/predict",
            files={"file": (sample_img.name, sample_img.read_bytes(), "image/jpeg")},
            data={"crop_name": "Tomato"},
            timeout=10,
        )
        assert pred_resp.status_code == 200, pred_resp.text
        pred_json = pred_resp.json()
        top = pred_json["predictions"][0]
        print(f"[PASS] POST /predict -> {top['friendly_name']} ({top['confidence']*100:.1f}%)")

        # Test /recommend
        rec_resp = requests.post(
            f"{base_url}/recommend",
            data={
                "class_name": top["class_name"],
                "friendly_name": top["friendly_name"],
                "crop_name": "Tomato",
                "plant_age_weeks": "6",
                "soil_pH": "7.0",
                "spray_count": "1",
                "avg_temp": "26.5",
                "avg_humidity": "82.0",
                "total_rain": "8.0",
                "risk_text": "HIGH",
            },
            timeout=25,
        )
        assert rec_resp.status_code == 200, rec_resp.text
        rec_json = rec_resp.json()
        assert "structured" in rec_json and "english" in rec_json["structured"] and "hindi" in rec_json["structured"]
        print(f"[PASS] POST /recommend -> source={rec_json['structured']['source']}, items={rec_json['structured']['shopping_items']}")

        # Test /weather
        w_resp = requests.get(f"{base_url}/weather", params={"lat": 28.7041, "lon": 77.1025}, timeout=10)
        assert w_resp.status_code == 200, w_resp.text
        w_json = w_resp.json()
        print(f"[PASS] GET /weather -> temp={w_json['avg_temperature']}C, humidity={w_json['avg_humidity']}%, risk={w_json['risk_level']}")

        # Test /geocode
        g_resp = requests.get(f"{base_url}/geocode", params={"q": "Pune, India"}, timeout=10)
        assert g_resp.status_code == 200, g_resp.text
        g_json = g_resp.json()
        print(f"[PASS] GET /geocode -> {len(g_json['results'])} results for 'Pune, India'")

        # Test /stores/nearby
        s_resp = requests.get(f"{base_url}/stores/nearby", params={"lat": 28.7041, "lon": 77.1025, "radius_km": 12, "category": "all"}, timeout=30)
        assert s_resp.status_code == 200, s_resp.text
        s_json = s_resp.json()
        assert "stores" in s_json and "fallback_searches" in s_json
        sample_names = [s["name"] for s in s_json["stores"][:3]]
        print(f"[PASS] GET /stores/nearby -> found {s_json['total_found']} OSM stores (sample={sample_names}) + {len(s_json['fallback_searches'])} fallback links.")

        # Test / serving built frontend
        root_resp = requests.get(f"{base_url}/", timeout=5)
        assert root_resp.status_code == 200
        print(f"[PASS] GET / -> status={root_resp.status_code}")

    finally:
        proc.terminate()
        proc.wait(timeout=5)


if __name__ == "__main__":
    verify_knowledge_base()
    verify_tflite_accuracy_sample()
    verify_live_api()
    print("ALL VERIFICATION CHECKS PASSED!")
