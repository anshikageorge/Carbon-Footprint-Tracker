# -------------------------------
# app.py
# -------------------------------

# Optional auto-install Streamlit if missing
try:
    import streamlit as st
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
    import streamlit as st

from carbon_agent import calculate_emissions, compare_to_target, generate_reduction_tips, get_ai_recommendation

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="Carbon Footprint Tracker",
    page_icon="🌍",
    layout="centered"
)

st.title("🌱 Carbon Footprint Tracker")
st.write("Track your carbon footprint and get AI-powered suggestions.")

# -------------------------------
# User Inputs
# -------------------------------
electricity = st.number_input("⚡ Monthly Electricity Usage (kWh)", min_value=0.0, step=10.0)
ac_hours = st.number_input("❄️ AC Usage (hours)", min_value=0.0, step=1.0)
car_km = st.number_input("🚗 Transport (Car km)", min_value=0.0, step=5.0)
beef_meals = st.number_input("🍖 Beef meals", min_value=0, step=1)
chicken_meals = st.number_input("🍗 Chicken meals", min_value=0, step=1)
veg_meals = st.number_input("🥦 Vegetarian meals", min_value=0, step=1)
plastic_bottles = st.number_input("🥤 Plastic bottles used", min_value=0, step=1)

# -------------------------------
# Calculate Button
# -------------------------------
if st.button("🌍 Calculate Carbon Footprint"):
    activities = {
        "transport": {"car": car_km},
        "energy": {"electricity": electricity, "ac": ac_hours},
        "food": {"beef": beef_meals, "chicken": chicken_meals, "vegetarian": veg_meals},
        "waste": {"plastic": plastic_bottles}
    }

    daily_total, breakdown = calculate_emissions(activities)
    vs_target = compare_to_target(daily_total)
    tips = generate_reduction_tips(breakdown)
    ai_advice = get_ai_recommendation(daily_total)

    st.success(f"🌱 Estimated carbon footprint: **{daily_total} kg CO₂/day**")
    st.write(f"📊 Compared to target: {vs_target}")
    
    st.subheader("♻️ Reduction Tips (Rule-based)")
    for t in tips:
        st.write(f"- {t}")

    st.subheader("🤖 Gemini AI Suggestions")
    st.write(ai_advice)
