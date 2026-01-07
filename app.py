import streamlit as st
import pandas as pd
import datetime
from carbon_agent import (
    parse_user_input,
    calculate_emissions,
    get_ai_tips
)

st.set_page_config(
    page_title="Carbon Footprint Tracker",
    page_icon="🌍",
    layout="wide"
)

# ---------------- SESSION STORAGE ---------------- #
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- HEADER ---------------- #
st.title("🌱 Carbon Footprint Tracker")
st.caption("Talk to your Carbon Coach • SDG 13")

# ---------------- CHAT + CHART LAYOUT ---------------- #
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("📱 Chat Interface")
    user_input = st.text_input(
        "Describe your activity",
        placeholder="e.g. Drove 30km and had beef dinner"
    )

    if st.button("Analyze"):
        km, transport, meal = parse_user_input(user_input)
        emission = calculate_emissions(km, transport, meal)

        entry = {
            "date": datetime.date.today(),
            "activity": user_input,
            "emission": emission
        }

        st.session_state.history.append(entry)

        st.success(f"🌍 Emissions: **{emission} kg CO₂e**")

        st.subheader("💡 Personalized Tips")
        tips = get_ai_tips(emission)
        for tip in tips:
            st.write("•", tip)

with col2:
    st.subheader("📈 Progress Chart")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        df["date"] = pd.to_datetime(df["date"])

        chart = df.groupby("date")["emission"].sum()
        st.line_chart(chart)
    else:
        st.info("No data yet. Start logging activities!")

# ---------------- DASHBOARD ---------------- #
st.divider()
st.subheader("📊 Metrics Dashboard")

if st.session_state.history:
    total = sum(item["emission"] for item in st.session_state.history)
    target = 2.0

    c1, c2, c3 = st.columns(3)
    c1.metric("Total CO₂ (kg)", round(total, 2))
    c2.metric("Daily Target", f"{target} kg")
    c3.metric("Status", "⚠️ Above Target" if total > target else "✅ On Track")
else:
    st.info("Dashboard will appear after first entry.")
