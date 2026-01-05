import streamlit as st
from carbon_agent import calculate_emissions, compare_to_target, generate_reduction_tips, get_ai_recommendation

st.set_page_config(page_title="Carbon Footprint Tracker", page_icon="🌍", layout="centered")
st.title("🌱 Carbon Footprint Tracker")
st.write("Track your carbon footprint and get AI-powered suggestions.")

# User Inputs
electricity = st.number_input("⚡ Monthly Electricity Usage (kWh)", 0.0, 1000.0, 0.0, step=5.0)
ac_hours = st.number_input("❄️ AC Usage (hours)", 0.0, 100.0, 0.0, step=1.0)
car_km = st.number_input("🚗 Transport (Car km)", 0.0, 1000.0, 0.0, step=5.0)
beef_meals = st.number_input("🍖 Beef meals", 0, 50, 0)
chicken_meals = st.number_input("🍗 Chicken meals", 0, 50, 0)
veg_meals = st.number_input("🥦 Vegetarian meals", 0, 50, 0)
plastic_bottles = st.number_input("🥤 Plastic bottles used", 0, 100, 0)

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

    st.success(f"🌱 Estimated carbon footprint: **{daily_total} kg CO₂/day**")
    st.write(f"📊 Compared to target: {vs_target}")

    st.subheader("♻️ Reduction Tips")
    for t in tips:
        st.write(f"- {t}")

    try:
        st.subheader("🤖 Gemini AI Suggestions")
        advice = get_ai_recommendation(daily_total)
        st.write(advice)
    except Exception as e:
        st.warning("AI recommendations unavailable. Check your GEMINI_API_KEY.")
