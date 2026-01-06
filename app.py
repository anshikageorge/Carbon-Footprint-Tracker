import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from carbon_agent import calculate_emissions, generate_ai_tips

st.set_page_config("CarbonFootprintAgent v2.0", layout="wide")

DATA_FILE = "weekly_data.csv"
TARGET = 2.0  # kg/day

# ---------- LOAD / SAVE ----------
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Day", "Emissions"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# ---------- INIT ----------
if "data" not in st.session_state:
    st.session_state.data = load_data()

# ---------- UI ----------
st.title("🌍 CarbonFootprintAgent v2.0")
st.caption("SDG 13 – Climate Action | IBM SkillsBuild 2025 Capstone")

left, right = st.columns([1.2, 1])

# ---------- CHAT ----------
with left:
    st.subheader("📱 Chat Interface")

    user_input = st.text_area(
        "Describe your daily activities",
        placeholder="Drove 30km, beef dinner, used AC 2 hours, 5kWh electricity"
    )

    if st.button("Analyze Footprint"):
        breakdown, daily_total = calculate_emissions(user_input)

        day = len(st.session_state.data) + 1
        st.session_state.data.loc[len(st.session_state.data)] = [day, daily_total]
        save_data(st.session_state.data)

        weekly_total = round(st.session_state.data["Emissions"].sum(), 2)
        vs_target = f"{round((daily_total / TARGET) * 100, 1)}% of 2kg sustainable target"

        st.subheader("📊 Metrics Dashboard")
        c1, c2, c3 = st.columns(3)
        c1.metric("Daily CO₂e", f"{daily_total} kg")
        c2.metric("Weekly Total", f"{weekly_total} kg")
        c3.metric("Vs Target", vs_target)

        st.subheader("📄 JSON Output")
        st.json({
            "daily_total": daily_total,
            "weekly_total": weekly_total,
            "vs_target": vs_target,
            "breakdown": breakdown
        })

        st.subheader("💡 Personalized AI Tips")
        for tip in generate_ai_tips(breakdown, daily_total):
            st.write("•", tip)

    if st.button("🔄 Reset Weekly Data"):
        st.session_state.data = pd.DataFrame(columns=["Day", "Emissions"])
        save_data(st.session_state.data)
        st.success("Weekly data cleared")

# ---------- CHART ----------
with right:
    st.subheader("📈 Weekly Progress Chart")

    if not st.session_state.data.empty:
        fig, ax = plt.subplots()
        ax.plot(
            st.session_state.data["Day"],
            st.session_state.data["Emissions"],
            marker="o"
        )
        ax.axhline(TARGET, linestyle="--")
        ax.set_xlabel("Day")
        ax.set_ylabel("kg CO₂e")
        ax.set_title("Daily Emissions vs Sustainable Target")
        st.pyplot(fig)
    else:
        st.info("No data yet. Start tracking today.")
