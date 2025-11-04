import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# ---------- Title ----------
st.title("🔔 Smart Reminder App")
st.write("Set your own date and exact time for any event — no restrictions!")

# ---------- Load / Create CSV ----------
csv_file = "reminders.csv"

# Create or validate CSV file
if not os.path.exists(csv_file):
    reminders = pd.DataFrame(columns=["Task", "Date", "Time"])
    reminders.to_csv(csv_file, index=False)
else:
    reminders = pd.read_csv(csv_file)

# Ensure correct columns
expected_cols = ["Task", "Date", "Time"]
if list(reminders.columns) != expected_cols:
    reminders = pd.DataFrame(columns=expected_cols)
    reminders.to_csv(csv_file, index=False)

# ---------- Add new reminder ----------
st.subheader("➕ Add a New Reminder")

task = st.text_input("Reminder Title / Description")
date = st.date_input("Date")
time_input = st.time_input("Time (Set hour & minute as you wish)")

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

# ---------- Check reminders ----------
st.subheader("⏰ Reminder Status")

if not reminders.empty:
    # Combine date and time into datetime
    reminders["Datetime"] = pd.to_datetime(
        reminders["Date"].astype(str) + " " + reminders["Time"].astype(str),
        errors="coerce"
    )

    current_time = datetime.now()

    for _, row in reminders.iterrows():
        task = row["Task"]
        reminder_time = row["Datetime"]

        if pd.isna(reminder_time):
            continue

        if current_time >= reminder_time and current_time <= reminder_time + timedelta(minutes=1):
            st.warning(f"🔔 **Reminder Due Now:** {task} — {row['Date']} {row['Time']}")
        elif current_time < reminder_time:
            time_left = reminder_time - current_time
            hrs, mins = divmod(time_left.seconds // 60, 60)
            st.info(f"🕒 **{task}** is due in {hrs}h {mins}m.")
        else:
            st.success(f"✅ **{task}** was completed or past due.")

else:
    st.caption("Add a few reminders to get started!")

st.caption("💾 All reminders are auto-saved to reminders.csv in your working directory.")
