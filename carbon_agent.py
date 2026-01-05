import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

EMISSION_FACTORS = {
    "transport": {"car": 0.2, "motorcycle": 0.1, "bus": 0.1, "train": 0.04, "flight": 0.25},
    "energy": {"electricity": 0.5, "gas": 0.2, "ac": 1.5},
    "food": {"beef": 10, "chicken": 5, "vegetarian": 1, "milk": 2},
    "waste": {"plastic": 0.5, "paper": 0.1}
}

def calculate_emissions(activities):
    breakdown = {"transport":0, "energy":0, "food":0, "waste":0}
    for category, items in activities.items():
        for item, value in items.items():
            factor = EMISSION_FACTORS[category][item]
            breakdown[category] += factor * value
    daily_total = sum(breakdown.values())
    return daily_total, breakdown

def compare_to_target(daily_total):
    percentage = round((daily_total / 2) * 100)
    return f"{percentage}% of 2kg sustainable daily target"

def generate_reduction_tips(breakdown):
    tips = []
    if breakdown["transport"] > 0:
        tips.append("Reduce private vehicle usage: use public transport or walk more.")
    if breakdown["food"] > 0:
        tips.append("Choose vegetarian meals instead of beef or chicken.")
    if breakdown["energy"] > 0:
        tips.append("Reduce AC usage and switch to energy-efficient methods.")
    return tips[:3]

def get_ai_recommendation(carbon_value):
    prompt = f"My monthly carbon footprint is {carbon_value} kg CO2. Suggest 3 practical ways I can reduce it."
    response = model.generate_content(prompt)
    return response.text
