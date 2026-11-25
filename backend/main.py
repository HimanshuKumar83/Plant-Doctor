"""FastAPI backend for Plant Doctor: disease detection, weather risk, smart treatment, and store locator."""

import asyncio
import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.services.gemini_service import generate_smart_treatment
from backend.services.predictor import (
    get_model_status,
    get_supported_crops,
    predict_from_bytes,
)
from backend.services.store_locator import find_nearby_stores, geocode_location
from backend.services.weather_service import fetch_weather_summary

MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}

app = FastAPI(title="Plant Doctor - Plant Disease & Agro Store API", version="2.0.0")

allowed_origins_env = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://localhost:8000",
)
allowed_origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    model_status = await asyncio.to_thread(get_model_status)
    return {
        "status": "ok" if model_status.get("loaded") else "degraded",
        "model": model_status,
        "supported_crops": get_supported_crops(),
    }


@app.get("/crops")
async def list_crops():
    return {"crops": get_supported_crops()}


@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    crop_name: Optional[str] = Form(None),
):
    if file.content_type and file.content_type.lower() not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a JPG, PNG, or WebP leaf image.",
        )

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(image_bytes) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Image exceeds 10 MB size limit.")

    try:
        result = await asyncio.to_thread(
            predict_from_bytes, image_bytes, 3, crop_name
        )
        return {"success": True, **result}
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not process this image. Please upload a clear photo of a plant leaf.",
        )


@app.get("/weather")
async def get_weather_data(
    lat: float = Query(..., ge=-90.0, le=90.0),
    lon: float = Query(..., ge=-180.0, le=180.0),
):
    try:
        return await asyncio.to_thread(fetch_weather_summary, lat, lon)
    except Exception:
        raise HTTPException(status_code=502, detail="Weather service temporarily unavailable.")


@app.get("/geocode")
async def geocode(q: str = Query(..., min_length=2, max_length=120)):
    try:
        results = await asyncio.to_thread(geocode_location, q)
        return {"results": results}
    except Exception:
        raise HTTPException(status_code=502, detail="Location lookup service temporarily unavailable.")


@app.get("/stores/nearby")
async def nearby_stores(
    lat: float = Query(..., ge=-90.0, le=90.0),
    lon: float = Query(..., ge=-180.0, le=180.0),
    radius_km: int = Query(12, ge=2, le=30),
    category: str = Query("all"),
):
    valid_categories = {"all", "pesticides", "fertilizers", "manure", "seeds"}
    cat = category.lower().strip()
    if cat not in valid_categories:
        cat = "all"
    return await asyncio.to_thread(find_nearby_stores, lat, lon, radius_km, cat)


@app.post("/recommend")
async def get_recommendation(
    class_name: str = Form(...),
    friendly_name: str = Form(...),
    crop_name: str = Form(...),
    plant_age_weeks: int = Form(6),
    soil_pH: Optional[float] = Form(None),
    spray_count: int = Form(0),
    avg_temp: Optional[float] = Form(None),
    avg_humidity: Optional[float] = Form(None),
    total_rain: Optional[float] = Form(None),
    risk_text: Optional[str] = Form(None),
):
    weather_summary = {
        "avg_temperature": avg_temp,
        "avg_humidity": avg_humidity,
        "total_rain_mm": total_rain,
        "risk_text": risk_text,
    }
    advice = await asyncio.to_thread(
        generate_smart_treatment,
        class_name=class_name,
        friendly_name=friendly_name,
        crop_name=crop_name,
        plant_age_weeks=plant_age_weeks,
        soil_pH=soil_pH,
        spray_count=spray_count,
        weather_summary=weather_summary,
    )
    return {"advice": advice["advice_text"], "structured": advice}


# Serve built React frontend in single-container deployments (Docker / Hugging Face / Render)
FRONTEND_DIST = Path(__file__).resolve().parents[1] / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="frontend")
else:
    @app.get("/")
    async def root():
        return {"message": "Plant Doctor API is running", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=False)
