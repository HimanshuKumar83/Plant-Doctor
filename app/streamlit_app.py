import os
import uuid
import requests
import streamlit as st

from predict import predict_leaf_image
from knowledge_base.gemini_recommend import generate_treatment_with_gemini

# ---------- SETUP ----------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(page_title="AI Plant Doctor", page_icon="🌿")
st.title("🌿 AI-Powered Plant Disease Diagnosis & Smart Treatment Advisor")
st.markdown("""
This system will:
- 📷 Detect plant disease using CNN  
- 🌦 Analyze real-time weather impact  
- 💊 Recommend Organic + Chemical group treatment  
- 🌍 Auto-detect user location  
- 🔄 Works offline if Gemini API fails  
""")


# ---------- CITY LIST (for manual option) ----------
cities = {
    "Delhi": (28.7041, 77.1025), "Lucknow": (26.8467, 80.9462),
    "Chandigarh": (30.7333, 76.7794), "Jaipur": (26.9124, 75.7873),
    "Bengaluru": (12.9716, 77.5946), "Hyderabad": (17.3850, 78.4867),
    "Chennai": (13.0827, 80.2707), "Trivandrum": (8.5241, 76.9366),
    "Mumbai": (19.0760, 72.8777), "Ahmedabad": (23.0225, 72.5714),
    "Surat": (21.1702, 72.8311), "Pune": (18.5204, 73.8567),
    "Kolkata": (22.5726, 88.3639), "Patna": (25.5941, 85.1376),
    "Ranchi": (23.3441, 85.3096), "Guwahati": (26.1445, 91.7362),
    "Bhopal": (23.2599, 77.4126), "Jabalpur": (23.1815, 79.9864),
    "Raipur": (21.2514, 81.6296), "Nagpur": (21.1458, 79.0882),
    "Indore": (22.7196, 75.8577)
}


# ---------- AUTO-LOCATION USING IPINFO ----------
def auto_detect_location():
    """Auto-detect user location using IPInfo API."""
    IPINFO_TOKEN = "56828b4b718949"  # <--- REPLACE THIS

    try:
        res = requests.get(
            f"https://ipinfo.io/json?token={IPINFO_TOKEN}",
            timeout=5
        ).json()

        if "loc" in res:
            lat, lon = res["loc"].split(",")
            return float(lat), float(lon)
    except Exception as e:
        print("Location error:", e)

    return None, None


lat, lon = auto_detect_location()

if lat and lon:
    st.success(f"📍 Auto-location detected: Lat {lat:.2f}, Lon {lon:.2f}")
    st.session_state["latitude"] = lat
    st.session_state["longitude"] = lon
else:
    st.warning("⚠ Auto-location failed! Select city manually.")
    city = st.selectbox("🌍 Select Nearest City", list(cities.keys()))
    st.session_state["latitude"], st.session_state["longitude"] = cities[city]

latitude = st.session_state["latitude"]
longitude = st.session_state["longitude"]


# ---------- CROP + FARM DETAILS ----------
crop_options = [
    "Tomato", "Potato", "Apple", "Corn", "Grape",
    "Strawberry", "Peach", "Orange", "Bell Pepper"
]

col1, col2, col3 = st.columns(3)

crop_name = col1.selectbox("Select Crop", crop_options)
plant_age_weeks = col2.number_input("Plant Age (weeks)", 0, 30, 6)
soil_pH = col3.number_input("Soil pH (0 = unknown)", 0.0, 14.0, 7.0)

spray_count = st.slider("Previous Chemical Sprays This Season", 0, 10, 0)
use_soil_pH = soil_pH if soil_pH > 0 else None


# ---------- WEATHER FETCH + RISK LOGIC ----------
def get_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relativehumidity_2m,rain",
        "forecast_days": 3,
        "timezone": "auto"
    }

    try:
        res = requests.get(url, params=params, timeout=5).json()

        temps = res["hourly"]["temperature_2m"]
        hums = res["hourly"]["relativehumidity_2m"]
        rain = res["hourly"]["rain"]

        avg_temp = sum(temps) / len(temps)
        avg_humidity = sum(hums) / len(hums)
        total_rain = sum(rain)

        # ----- Disease Risk Rules -----
        if avg_humidity > 80 and total_rain > 5:
            risk = "HIGH 🔴 — Very favorable for fungal spread."
        elif avg_humidity > 60 or total_rain > 2:
            risk = "MODERATE 🟡 — Increased risk. Monitor closely."
        else:
            risk = "LOW 🟢 — Normal preventive care."

        return {
            "avg_temperature": avg_temp,
            "avg_humidity": avg_humidity,
            "total_rain_mm": total_rain,
            "risk_level": risk
        }

    except Exception as e:
        print("Weather error:", e)
        return {"error": "Weather fetch failed!"}


# ---------- FILE UPLOAD ----------
uploaded_file = st.file_uploader("📤 Upload Leaf Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    ext = uploaded_file.name.split(".")[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    img_path = os.path.join(UPLOAD_DIR, filename)

    with open(img_path, "wb") as f:
        f.write(uploaded_file.read())

    st.image(img_path, width=300, caption="Uploaded Leaf")

    # ----- CNN PREDICTION -----
    with st.spinner("🔍 Detecting disease..."):
        preds = predict_leaf_image(img_path)
    best = preds[0]

    st.subheader("🧬 Disease Prediction")
    st.write(f"**Detected Disease:** {best['friendly_name']} ({best['confidence']*100:.2f}%)")

    # ----- WEATHER -----
    weather = get_weather(latitude, longitude)

    st.subheader("🌦 Weather Impact Analysis")
    if "error" in weather:
        st.error(weather["error"])
    else:
        st.write(f"- Avg Temp (3 days): {weather['avg_temperature']:.1f}°C")
        st.write(f"- Avg Humidity: {weather['avg_humidity']:.1f}%")
        st.write(f"- Total Rainfall: {weather['total_rain_mm']:.1f} mm")
        st.markdown(f"**Disease Spread Risk:** {weather['risk_level']}")

    # ----- TREATMENT (Gemini + Offline fallback) -----
    with st.spinner("💊 Generating Smart Treatment Plan..."):
        advice = generate_treatment_with_gemini(
            class_name=best["class_name"],
            friendly_name=best["friendly_name"],
            crop_name=crop_name,
            plant_age_weeks=plant_age_weeks,
            soil_pH=use_soil_pH,
            spray_count=spray_count,
            weather_summary=weather
        )

    st.subheader("💡 Treatment Recommendations (EN + HI)")
    st.write(advice)

else:
    st.info("📌 Upload a clear leaf image to begin diagnosis.")
