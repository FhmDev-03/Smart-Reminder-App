import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
import base64

# ---------- Helper: Play alert sound ----------
def play_sound():
    # Simple beep sound using HTML audio tag
    sound_html = """
    <audio autoplay>
        <source src="data:audio/mp3;base64,SUQzAwAAAAAAQ1RTU0... (short beep sound base64)" type="audio/mp3">
    </audio>
    """
    st.markdown(sound_html, unsafe_allow_html=True)

# ---------- Title ----------
st.title("🔔 Simple Reminder App")
st.write("Keep track of birthdays, assignments, and important dates!")

# ---------- Load / Create CSV ----------
csv_file = "reminders.csv"

try:
    reminders = pd.read_csv(csv_file)
except FileNotFoundError:
    reminders = pd.DataFrame(columns=["Task", "Date", "Time"])

# ---------- Add new reminder ----------
st.subheader("Add a New Reminder")
task = st.text_input("Reminder Title / Description")
date = st.date_input("Date")
time_input = st.time_input("Time")

if st.button("➕ Add Reminder"):
    new_row = pd.DataFrame([[task, date, time_input]], columns=["Task", "Date", "Time"])
    reminders = pd.concat([reminders, new_row], ignore_index=True)
    reminders.to_csv(csv_file, index=False)
    st.success(f"Reminder added: {task} on {date} at {time_input}")

# ---------- Display reminders ----------
st.subheader("📅 Your Reminders")
if not reminders.empty:
    st.dataframe(reminders)
else:
    st.info("No reminders added yet.")

# ---------- Check for alerts ----------
st.subheader("⏰ Check Upcoming Reminders")
current_time = datetime.now()
reminders["Datetime"] = pd.to_datetime(reminders["Date"] + " " + reminders["Time"].astype(str))

for _, row in reminders.iterrows():
    reminder_time = row["Datetime"]
    if current_time >= reminder_time and current_time <= reminder_time + timedelta(minutes=1):
        st.warning(f"🔔 Reminder Due: **{row['Task']}** — {row['Date']} {row['Time']}")
        play_sound()
    elif current_time < reminder_time:
        time_left = reminder_time - current_time
        st.info(f"🕒 {row['Task']} is due in {time_left.seconds//60} minutes.")
    else:
        st.success(f"✅ {row['Task']} was completed or past due.")

st.caption("Reminders auto-save to `reminders.csv` in your working directory.")
