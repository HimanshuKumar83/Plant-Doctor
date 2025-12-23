from api_keys.gemini_key import get_gemini_model
from knowledge_base.local_fallback import get_local_recommendation

def generate_treatment_with_gemini(
    class_name,
    friendly_name,
    crop_name,
    plant_age_weeks,
    soil_pH,
    spray_count,
    weather_summary=None,
):
    """
    First tries to get bilingual recommendation using Gemini API.
    If Gemini fails / no internet → Falls back to offline recommendations.
    """

    try:
        model = get_gemini_model()

        # ------------ STRONG, WEATHER-AWARE PROMPT --------------
        prompt = f"""
You are an award-winning Agricultural Plant Pathologist and Crop Disease Advisor.

🧪 Your job:
Generate a weather-aware, crop-specific, practical treatment plan.
It must change based on:
- Humidity
- Temperature
- Rainfall
- Soil pH
- Previous chemical spray count

==================== INPUT DIAGNOSIS DATA =====================
Disease Detected: {friendly_name}
Disease Class ID: {class_name}
Crop Name: {crop_name}
Plant Age: {plant_age_weeks} weeks
Soil pH Provided: {"Unknown" if soil_pH is None else soil_pH}
Sprays used this season: {spray_count}

Weather Forecast — Next 3 Days:
Temperature: {weather_summary.get('avg_temperature', 'NA')} °C
Humidity: {weather_summary.get('avg_humidity', 'NA')} %
Rainfall total: {weather_summary.get('total_rain_mm', 'NA')} mm
Disease Risk Level: {weather_summary.get('risk_level', 'NA')}
===============================================================

⚠ RULES for generating recommendations:
- If humidity > 80% OR rainfall > 5mm → DO NOT advise immediate chemical spray.
- If rainfall predicted → Tell farmer WHEN to spray (gap before/after rain).
- If soil pH < 5.5 → recommend lime / pH correction methods.
- If soil pH > 7.5 → advise sulfur / organic acid application.
- If chemical sprays ≥ 3 → warn about resistance & switch pesticide group.
- Mention mode of action / pesticide GROUP only — NO BRAND NAMES.
- Include farmer-friendly organic options using local Indian resources.
- Make content unique & not repetitive.
- Use simple, village-level language.

================== OUTPUT MUST BE IN TWO LANGUAGES ================

[ENGLISH]
1️⃣ Short reason why this disease spreads (based on weather)
2️⃣ Chemical Control – Group name, mode of action, & correct timing
3️⃣ Organic / Natural treatment suggestions
4️⃣ Soil correction (if pH abnormal) AND preventive care for 2 weeks
5️⃣ Safety + PPE + Environmental precautions

[HINDI]
1️⃣ मौसम के अनुसार रोग क्यों फैलता है (संक्षेप में)
2️⃣ रासायनिक उपचार – केवल समूह का नाम, समय और सावधानी
3️⃣ प्राकृतिक / घरेलू / आसानी से उपलब्ध उपचार
4️⃣ मिट्टी सुधार और अगले 2 सप्ताह के लिए रोकथाम
5️⃣ किसान सुरक्षा और पर्यावरण सावधानियाँ

Keep output SHORT, CLEAR, and ACTIONABLE for farmers.
"""

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception:
        # Offline fallback if Gemini fails
        fallback = get_local_recommendation(class_name)
        en = fallback["english"]
        hi = fallback["hindi"]

        english_text = (
            f"[ENGLISH]\n"
            f"1. Disease Summary: {en['summary']}\n"
            f"2. Chemical Treatment: {'; '.join(en['chemical'])}\n"
            f"3. Organic Treatment: {'; '.join(en['organic'])}\n"
            f"4. Preventive Measures: {'; '.join(en['prevention'])}\n"
            f"5. Safety Precautions: {'; '.join(en['safety'])}\n"
        )

        hindi_text = (
            f"\n[HINDI]\n"
            f"1. रोग सारांश: {hi['summary']}\n"
            f"2. रासायनिक उपचार: {'; '.join(hi['chemical'])}\n"
            f"3. ऑर्गेनिक उपचार: {'; '.join(hi['organic'])}\n"
            f"4. रोकथाम उपाय: {'; '.join(hi['prevention'])}\n"
            f"5. सुरक्षा उपाय: {'; '.join(hi['safety'])}\n"
        )

        return english_text + hindi_text
