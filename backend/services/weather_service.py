"""Open-Meteo weather fetching with in-memory TTL caching and disease risk assessment."""

import time
from typing import Any, Dict, Tuple
import requests

_WEATHER_CACHE: Dict[Tuple[float, float], Tuple[float, Dict[str, Any]]] = {}
_CACHE_TTL_SECONDS = 900  # 15 minutes


def fetch_weather_summary(lat: float, lon: float) -> Dict[str, Any]:
    """Fetch 3-day hourly forecast from Open-Meteo and compute agricultural spread risk."""
    cache_key = (round(lat, 2), round(lon, 2))
    now = time.time()
    cached = _WEATHER_CACHE.get(cache_key)
    if cached and (now - cached[0]) < _CACHE_TTL_SECONDS:
        return cached[1]

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relativehumidity_2m,rain",
        "forecast_days": 3,
        "timezone": "auto",
    }

    payload = None
    last_exc = None
    for attempt_timeout in (8, 12):
        try:
            res = requests.get(url, params=params, timeout=attempt_timeout)
            res.raise_for_status()
            payload = res.json()
            break
        except Exception as exc:
            last_exc = exc
            time.sleep(0.5)
    if payload is None:
        raise last_exc or RuntimeError("Weather request failed")

    hourly = payload.get("hourly") or {}
    temps = [x for x in hourly.get("temperature_2m", []) if x is not None]
    hums = [x for x in hourly.get("relativehumidity_2m", []) if x is not None]
    rain = [x for x in hourly.get("rain", []) if x is not None]

    if not temps or not hums:
        raise ValueError("Incomplete weather data returned by Open-Meteo")

    avg_temp = sum(temps) / len(temps)
    avg_humidity = sum(hums) / len(hums)
    total_rain = sum(rain) if rain else 0.0

    if avg_humidity > 80 and total_rain > 5:
        risk_text = "HIGH — Very favorable for fungal and bacterial spread. Delay spraying until dry window."
        risk_level = "high"
    elif avg_humidity > 60 or total_rain > 2:
        risk_text = "MODERATE — Elevated moisture risk. Monitor leaf undersides closely."
        risk_level = "moderate"
    else:
        risk_text = "LOW — Dry conditions. Good window for preventive care or targeted spraying."
        risk_level = "low"

    result = {
        "avg_temperature": round(avg_temp, 1),
        "avg_humidity": round(avg_humidity, 1),
        "total_rain_mm": round(total_rain, 1),
        "risk_text": risk_text,
        "risk_level": risk_level,
        "timezone": payload.get("timezone", "auto"),
    }

    _WEATHER_CACHE[cache_key] = (now, result)
    return result
