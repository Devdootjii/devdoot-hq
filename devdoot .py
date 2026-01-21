import streamlit as st
import datetime
import pandas as pd
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Devdoot HQ", page_icon="🦅", layout="wide")

# --- FILE PATHS (Yahan Data Save Hoga) ---
ATTENDANCE_FILE = "attendance_log.csv"
TASK_FILE = "task_log.csv"

# --- HELPER FUNCTIONS (System ka Engine) ---
# Function 1: Attendance Load karna
def load_attendance():
    if not os.path.exists(ATTENDANCE_FILE):
        return pd.DataFrame(columns=["Date", "Time", "Name", "Status"])
    return pd.read_csv(ATTENDANCE_FILE)

# Function 2: Attendance Save karna
def mark_attendance(name, status):
    df = load_attendance()
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    
    # Check karo ki aaj attendance pehle se to nahi lagi?
    if not df[(df['Name'] == name) & (df['Date'] == today)].empty:
        return False, "Attendance already marked for today!"
    
    new_data = pd.DataFrame({"Date": [today], "Time": [current_time], "Name": [name], "Status": [status]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(ATTENDANCE_FILE, index=False)
    return True, f"Success! Marked present at {current_time}"

# --- 2. BRANDING CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #111111; border-right: 2px solid #FF5F1F; }
    .stButton>button { background: linear-gradient(45deg, #FF5F1F, #FF8C00); color: white; border: none; font-weight: bold; }
    h1, h2, h3 { color: #FF5F1F !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
st.sidebar.title("🚀 Mission Control")
menu = st.sidebar.radio("Navigation", ["Dashboard", "Mark Attendance", "Task Upload", "Admin View (History)"])
team_members = ["Devdoot", "Balram", "Naina", "Ritesh", "Harsh", "Shalini"]

# --- PAGE: DASHBOARD ---
if menu == "Dashboard":
    st.title("🦅 Devdoot HQ: Dashboard")
    st.markdown("### *Real-Time Data Center*")
    
    # Real Data Show karo
    df = load_attendance()
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    present_today = df[df['Date'] == today_date].shape[0]
    
    col1, col2 = st.columns(2)
    col1.metric("📅 Aaj ki Date", today_date)
    col2.metric("🟢 Members Present Today", f"{present_today} / 6")

# --- PAGE: ATTENDANCE (ASLI KAAM) ---
elif menu == "Mark Attendance":
    st.title("✅ Mark Attendance")
    name = st.selectbox("Apna Naam Select Karein", team_members)
    
    if st.button("MARK PRESENT 🔥"):
        success, msg = mark_attendance(name, "Present")
        if success:
            st.balloons()
            st.success(msg)
        else:
            st.warning(msg) # Agar duplicate hai to warning dega

# --- PAGE: ADMIN VIEW (Jadu) ---
elif menu == "Admin View (History)":
    st.title("📜 Attendance History")
    st.write("Ye data 'attendance_log.csv' file me save ho raha hai.")
    
    df = load_attendance()
    # Table dikhao
    st.dataframe(df.style.highlight_max(axis=0)) 
    
    # Download Button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Report (CSV)", csv, "attendance_report.csv")