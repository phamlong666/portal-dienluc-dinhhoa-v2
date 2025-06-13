
import streamlit as st
import pandas as pd
import os
from datetime import date, time
from io import BytesIO
from docx import Document

# Cài đặt thư mục lưu file và dữ liệu
DATA_FILE = "lich_su_cuoc_hop.csv"
REMINDERS_FILE = "nhac_viec.csv"
UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Giao diện "Phục vụ họp"
def phuc_vu_hop():
    st.markdown("### 📑 Phục vụ họp", unsafe_allow_html=True)
    with st.expander("➕ Thêm cuộc họp mới / Xem lại"):
        with st.form("form_hop"):
            ten = st.text_input("📌 Tên cuộc họp")
            ngay = st.date_input("📅 Ngày họp", format="DD/MM/YY")
            gio = st.time_input("⏰ Giờ họp", time(8, 0))
            noidung = st.text_area("📝 Nội dung")
            files = st.file_uploader("📎 Đính kèm file", accept_multiple_files=True)
            submit = st.form_submit_button("💾 Lưu cuộc họp")

        if submit:
            file_names = []
            for f in files:
                save_path = os.path.join(UPLOAD_FOLDER, f.name)
                with open(save_path, "wb") as out:
                    out.write(f.read())
                file_names.append(f.name)
            new_row = {
                "Ngày": ngay.strftime("%d/%m/%y"),
                "Giờ": gio.strftime("%H:%M"),
                "Tên cuộc họp": ten,
                "Nội dung": noidung,
                "Tệp": ";".join(file_names)
            }
            if os.path.exists(DATA_FILE):
                df = pd.read_csv(DATA_FILE)
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            else:
                df = pd.DataFrame([new_row])
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ Đã lưu cuộc họp!")

    # Hiển thị danh sách cuộc họp
    if os.path.exists(DATA_FILE):
        st.markdown("#### 📚 Danh sách cuộc họp đã lưu")
        df = pd.read_csv(DATA_FILE)
        for idx, row in df.iterrows():
            with st.expander(f"📌 {row['Tên cuộc họp']} – {row['Ngày']} {row['Giờ']}"):
                st.write("📝", row["Nội dung"])
                file_list = row["Tệp"].split(";") if row["Tệp"] else []
                for file in file_list:
                    file_path = os.path.join(UPLOAD_FOLDER, file)
                    if os.path.exists(file_path):
                        st.write(f"📎 {file}")
                        with open(file_path, "rb") as f:
                            st.download_button("⬇️ Tải xuống", f.read(), file_name=file, key=f"dl_{idx}_{file}")
                if st.checkbox("🗑️ Xóa cuộc họp này", key=f"delete_{idx}"):
                    df.drop(index=idx, inplace=True)
                    df.to_csv(DATA_FILE, index=False)
                    st.experimental_rerun()

# Giao diện "Nhắc việc"
def nhac_viec():
    st.markdown("### ⏰ Nhắc việc", unsafe_allow_html=True)
    with st.expander("➕ Thêm việc cần nhắc"):
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

    # Hiển thị danh sách nhắc việc
    if os.path.exists(REMINDERS_FILE):
        st.markdown("#### 📋 Việc cần nhắc")
        df = pd.read_csv(REMINDERS_FILE)
        for idx, row in df.iterrows():
            st.write(f"📌 **{row['Việc']}** lúc {row['Giờ']} ngày {row['Ngày']}")

# Chạy toàn bộ
def main():
    st.title("🛠️ Trung tâm điều hành – Họp & Nhắc việc")
    phuc_vu_hop()
    nhac_viec()

main()
