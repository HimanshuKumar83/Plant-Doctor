"""Gemini treatment recommendation service with structured JSON output and offline fallback."""

import json
import os
import re
from typing import Any, Dict, Optional

import google.generativeai as genai
from dotenv import load_dotenv

from backend.services.knowledge_base import (
    format_advice_text,
    get_local_recommendation,
)

load_dotenv()


def _get_gemini_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured")
    genai.configure(api_key=api_key)
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    return genai.GenerativeModel(model_name)


def _extract_json(raw_text: str) -> Dict[str, Any]:
    cleaned = raw_text.strip()
    fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, flags=re.DOTALL)
    if fence_match:
        cleaned = fence_match.group(1)
    return json.loads(cleaned)


def _validate_lang_block(block: Any, fallback_block: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(block, dict):
        return fallback_block
    return {
        "summary": str(block.get("summary") or fallback_block["summary"]),
        "chemical": [str(x) for x in block.get("chemical", fallback_block["chemical"]) if x] or fallback_block["chemical"],
        "organic": [str(x) for x in block.get("organic", fallback_block["organic"]) if x] or fallback_block["organic"],
        "prevention": [str(x) for x in block.get("prevention", fallback_block["prevention"]) if x] or fallback_block["prevention"],
        "safety": [str(x) for x in block.get("safety", fallback_block["safety"]) if x] or fallback_block["safety"],
    }


def generate_smart_treatment(
    class_name: str,
    friendly_name: str,
    crop_name: str,
    plant_age_weeks: int,
    soil_pH: Optional[float],
    spray_count: int,
    weather_summary: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Generate structured bilingual advice via Gemini, falling back seamlessly to offline KB."""
    weather_summary = weather_summary or {}
    offline = get_local_recommendation(
        class_name=class_name,
        soil_pH=soil_pH,
        spray_count=spray_count,
        weather_summary=weather_summary,
    )

    try:
        model = _get_gemini_model()
        prompt = f"""
You are an expert Agricultural Plant Pathologist advising a farmer.
Return ONLY valid JSON matching the exact schema below (no markdown outside JSON).

DIAGNOSIS INPUT:
- Disease Detected: {friendly_name} ({class_name})
- Crop Name: {crop_name}
- Plant Age: {plant_age_weeks} weeks
- Soil pH: {"Unknown" if soil_pH is None or soil_pH <= 0 else soil_pH}
- Chemical Sprays Used This Season: {spray_count}
- 3-Day Avg Temp: {weather_summary.get("avg_temperature", "NA")} °C
- 3-Day Avg Humidity: {weather_summary.get("avg_humidity", "NA")} %
- 3-Day Total Rain: {weather_summary.get("total_rain_mm", "NA")} mm
- Spread Risk: {weather_summary.get("risk_text", "NA")}

STRICT AGRONOMY RULES:
1. If humidity > 80% OR rainfall > 5mm, advise waiting for a dry 6+ hour window before chemical spraying.
2. If soil pH < 5.5, include agricultural lime correction; if soil pH > 7.5, include sulfur/gypsum/organic compost correction.
3. If sprays >= 3, warn about resistance and recommend rotating chemical mode-of-action groups.
4. Mention active ingredient / fungicide / pesticide GROUP names ONLY — NO commercial brand names.
5. Include practical organic, manure/compost, or fertilizer options available at local Indian agri-stores (Krishi Kendra).
6. Keep bullet items short, clear, and farmer-friendly in both English and simple Hindi.
7. "store_categories" must be a subset of ["pesticides", "fertilizers", "manure", "seeds"].
8. "shopping_items" must list 2–4 concise item names the farmer should ask for at a nearby agri-medicine / fertilizer store.

JSON SCHEMA:
{{
  "store_categories": ["pesticides", "manure"],
  "shopping_items": ["Mancozeb group fungicide", "Neem oil 2%", "Vermicompost"],
  "english": {{
    "summary": "1-2 sentence explanation tied to current weather.",
    "chemical": ["bullet 1", "bullet 2"],
    "organic": ["bullet 1", "bullet 2"],
    "prevention": ["bullet 1", "bullet 2"],
    "safety": ["bullet 1", "bullet 2"]
  }},
  "hindi": {{
    "summary": "मौसम के अनुसार 1-2 वाक्य में रोग सारांश।",
    "chemical": ["बिंदु 1", "बिंदु 2"],
    "organic": ["बिंदु 1", "बिंदु 2"],
    "prevention": ["बिंदु 1", "बिंदु 2"],
    "safety": ["बिंदु 1", "बिंदु 2"]
  }}
}}
"""
        response = model.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.3,
            },
            request_options={"timeout": 15},
        )
        parsed = _extract_json(response.text)

        valid_cats = {"pesticides", "fertilizers", "manure", "seeds"}
        cats = [c for c in parsed.get("store_categories", []) if c in valid_cats] or offline["store_categories"]
        shopping = [str(x) for x in parsed.get("shopping_items", []) if x][:5] or offline["shopping_items"]

        structured = {
            "friendly_name": friendly_name,
            "source": "gemini",
            "store_categories": cats,
            "shopping_items": shopping,
            "english": _validate_lang_block(parsed.get("english"), offline["english"]),
            "hindi": _validate_lang_block(parsed.get("hindi"), offline["hindi"]),
        }
        structured["advice_text"] = format_advice_text(structured)
        return structured

    except Exception:
        offline["source"] = "offline_fallback"
        offline["advice_text"] = format_advice_text(offline)
        return offline
