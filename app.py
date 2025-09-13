import streamlit as st
import os
import json
from datetime import date
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# 🔧 Seitenlayout konfigurieren
st.set_page_config(page_title="🧘 Habit Tracker", layout="centered")

# 📁 habits.json laden oder neu erstellen
habits_path = "habits.json"
if os.path.exists(habits_path):
    try:
        with open(habits_path, "r") as f:
            habits = json.load(f)
    except json.JSONDecodeError:
        habits = {}
else:
    habits = {}

# 🧠 Begrüßung
st.title("🌱 Minimalistischer Habit Tracker mit KI-Coach")
st.markdown("Tracke deine täglichen Gewohnheiten – bleib dran, wachse Schritt für Schritt.")

# ➕ Neue Gewohnheit hinzufügen
new_habit = st.text_input("Neue Gewohnheit hinzufügen")
if st.button("Hinzufügen") and new_habit:
    if new_habit not in habits:
        habits[new_habit] = []
        st.success(f"'{new_habit}' wurde hinzugefügt!")
    else:
        st.info(f"'{new_habit}' existiert bereits.")

# 📅 Heute tracken
today = str(date.today())
st.markdown("## ✅ Heute erledigt?")
data_changed = False  # Flag zum Speichern

for habit in habits:
    if st.checkbox(f"{habit}", key=habit):
        if today not in habits[habit]:
            habits[habit].append(today)
            data_changed = True

# 📊 Fortschritt anzeigen
st.markdown("## 📈 Fortschritt")
for habit, dates in habits.items():
    streak = len(dates)
    st.markdown(f"**{habit}** – {streak} Tage")
    st.progress(min(streak / 30, 1.0))  # Ziel: 30 Tage

    if streak >= 5:
        st.success(f"🔥 Super! Du hast '{habit}' schon {streak} Tage durchgezogen!")
    elif streak == 0:
        st.warning(f"⏳ Zeit, mit '{habit}' zu starten!")

# 🤖 KI-Coach mit distilgpt2
st.markdown("## 🧠 KI-Coach Motivation")

model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
coach = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)

input_text = "Gib mir Motivation für jemanden, der seine Gewohnheiten durchhält:"
output = coach(input_text, max_length=50, num_return_sequences=1)
motivation = output[0]['generated_text']
st.success("🧠 KI-Coach sagt: " + motivation)

# 💾 Daten speichern nur bei Änderung
if data_changed or new_habit:
    with open(habits_path, "w") as f:
        json.dump(habits, f, indent=2)
