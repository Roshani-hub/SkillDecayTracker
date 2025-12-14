import streamlit as st
import json
import math
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Skill Decay Tracker", layout="centered")

st.title("🧠 Skill Decay Tracker")
st.write("Track how your skills decay over time and get smart practice guidance.")

# ---------------- LOAD DATA ----------------
with open("skill_data.json", "r") as f:
    skill_data = json.load(f)

# ---------------- SELECT SKILL ----------------
skill = st.selectbox("Select a skill", list(skill_data.keys()))

last_practice = st.date_input(
    "Last practiced date",
    datetime.date.fromisoformat(skill_data[skill]["last_practice"])
)

decay_rate = skill_data[skill]["decay_rate"]

# ---------------- DECAY CALCULATION ----------------
today = datetime.date.today()
days_passed = (today - last_practice).days

decay_score = max(
    0,
    round(100 * math.exp(-decay_rate * days_passed), 2)
)

# ---------------- ACTIVITY 1: SKILL DECAY ----------------
st.subheader("📉 Skill Strength")
st.metric("Current Skill Level", f"{decay_score}%")

days = list(range(0, days_passed + 1))
values = [100 * math.exp(-decay_rate * d) for d in days]

fig, ax = plt.subplots()
ax.plot(days, values)
ax.set_xlabel("Days since last practice")
ax.set_ylabel("Skill strength (%)")
ax.set_title("Skill Decay Curve")

st.pyplot(fig)

if decay_score < 50:
    st.warning("⚠️ Skill is decaying fast. Time to practice!")
else:
    st.success("✅ Skill is in good condition.")

# ======================================================
# 🟢 ACTIVITY 2: PRACTICE RECOMMENDATION ENGINE
# ======================================================
st.subheader("🛠️ Practice Recommendation")

if decay_score > 75:
    recommendation = "Light revision once a week"
    frequency = "1 session / week"
elif decay_score > 40:
    recommendation = "Practice core concepts"
    frequency = "3 sessions / week"
else:
    recommendation = "Immediate intensive practice"
    frequency = "Daily practice"

next_practice = today + datetime.timedelta(days=2)

st.write(f"**Recommended Action:** {recommendation}")
st.write(f"**Practice Frequency:** {frequency}")
st.write(f"**Suggested Next Practice Date:** {next_practice}")

# ======================================================
# 🟢 ACTIVITY 4: ADJACENT SKILLS + MINI ROADMAP
# ======================================================
st.subheader("🧭 Adjacent Skill Suggestions")

adjacent_skills_map = {
    "Python": ["Data Analysis", "Automation", "Machine Learning"],
    "Machine Learning": ["Deep Learning", "MLOps", "Statistics"],
    "Web Development": ["React", "Backend APIs", "UI/UX"],
    "Data Science": ["SQL", "Visualization", "Model Deployment"]
}

adjacent_skills = adjacent_skills_map.get(skill, ["Problem Solving", "System Design"])

st.write("**Related skills you can build next:**")
for s in adjacent_skills:
    st.write(f"• {s}")

st.subheader("📚 Mini Learning Roadmap")

roadmap = pd.DataFrame({
    "Stage": ["Beginner", "Intermediate", "Advanced"],
    "Focus": [
        f"Basics of {skill}",
        f"Hands-on projects with {skill}",
        f"Optimization & real-world use"
    ]
})

st.table(roadmap)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🚀 Roshani-hub | Skill Decay Tracker")
