import streamlit as st
import json
from datetime import date
import random
from transformers import pipeline

# 🔧 Seitenlayout konfigurieren
st.set_page_config(page_title="🧘 Habit Tracker", layout="centered")

# 📁 Datenbank laden oder erstellen
try:
    with open("habits.json", "r") as f:
        habits = json.load(f)
except:
    habits = {}

# 🧠 Begrüßung
st.title("🌱 Minimalistischer Habit Tracker")
st.markdown("Tracke deine täglichen Gewohnheiten – bleib dran, wachse Schritt für Schritt.")

# ➕ Neue Gewohnheit hinzufügen
new_habit = st.text_input("Neue Gewohnheit hinzufügen")
if st.button("Hinzufügen") and new_habit:
    if new_habit not in habits:
        habits[new_habit] = []
        st.success(f"'{new_habit}' wurde hinzugefügt!")

# 📅 Heute tracken
today = str(date.today())
st.markdown("## ✅ Heute erledigt?")
for habit in habits:
    if st.checkbox(f"{habit}", key=habit):
        if today not in habits[habit]:
            habits[habit].append(today)

# 📊 Fortschritt anzeigen
st.markdown("## 📈 Fortschritt")
for habit, dates in habits.items():
    streak = len(dates)
    st.markdown(f"**{habit}** – {streak} Tage")
    st.progress(min(streak / 30, 1.0))  # Ziel: 30 Tage

    # 🔥 Streak-Motivation
    if streak >= 5:
        st.success(f"🔥 Super! Du hast '{habit}' schon {streak} Tage durchgezogen!")
    elif streak == 0:
        st.warning(f"⏳ Zeit, mit '{habit}' zu starten!")

# 🤖 KI-Coach mit GPT2
st.markdown("## 🧠 KI-Coach Motivation")

# GPT2-Modell laden
coach = pipeline("text-generation", model="gpt2")

# Eingabetext für Motivation
input_text = "Gib mir Motivation für jemanden, der seine täglichen Gewohnheiten durchhält:"
motivation = coach(input_text, max_length=50, num_return_sequences=1)[0]['generated_text']

# Anzeige
st.success("🧠 KI-Coach sagt: " + motivation)

# 💾 Daten speichern
with open("habits.json", "w") as f:
    json.dump(habits, f)
