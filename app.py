import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from carbon_agent import calculate_emissions, generate_ai_tips

st.set_page_config(page_title="CarbonFootprintAgent v2.0", layout="wide")

st.title("🌍 CarbonFootprintAgent v2.0")
st.caption("SDG 13 – Climate Action | IBM SkillsBuild 2025 Capstone")

TARGET = 2.0  # kg/day

# Session state
if "weekly_data" not in st.session_state:
    st.session_state.weekly_data = []

# Layout
left, right = st.columns([1.2, 1])

# ---------------- CHAT INTERFACE ----------------
with left:
    st.subheader("📱 Chat Interface")

    user_input = st.text_area(
        "Describe your daily activities",
        placeholder="Drove 30km, beef dinner, used AC 2 hours, 5kWh electricity"
    )

    if st.button("Analyze Footprint"):
        breakdown, daily_total = calculate_emissions(user_input)
        st.session_state.weekly_data.append(daily_total)

        weekly_total = round(sum(st.session_state.weekly_data), 2)
        vs_target = f"{round((daily_total / TARGET) * 100, 1)}% of 2kg sustainable daily target"

        st.subheader("📊 Metrics Dashboard")
        col1, col2, col3 = st.columns(3)
        col1.metric("Daily CO₂e", f"{daily_total} kg")
        col2.metric("Weekly Total", f"{weekly_total} kg")
        col3.metric("Vs Target", vs_target)

        st.subheader("📄 JSON Output")
        st.json({
            "daily_total": daily_total,
            "weekly_total": weekly_total,
            "vs_target": vs_target,
            "breakdown": breakdown
        })

        st.subheader("💡 Personalized AI Tips")
        tips = generate_ai_tips(breakdown, daily_total)
        for tip in tips:
            st.write("•", tip)

# ---------------- PROGRESS CHART ----------------
with right:
    st.subheader("📈 Weekly Progress Chart")

    if st.session_state.weekly_data:
        df = pd.DataFrame({
            "Day": range(1, len(st.session_state.weekly_data) + 1),
            "Emissions": st.session_state.weekly_data
        })

        fig, ax = plt.subplots()
        ax.plot(df["Day"], df["Emissions"], marker="o")
        ax.axhline(TARGET, linestyle="--")
        ax.set_xlabel("Day")
        ax.set_ylabel("kg CO₂e")
        ax.set_title("Daily Emissions vs Sustainable Target")

        st.pyplot(fig)
    else:
        st.info("No data yet. Start by entering your daily activities.")
