
import streamlit as st
import pandas as pd
import os
from datetime import date, time

REMINDERS_FILE = "nhac_viec.csv"
EMAIL_MACC_DINH = "phamlong666@gmail.com"

st.title("⏰ Nhắc việc")

# Tạo mới danh sách nhắc việc
if st.button("🆕 Tạo mới danh sách nhắc việc"):
    df = pd.DataFrame(columns=["Việc", "Ngày", "Giờ", "Email"])
    df.to_csv(REMINDERS_FILE, index=False)
    st.success("✅ Đã khởi tạo mới danh sách nhắc việc.")

with st.expander("➕ Thêm việc cần nhắc", expanded=False):
    with st.form("form_nhac"):
        viec = st.text_input("🔔 Việc cần nhắc")
        ngay = st.date_input("📅 Ngày nhắc", date.today())
        gio = st.time_input("⏰ Giờ nhắc", time(7, 30))
        email = st.text_input("📧 Gửi tới", value=EMAIL_MACC_DINH)
        submit = st.form_submit_button("📌 Tạo nhắc việc")

    if submit:
        new_row = {
            "Việc": viec,
            "Ngày": ngay.strftime("%d/%m/%y"),
            "Giờ": gio.strftime("%H:%M"),
            "Email": email
        }
        if os.path.exists(REMINDERS_FILE):
            df = pd.read_csv(REMINDERS_FILE)
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        else:
            df = pd.DataFrame([new_row])
        df.to_csv(REMINDERS_FILE, index=False)
        st.success("✅ Đã tạo nhắc việc!")

# Hiển thị danh sách nhắc việc
if os.path.exists(REMINDERS_FILE):
    st.markdown("#### 📋 Việc cần nhắc")
    df = pd.read_csv(REMINDERS_FILE)
    for idx, row in df.iterrows():
        col1, col2 = st.columns([6,1])
        with col1:
            st.write(f"📌 **{row['Việc']}** lúc {row['Giờ']} ngày {row['Ngày']} → {row['Email']}")
        with col2:
            if st.button("❌", key=f"xoa_{idx}"):
                df.drop(index=idx, inplace=True)
                df.to_csv(REMINDERS_FILE, index=False)
                st.experimental_rerun()
