import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# ---------- App Setup ----------
st.set_page_config(page_title="🕰️ Smart Reminder App", layout="centered")
st.title("🕰️ Smart Reminder App")
st.write("Add reminders with any exact hour and minute you like!")

# ---------- CSV File ----------
FILE_PATH = "reminders.csv"

# Load or create the CSV
try:
    reminders = pd.read_csv(FILE_PATH)
except FileNotFoundError:
    reminders = pd.DataFrame(columns=["Task", "Date", "Time"])

# ---------- Add Reminder ----------
st.subheader("➕ Add a New Reminder")

task = st.text_input("Task name")
date = st.date_input("Select date")

# --- Custom time input ---
# This trick removes 15-minute limitation: use a text_input instead of time_input
time_text = st.text_input(
    "Enter time in 24-hour format (HH:MM)", 
    value=datetime.now().strftime("%H:%M")
)

if st.button("Add Reminder"):
    try:
        # Validate entered time
        datetime.strptime(time_text, "%H:%M")
        new_row = {"Task": task, "Date": str(date), "Time": time_text}
        reminders = pd.concat([reminders, pd.DataFrame([new_row])], ignore_index=True)
        reminders.to_csv(FILE_PATH, index=False)
        st.success(f"✅ Added reminder for **{task}** at {date} {time_text}")
    except ValueError:
        st.error("⚠️ Invalid time format! Please use HH:MM (e.g. 19:04).")

# ---------- Display Reminders ----------
st.subheader("📋 All Reminders")

if reminders.empty:
    st.info("No reminders added yet.")
else:
    st.dataframe(reminders)

# ---------- Reminder Status ----------
st.subheader("⏰ Reminder Status")

if not reminders.empty:
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.now(tz)

    reminders["Datetime"] = pd.to_datetime(
        reminders["Date"].astype(str) + " " + reminders["Time"].astype(str),
        errors="coerce"
    )

    for _, row in reminders.iterrows():
        task_name = row["Task"]
        reminder_time = row["Datetime"]

        if pd.isna(reminder_time):
            continue

        if reminder_time.tzinfo is None:
            reminder_time = tz.localize(reminder_time)

        if now >= reminder_time and now <= reminder_time + timedelta(minutes=1):
            st.warning(f"🔔 **Reminder Due Now:** {task_name}")
        elif now < reminder_time:
            diff = reminder_time - now
            hrs, rem = divmod(int(diff.total_seconds()), 3600)
            mins = rem // 60
            st.info(f"🕒 **{task_name}** is due in {hrs}h {mins}m.")
        else:
            st.success(f"✅ **{task_name}** was due earlier.")

# ---------- Clear All ----------
if st.button("🗑️ Clear All Reminders"):
    reminders = pd.DataFrame(columns=["Task", "Date", "Time"])
    reminders.to_csv(FILE_PATH, index=False)
    st.success("🧹 All reminders cleared.")
