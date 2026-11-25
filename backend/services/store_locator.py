"""Free nearby agricultural, pesticide, manure, and fertilizer store locator via OpenStreetMap & Open-Meteo."""

import concurrent.futures
import math
import time
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import quote_plus

import requests

OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

OPEN_METEO_GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
PHOTON_URL = "https://photon.komoot.io/api/"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "PlantDoctor/2.0 (plant-disease-advisor)"

_STORE_CACHE: Dict[Tuple[float, float, int], Tuple[float, List[Dict[str, Any]]]] = {}
_GEOCODE_CACHE: Dict[str, Tuple[float, List[Dict[str, Any]]]] = {}
_STORE_TTL_SECONDS = 1800  # 30 minutes
_GEOCODE_TTL_SECONDS = 3600  # 1 hour


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return round(2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 2)


def _infer_categories(name: str, tags: Dict[str, str]) -> List[str]:
    text = f"{name} {tags.get('shop', '')} {tags.get('description', '')} {tags.get('product', '')}".lower()
    cats: List[str] = []

    if any(k in text for k in ["pesticid", "chemical", "plant protection", "krishi", "agro", "kisan", "agrarian"]):
        cats.append("pesticides")
    if any(k in text for k in ["fertiliz", "khad", "urea", "npk", "krishi", "agro", "kisan", "agrarian", "farm"]):
        cats.append("fertilizers")
    if any(k in text for k in ["manure", "compost", "vermi", "organic", "nursery", "garden_centre", "garden"]):
        cats.append("manure")
    if any(k in text for k in ["seed", "beej", "nursery", "krishi", "agrarian"]):
        cats.append("seeds")

    if not cats:
        cats = ["pesticides", "fertilizers", "manure"]
    return sorted(set(cats))


def _format_address(tags: Dict[str, str]) -> str:
    parts = [
        tags.get("addr:housenumber"),
        tags.get("addr:street"),
        tags.get("addr:suburb") or tags.get("addr:neighbourhood"),
        tags.get("addr:city") or tags.get("addr:town") or tags.get("addr:village"),
        tags.get("addr:state"),
        tags.get("addr:postcode"),
    ]
    cleaned = [p.strip() for p in parts if p and p.strip()]
    return ", ".join(cleaned) if cleaned else (tags.get("addr:full") or "Address details on map")


def _query_overpass(lat: float, lon: float, radius_m: int) -> List[Dict[str, Any]]:
    # Exact tag equality uses Overpass's tag index for fast responses
    query = f"""
[out:json][timeout:6];
(
  node["shop"="agrarian"](around:{radius_m},{lat},{lon});
  way["shop"="agrarian"](around:{radius_m},{lat},{lon});
  node["shop"="garden_centre"](around:{radius_m},{lat},{lon});
  way["shop"="garden_centre"](around:{radius_m},{lat},{lon});
  node["shop"="farm"](around:{radius_m},{lat},{lon});
  way["shop"="farm"](around:{radius_m},{lat},{lon});
  node["shop"="agro"](around:{radius_m},{lat},{lon});
  node["shop"="seed"](around:{radius_m},{lat},{lon});
);
out center tags 50;
"""
    for endpoint in OVERPASS_ENDPOINTS:
        try:
            resp = requests.post(
                endpoint,
                data={"data": query},
                headers={"User-Agent": USER_AGENT},
                timeout=6,
            )
            if resp.ok:
                return resp.json().get("elements", [])
        except Exception:
            continue
    return []


def _query_photon_stores(lat: float, lon: float, radius_km: int) -> List[Dict[str, Any]]:
    """Lightweight OpenStreetMap Photon POI search bounded around user coordinates."""
    deg_lat = radius_km / 111.0
    deg_lon = radius_km / max(111.0 * math.cos(math.radians(lat)), 20.0)
    bbox = f"{lon - deg_lon:.5f},{lat - deg_lat:.5f},{lon + deg_lon:.5f},{lat + deg_lat:.5f}"

    allowed_osm_values = {
        "agrarian",
        "farm",
        "garden_centre",
        "agro",
        "seed",
        "nursery",
        "marketplace",
        "florist",
    }
    excluded_osm_values = {
        "apartments",
        "residential",
        "house",
        "bus_stop",
        "station",
        "school",
        "college",
        "hospital",
        "hotel",
        "restaurant",
        "park",
        "landfill",
    }

    def fetch_kw(kw: str) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        try:
            resp = requests.get(
                PHOTON_URL,
                params={"q": kw, "bbox": bbox, "limit": 10},
                headers={"User-Agent": USER_AGENT},
                timeout=5,
            )
            if not resp.ok:
                return out
            for feat in resp.json().get("features", []):
                props = feat.get("properties") or {}
                osm_key = (props.get("osm_key") or "").lower()
                osm_value = (props.get("osm_value") or "").lower()
                name = (props.get("name") or "").strip()
                if not name:
                    continue
                if osm_value in excluded_osm_values:
                    continue
                if osm_key != "shop" and osm_value not in allowed_osm_values:
                    # Keep non-shop POIs only when their name explicitly indicates an agro store/nursery
                    lower_name = name.lower()
                    if not any(t in lower_name for t in ("krishi", "khad", "beej", "fertiliz", "pesticid", "manure", "vermi", "nursery", "kisan", "agro")):
                        continue
                    if any(b in lower_name for b in ("apartment", "residency", "enclave", "tower", "school", "public park", "metro")):
                        continue

                coords = (feat.get("geometry") or {}).get("coordinates") or []
                if len(coords) < 2:
                    continue
                out.append(
                    {
                        "type": props.get("osm_type", "node"),
                        "id": props.get("osm_id") or f"{kw}_{coords[0]}_{coords[1]}",
                        "lat": coords[1],
                        "lon": coords[0],
                        "tags": {
                            "name": name,
                            "shop": osm_value or "agrarian",
                            "addr:street": props.get("street"),
                            "addr:city": props.get("city") or props.get("county"),
                            "addr:state": props.get("state"),
                            "addr:postcode": props.get("postcode"),
                        },
                    }
                )
        except Exception:
            pass
        return out

    elements: List[Dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for res in pool.map(fetch_kw, ("krishi", "fertilizer", "agro", "nursery")):
            elements.extend(res)
    return elements


def find_nearby_stores(
    lat: float,
    lon: float,
    radius_km: int = 12,
    category: str = "all",
) -> Dict[str, Any]:
    """Find nearby agro/pesticide/fertilizer/manure stores using free OpenStreetMap data."""
    radius_km = max(2, min(radius_km, 30))
    cache_key = (round(lat, 2), round(lon, 2), radius_km)
    now = time.time()

    raw_stores: Optional[List[Dict[str, Any]]] = None
    osm_warning: Optional[str] = None
    cached = _STORE_CACHE.get(cache_key)
    if cached and (now - cached[0]) < _STORE_TTL_SECONDS:
        raw_stores = cached[1]
    else:
        elements: List[Dict[str, Any]] = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            overpass_future = pool.submit(_query_overpass, lat, lon, radius_km * 1000)
            photon_future = pool.submit(_query_photon_stores, lat, lon, radius_km)
            elements.extend(overpass_future.result())
            elements.extend(photon_future.result())

        if not elements:
            osm_warning = (
                "No live OpenStreetMap entries returned within timeout; "
                "use the direct Google Maps buttons below to view all nearby stores."
            )

        seen = set()
        parsed: List[Dict[str, Any]] = []
        for el in elements:
            tags = el.get("tags") or {}
            el_lat = el.get("lat") or (el.get("center") or {}).get("lat")
            el_lon = el.get("lon") or (el.get("center") or {}).get("lon")
            if el_lat is None or el_lon is None:
                continue

            name = tags.get("name") or tags.get("brand") or tags.get("operator") or "Agricultural Supply Store"
            dedupe_key = (name.lower().strip(), round(float(el_lat), 4), round(float(el_lon), 4))
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)

            dist_km = _haversine_km(lat, lon, float(el_lat), float(el_lon))
            if dist_km > radius_km * 1.25:
                continue
            cats = _infer_categories(name, tags)

            parsed.append(
                {
                    "id": f"{el.get('type', 'node')}_{el.get('id')}",
                    "name": name,
                    "shop_type": tags.get("shop") or tags.get("amenity") or "agro_store",
                    "categories": cats,
                    "lat": float(el_lat),
                    "lon": float(el_lon),
                    "distance_km": dist_km,
                    "address": _format_address(tags),
                    "phone": tags.get("phone") or tags.get("contact:phone") or tags.get("mobile"),
                    "opening_hours": tags.get("opening_hours"),
                    "directions_url": f"https://www.google.com/maps/dir/?api=1&destination={el_lat},{el_lon}",
                    "osm_url": f"https://www.openstreetmap.org/?mlat={el_lat}&mlon={el_lon}#map=17/{el_lat}/{el_lon}",
                }
            )

        parsed.sort(key=lambda s: s["distance_km"])
        raw_stores = parsed
        if raw_stores:
            _STORE_CACHE[cache_key] = (now, parsed)

    filtered = raw_stores
    if category and category != "all":
        filtered = [s for s in raw_stores if category in s["categories"]]

    fallback_searches = [
        {
            "label": "Pesticide & Fertilizer Shops (Google Maps)",
            "category": "pesticides",
            "url": f"https://www.google.com/maps/search/{quote_plus('pesticide fertilizer krishi kendra')}/@{lat},{lon},13z",
        },
        {
            "label": "Organic Manure & Nurseries (Google Maps)",
            "category": "manure",
            "url": f"https://www.google.com/maps/search/{quote_plus('organic manure vermicompost nursery')}/@{lat},{lon},13z",
        },
        {
            "label": "Krishi Seva Kendra / Agro Center (Google Maps)",
            "category": "fertilizers",
            "url": f"https://www.google.com/maps/search/{quote_plus('krishi seva kendra agro store')}/@{lat},{lon},13z",
        },
    ]

    return {
        "stores": filtered[:25],
        "total_found": len(filtered),
        "radius_km": radius_km,
        "category": category,
        "source": "openstreetmap",
        "warning": osm_warning,
        "fallback_searches": fallback_searches,
    }


def geocode_location(query: str) -> List[Dict[str, Any]]:
    """Convert a village, city, or PIN code query into coordinates (Open-Meteo + Photon/Nominatim fallback)."""
    cleaned = query.strip()
    if len(cleaned) < 2:
        return []

    cache_key = cleaned.lower()
    now = time.time()
    cached = _GEOCODE_CACHE.get(cache_key)
    if cached and (now - cached[0]) < _GEOCODE_TTL_SECONDS:
        return cached[1]

    results: List[Dict[str, Any]] = []

    # 1. Open-Meteo Geocoding API (fast, free, cloud-friendly)
    primary_term = cleaned.split(",")[0].strip()
    try:
        resp = requests.get(
            OPEN_METEO_GEOCODE_URL,
            params={"name": primary_term, "count": 6, "language": "en", "format": "json"},
            timeout=6,
        )
        if resp.ok:
            for item in resp.json().get("results", []):
                parts = [item.get("name"), item.get("admin1"), item.get("country")]
                display = ", ".join(p for p in parts if p)
                results.append(
                    {
                        "display_name": display,
                        "lat": float(item["latitude"]),
                        "lon": float(item["longitude"]),
                    }
                )
    except Exception:
        pass

    # 2. Photon fallback (handles PIN codes and street/village queries)
    if not results:
        try:
            resp = requests.get(
                PHOTON_URL,
                params={"q": cleaned, "limit": 5},
                headers={"User-Agent": USER_AGENT},
                timeout=6,
            )
            if resp.ok:
                for feat in resp.json().get("features", []):
                    props = feat.get("properties") or {}
                    coords = (feat.get("geometry") or {}).get("coordinates") or []
                    if len(coords) < 2:
                        continue
                    parts = [props.get("name"), props.get("city"), props.get("state"), props.get("country")]
                    display = ", ".join(dict.fromkeys(p for p in parts if p))
                    if display:
                        results.append({"display_name": display, "lat": float(coords[1]), "lon": float(coords[0])})
        except Exception:
            pass

    # 3. Nominatim fallback
    if not results:
        resp = requests.get(
            NOMINATIM_URL,
            params={"q": cleaned, "format": "json", "limit": 5},
            headers={"User-Agent": USER_AGENT},
            timeout=8,
        )
        resp.raise_for_status()
        for item in resp.json():
            if "lat" in item and "lon" in item:
                results.append(
                    {
                        "display_name": item.get("display_name"),
                        "lat": float(item["lat"]),
                        "lon": float(item["lon"]),
                    }
                )

    _GEOCODE_CACHE[cache_key] = (now, results)
    return results
