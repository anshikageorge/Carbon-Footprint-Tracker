import google.generativeai as genai
import os
import re

# ---------------- CONFIG ---------------- #
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None

# ---------------- CARBON FACTORS ---------------- #
EMISSION_FACTORS = {
    "car_km": 0.21,        # kg CO2 per km
    "bike_km": 0.05,
    "flight_km": 0.15,
    "beef_meal": 27.0,
    "veg_meal": 2.0
}

# ---------------- PARSER ---------------- #
def parse_user_input(text):
    text = text.lower()

    km = re.search(r"(\d+)\s?km", text)
    km = int(km.group(1)) if km else 0

    transport = "car"
    if "bike" in text or "cycle" in text:
        transport = "bike"
    if "flight" in text or "flew" in text:
        transport = "flight"

    meal = None
    if "beef" in text:
        meal = "beef"
    elif "veg" in text or "vegetable" in text:
        meal = "veg"

    return km, transport, meal

# ---------------- CALCULATOR ---------------- #
def calculate_emissions(km, transport, meal):
    total = 0

    if km > 0:
        if transport == "car":
            total += km * EMISSION_FACTORS["car_km"]
        elif transport == "bike":
            total += km * EMISSION_FACTORS["bike_km"]
        elif transport == "flight":
            total += km * EMISSION_FACTORS["flight_km"]

    if meal == "beef":
        total += EMISSION_FACTORS["beef_meal"]
    elif meal == "veg":
        total += EMISSION_FACTORS["veg_meal"]

    return round(total, 2)

# ---------------- AI TIPS ---------------- #
def get_ai_tips(total_emission):
    if not model:
        return [
            "Cycle instead of driving to cut emissions by 75%",
            "Choose plant-based meals to save up to 90%",
            "Combine trips to reduce fuel usage"
        ]

    prompt = f"""
    User emitted {total_emission} kg CO2 today.
    Give 3 short, practical, friendly tips to reduce carbon footprint.
    Keep it concise.
    """

    response = model.generate_content(prompt)
    return response.text.strip().split("\n")[:3]
