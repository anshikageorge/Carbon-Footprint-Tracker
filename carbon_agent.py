import re
import google.generativeai as genai
import streamlit as st

# Configure Gemini safely
def setup_gemini():
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        return genai.GenerativeModel("gemini-pro")
    return None

model = setup_gemini()

# Emission factors
FACTORS = {
    "car": 0.2,
    "motorcycle": 0.1,
    "bus": 0.1,
    "train": 0.04,
    "flight": 0.25,
    "electricity": 0.5,
    "gas": 0.2,
    "ac": 1.5,
    "beef": 10,
    "chicken": 5,
    "vegetarian": 1,
    "milk": 2,
    "plastic": 0.5,
    "paper": 0.1
}

def calculate_emissions(text):
    text = text.lower()
    breakdown = {"transport": 0, "food": 0, "energy": 0, "waste": 0}

    km = re.findall(r"(\d+)\s?km", text)
    if "car" in text and km:
        breakdown["transport"] += int(km[0]) * FACTORS["car"]

    if "beef" in text:
        breakdown["food"] += FACTORS["beef"]
    if "chicken" in text:
        breakdown["food"] += FACTORS["chicken"]
    if "vegetarian" in text:
        breakdown["food"] += FACTORS["vegetarian"]

    hours = re.findall(r"(\d+)\s?hour", text)
    if "ac" in text and hours:
        breakdown["energy"] += int(hours[0]) * FACTORS["ac"]

    kwh = re.findall(r"(\d+)\s?kwh", text)
    if kwh:
        breakdown["energy"] += int(kwh[0]) * FACTORS["electricity"]

    total = sum(breakdown.values())
    return breakdown, total

def ai_tips(summary):
    if not model:
        return [
            "Use public transport instead of car",
            "Reduce AC usage",
            "Choose vegetarian meals"
        ]

    prompt = f"""
    User carbon footprint summary:
    {summary}

    Give EXACTLY 3 short, actionable tips to reduce emissions.
    """
    response = model.generate_content(prompt)
    return response.text.strip().split("\n")[:3]
