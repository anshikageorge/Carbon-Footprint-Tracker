import os
import google.generativeai as genai

# -----------------------------
# Gemini Configuration
# -----------------------------
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# -----------------------------
# Emission Factors (MANDATORY)
# -----------------------------
EMISSION_FACTORS = {
    "transport": {
        "car": 0.2,
        "motorcycle": 0.1,
        "bus": 0.1,
        "train": 0.04,
        "flight": 0.25
    },
    "energy": {
        "electricity": 0.5,
        "gas": 0.2,
        "ac": 1.5
    },
    "food": {
        "beef": 10,
        "chicken": 5,
        "vegetarian": 1,
        "milk": 2
    },
    "waste": {
        "plastic": 0.5,
        "paper": 0.1
    }
}

# -----------------------------
# Core Logic
# -----------------------------
def calculate_emissions(activities):
    breakdown = {"transport": 0, "energy": 0, "food": 0, "waste": 0}

    for category, items in activities.items():
        for item, value in items.items():
            breakdown[category] += EMISSION_FACTORS[category][item] * value

    return sum(breakdown.values()), breakdown

def compare_to_target(daily_total):
    percent = round((daily_total / 2) * 100)
    return f"{percent}% of the 2kg/day sustainable target"

def generate_reduction_tips(breakdown):
    tips = []

    if breakdown["transport"] > 0:
        tips.append("🚲 Cycling or public transport can reduce transport emissions by ~75%.")

    if breakdown["food"] > 0:
        tips.append("🥗 Switching from beef to vegetarian meals can reduce food emissions by ~90%.")

    if breakdown["energy"] > 0:
        tips.append("❄️ Using fans instead of AC can reduce energy emissions by ~67%.")

    return tips[:3]

def get_ai_recommendation(daily_total):
    prompt = f"""
    My daily carbon footprint is {daily_total} kg CO2.
    Give exactly 3 simple, realistic actions I can take to reduce it.
    Keep it short and practical.
    """
    response = model.generate_content(prompt)
    return response.text
