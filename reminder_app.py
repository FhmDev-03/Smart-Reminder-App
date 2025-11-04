import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# ---------- Initialize App ----------
st.set_page_config(page_title="🕰️ Smart Reminder App", layout="centered")

st.title("🕰️ Smart Reminder App")
st.write("Set reminders, track tasks, and get notified in your local time zone!")

# ---------- File Persistence ----------
FILE_PATH = "reminders.csv"

try:
    reminders = pd.read_csv(FILE_PATH)
except FileNotFoundError:
    reminders = pd.DataFrame(columns=["Task", "Date", "Time"])

# ---------- Add New Reminder ----------
st.subheader("➕ Add a New Reminder")

task = st.text_input("Task")
date = st.date_input("Date")
time = st.time_input("Time")

if st.button("Add Reminder"):
    if task:
        new_row = {"Task": task, "Date": date, "Time": time}
        reminders = pd.concat([reminders, pd.DataFrame([new_row])], ignore_index=True)
        reminders.to_csv(FILE_PATH, index=False)
        st.success(f"✅ Reminder added for **{task}** on {date} at {time}.")
    else:
        st.error("⚠️ Please enter a task before adding a reminder.")

# ---------- Display All Reminders ----------
st.subheader("📋 All Reminders")

if reminders.empty:
    st.info("No reminders added yet.")
else:
    st.dataframe(reminders)

# ---------- Check Reminder Status ----------
st.subheader("⏰ Reminder Status")

if not reminders.empty:
    # Convert Date + Time columns into one datetime
    reminders["Datetime"] = pd.to_datetime(
        reminders["Date"].astype(str) + " " + reminders["Time"].astype(str),
        errors="coerce"
    )

    # FIX: use local timezone (Asia/Kolkata)
    tz = pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(tz)

    for _, row in reminders.iterrows():
        task = r
