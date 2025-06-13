
import streamlit as st
import pandas as pd
import os
from datetime import date, time

REMINDERS_FILE = "nhac_viec.csv"

st.title("⏰ Nhắc việc")

with st.expander("➕ Thêm việc cần nhắc", expanded=False):
    with st.form("form_nhac"):
        viec = st.text_input("🔔 Việc cần nhắc")
        ngay = st.date_input("📅 Ngày nhắc", date.today())
        gio = st.time_input("⏰ Giờ nhắc", time(7, 30))
        submit = st.form_submit_button("📌 Tạo nhắc việc")

    if submit:
        new_row = {
            "Việc": viec,
            "Ngày": ngay.strftime("%d/%m/%y"),
            "Giờ": gio.strftime("%H:%M")
        }
        if os.path.exists(REMINDERS_FILE):
            df = pd.read_csv(REMINDERS_FILE)
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        else:
            df = pd.DataFrame([new_row])
        df.to_csv(REMINDERS_FILE, index=False)
        st.success("✅ Đã tạo nhắc việc!")

if os.path.exists(REMINDERS_FILE):
    st.markdown("#### 📋 Việc cần nhắc")
    df = pd.read_csv(REMINDERS_FILE)
    for idx, row in df.iterrows():
        st.write(f"📌 **{row['Việc']}** lúc {row['Giờ']} ngày {row['Ngày']}")
