import re
import streamlit as st
import google.generativeai as genai

# ---------------- GEMINI SETUP ----------------
def setup_gemini():
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        return genai.GenerativeModel("gemini-pro")
    except:
        return None

model = setup_gemini()

# ---------------- EMISSION FACTORS ----------------
FACTORS = {
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

# ---------------- PARSER + CALCULATOR ----------------
def calculate_emissions(text):
    text = text.lower()

    breakdown = {
        "transport": 0.0,
        "food": 0.0,
        "energy": 0.0,
        "waste": 0.0
    }

    # Transport (km based)
    km_matches = re.findall(r"(\d+)\s?km", text)
    if km_matches:
        km = int(km_matches[0])
        for mode in FACTORS["transport"]:
            if mode in text:
                breakdown["transport"] += km * FACTORS["transport"][mode]

    # Food (per meal)
    for food in FACTORS["food"]:
        if food in text:
            if food == "milk":
                liters = re.findall(r"(\d+)\s?liter", text)
                breakdown["food"] += int(liters[0]) * FACTORS["food"][food] if liters else FACTORS["food"][food]
            else:
                breakdown["food"] += FACTORS["food"][food]

    # Energy
    hours = re.findall(r"(\d+)\s?hour", text)
    if "ac" in text and hours:
        breakdown["energy"] += int(hours[0]) * FACTORS["energy"]["ac"]

    kwh = re.findall(r"(\d+)\s?kwh", text)
    if kwh:
        breakdown["energy"] += int(kwh[0]) * FACTORS["energy"]["electricity"]

    # Waste
    bottles = re.findall(r"(\d+)\s?plastic", text)
    if bottles:
        breakdown["waste"] += int(bottles[0]) * FACTORS["waste"]["plastic"]

    paper = re.findall(r"(\d+)\s?paper", text)
    if paper:
        breakdown["waste"] += int(paper[0]) * FACTORS["waste"]["paper"]

    total = round(sum(breakdown.values()), 2)
    return breakdown, total

# ---------------- AI TIPS ----------------
def generate_ai_tips(breakdown, total):
    if not model:
        return [
            "Switch to public transport or walking",
            "Reduce AC usage and save energy",
            "Prefer vegetarian meals more often"
        ]

    prompt = f"""
You are CarbonFootprintAgent v2.0.
User daily emissions: {total} kg CO2e
Breakdown: {breakdown}

Rules:
- Generate EXACTLY 3 tips
- Short, actionable
- Mention percentage savings if possible
"""

    try:
        response = model.generate_content(prompt)
        tips = response.text.strip().split("\n")
        return tips[:3]
    except:
        return [
            "Use energy-efficient appliances",
            "Reduce meat consumption",
            "Avoid single-use plastics"
        ]
