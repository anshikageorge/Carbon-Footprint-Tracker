import streamlit as st
from datetime import date

from carbon_agent import (
    calculate_emissions,
    compare_to_target,
    generate_reduction_tips,
    get_ai_recommendation
)

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="CarbonFootprintAgent v2.0",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 CarbonFootprintAgent v2.0")
st.caption("SDG 13 – Climate Action | IBM SkillsBuild Capstone")

# -----------------------------
# Session State (Weekly Tracking)
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# Layout
# -----------------------------
col1, col2 = st.columns(2)

# =============================
# 📱 CHAT INTERFACE
# =============================
with col1:
    st.subheader("📱 Chat Interface")

    user_text = st.text_input(
        "Describe your activities (e.g. 'Drove 30km, ate beef, used AC 2 hours')"
    )

    if st.button("Analyze"):
        # Simple demo mapping (can be upgraded later with NLP)
        activities = {
            "transport": {"car": 30},
            "energy": {"ac": 2},
            "food": {"beef": 1},
            "waste": {}
        }

        daily_total, breakdown = calculate_emissions(activities)

        record = {
            "date": str(date.today()),
            "daily_total": daily_total,
            "breakdown": breakdown
        }

        st.session_state.history.append(record)

        st.json({
            "daily_total": daily_total,
            "breakdown": breakdown,
            "vs_target": compare_to_target(daily_total),
            "tips": generate_reduction_tips(breakdown)
        })

# =============================
# 📊 DASHBOARD + CHART
# =============================
with col2:
    st.subheader("📊 Metrics Dashboard")

    if st.session_state.history:
        latest = st.session_state.history[-1]

        st.metric(
            label="Daily Carbon Footprint (kg CO₂)",
            value=latest["daily_total"],
            delta=latest["daily_total"] - 2
        )

        st.write("**Target:** 2 kg/day")

        st.subheader("📈 Weekly Progress")
        values = [item["daily_total"] for item in st.session_state.history]
        st.line_chart(values)

        st.subheader("💡 Personalized Tips")
        for tip in generate_reduction_tips(latest["breakdown"]):
            st.write(tip)

        st.subheader("🤖 Gemini AI Recommendations")
        st.write(get_ai_recommendation(latest["daily_total"]))

    else:
        st.info("No activity data yet. Use the chat to begin.")
