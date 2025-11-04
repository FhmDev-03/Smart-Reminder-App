import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# ---------- Title ----------
st.title("🔔 Simple Reminder App")
st.write("Keep track of birthdays, assignments, and important dates easily!")

# ---------- Load / Create CSV ----------
csv_file = "reminders.csv"

# Create new CSV if it doesn't exist
if not os.path.exists(csv_file):
    reminders = pd.DataFrame(columns=["Task", "Date", "Time"])
    reminders.to_csv(csv_file, index=False)
else:
    reminders = pd.read_csv(csv_file)

# Ensure correct columns (in case CSV got corrupted)
expected_cols = ["Task", "Date", "Time"]
if list(reminders.columns) != expected_cols:
    reminders = pd.DataFrame(columns=expected_cols)
    reminders.to_csv(csv_file, index=False)

# ---------- Add new reminder ----------
st.subheader("➕ Add a New Reminder")

task = st.text_input("Reminder Title / Description")
date = st.date_input("Date")
time_input = st.time_input("Time")

if st.button("Add Reminder"):
    if task.strip() == "":
        st.error("Please enter a valid reminder title.")
    else:
        new_row = pd.DataFrame([[task, date, time_input]], columns=expected_cols)
        reminders = pd.concat([reminders, new_row], ignore_index=True)
        reminders.to_csv(csv_file, index=False)
        st.success(f"✅ Reminder added: {task} on {date} at {time_input}")

# ---------- Display reminders ----------
st.subheader("📅 Your Reminders")

if not reminders.empty:
    st.dataframe(reminders)
else:
    st.info("No reminders added yet.")

# ---------- Check for alerts ----------
st.subheader("⏰ Check Upcoming Reminders")

# Convert date + time to datetime safely
if not reminders.empty:
    reminders["Datetime"] = pd.to_datetime(
        reminders["Date"].astype(str) + " " + reminders["Time"].astype(str),
        errors="coerce"
    )

    current_time = datetime.now()

    found_alert = False

    for _, row in reminders.iterrows():
        task = str(row["Task"])
        reminder_time = row["Datetime"]

        if pd.isna(reminder_time):
            continue  # skip bad rows

        # Check if reminder is due
        if current_time >= reminder_time and current_time <= reminder_time + timedelta(minutes=1):
            st.warning(f"🔔 Reminder Due: **{task}** — {row['Date']} {row['Time']}")
            found_alert = True

        elif current_time < reminder_time:
            time_left = reminder_time - current_time
            minutes_left = time_left.seconds // 60
            st.info(f"🕒 {task} is due in {minutes_left} minutes.")

        else:
            st.success(f"✅ {task} was completed or past due.")

    if not found_alert:
        st.caption("✅ No reminders due right now.")

st.caption("Reminders auto-save to `reminders.csv` in your working directory.")
