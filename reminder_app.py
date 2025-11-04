import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Smart Reminder App ⏰", layout="centered")
st.title("🕓 Smart Reminder App")

# Load or create reminder data
try:
    reminders = pd.read_csv("reminders.csv")
except FileNotFoundError:
    reminders = pd.DataFrame(columns=["Event","Date","Time","Advance_Minutes"])

# Form to add reminders
with st.form("reminder_form"):
    event = st.text_input("Event")
    date = st.date_input("Date")
    time_input = st.time_input("Time", value=datetime.time(9, 0))
    advance = st.number_input("Remind me (minutes before)", 0, 1440, 0)
    submitted = st.form_submit_button("Add Reminder")

if submitted:
    new_entry = {
        "Event": event,
        "Date": date.strftime("%Y-%m-%d"),
        "Time": time_input.strftime("%H:%M"),
        "Advance_Minutes": advance
    }
    reminders = pd.concat([reminders, pd.DataFrame([new_entry])], ignore_index=True)
    reminders.to_csv("reminders.csv", index=False)
    st.success("✅ Reminder added successfully!")

st.subheader("📋 All Reminders")
st.dataframe(reminders)

# Combine date + time + advance minutes
reminders["Datetime"] = pd.to_datetime(reminders["Date"] + " " + reminders["Time"])
reminders["Notify_At"] = reminders["Datetime"] - pd.to_timedelta(reminders["Advance_Minutes"], unit="m")

now = datetime.datetime.now()
due = reminders[reminders["Notify_At"] <= now]

# Show reminders due for alert
if not due.empty:
    for _, row in due.iterrows():
        st.warning(f"🚨 **{row['Event']}** is due!  \n⏰ Scheduled for: {row['Datetime']}")
        st.toast(f"Reminder: {row['Event']} is due now!", icon="⏰")
        # ✅ Browser pop-up (works on Streamlit Cloud)
        st.markdown(f"""
        <script>
        alert("⏰ Reminder: {row['Event']} is due!");
        </script>
        """, unsafe_allow_html=True)

# Auto-refresh every 60 seconds
st.markdown('<meta http-equiv="refresh" content="60">', unsafe_allow_html=True)
