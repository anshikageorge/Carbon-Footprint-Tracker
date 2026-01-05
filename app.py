import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from carbon_agent import calculate_emissions, ai_tips

st.set_page_config(page_title="Carbon Footprint Agent", layout="wide")

st.title("🌍 CarbonFootprintAgent v2.0")
st.caption("SDG 13 – Climate Action | IBM SkillsBuild Capstone")

if "weekly" not in st.session_state:
    st.session_state.weekly = []

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📱 Chat Interface")
    user_input = st.text_area("Describe your daily activities", placeholder="Drove 30km, beef dinner, AC 2 hours")

    if st.button("Calculate"):
        breakdown, total = calculate_emissions(user_input)
        st.session_state.weekly.append(total)

        st.subheader("📊 Metrics Dashboard")
        st.metric("Daily Emissions (kg CO₂e)", round(total, 2))
        st.metric("Sustainable Target", "2 kg/day")

        st.json(breakdown)

        tips = ai_tips(breakdown)
        st.subheader("💡 Personalized Tips")
        for t in tips:
            st.write("•", t)

with col2:
    st.subheader("📈 Weekly Progress Chart")
    if st.session_state.weekly:
        df = pd.DataFrame({
            "Day": range(1, len(st.session_state.weekly) + 1),
            "Emissions": st.session_state.weekly
        })

        fig, ax = plt.subplots()
        ax.plot(df["Day"], df["Emissions"])
        ax.axhline(2, linestyle="--")
        ax.set_ylabel("kg CO₂e")
        ax.set_xlabel("Day")

        st.pyplot(fig)
