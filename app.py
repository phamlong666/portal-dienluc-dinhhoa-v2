
import streamlit as st
import pandas as pd
import os
from datetime import time
from io import BytesIO
from PIL import Image

DATA_FILE = "lich_su_cuoc_hop.csv"
UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.title("📑 Phục vụ họp")

# Dùng session state để giữ danh sách file đính kèm tạm thời
if "temp_files" not in st.session_state:
    st.session_state["temp_files"] = []

with st.expander("➕ Thêm cuộc họp mới / Xem lại", expanded=False):
    with st.form("form_hop"):
        ten = st.text_input("📌 Tên cuộc họp")
        ngay = st.date_input("📅 Ngày họp")
        gio = st.time_input("⏰ Giờ họp", time(8, 0))
        noidung = st.text_area("📝 Nội dung")
        uploaded_files = st.file_uploader("📎 Đính kèm file", accept_multiple_files=True)

        # Gộp vào session_state nếu có file mới
        if uploaded_files:
            for f in uploaded_files:
                if f.name not in [f.name for f in st.session_state["temp_files"]]:
                    st.session_state["temp_files"].append(f)

        # Hiển thị file đã tải và có nút xoá
        st.markdown("#### 📁 File đã chọn:")
        updated_files = []
        for f in st.session_state["temp_files"]:
            col1, col2 = st.columns([6,1])
            with col1:
                st.write(f"📎 {f.name}")
            with col2:
                if not st.checkbox(f"Xoá", key=f"remove_{f.name}"):
                    updated_files.append(f)
        st.session_state["temp_files"] = updated_files

        submit = st.form_submit_button("💾 Lưu cuộc họp")

    if submit:
        file_names = []
        for f in st.session_state["temp_files"]:
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
        st.session_state["temp_files"] = []
        st.success("✅ Đã lưu cuộc họp!")

# Hiển thị danh sách cuộc họp
if os.path.exists(DATA_FILE):
    st.markdown("#### 📚 Danh sách cuộc họp đã lưu")
    df = pd.read_csv(DATA_FILE)
    for idx, row in df.iterrows():
        with st.expander(f"📌 {row['Tên cuộc họp']} – {row['Ngày']} {row['Giờ']}", expanded=False):
            st.write("📝", row["Nội dung"])
            file_list = row["Tệp"].split(";") if row["Tệp"] else []
            for file in file_list:
                file_path = os.path.join(UPLOAD_FOLDER, file)
                if os.path.exists(file_path):
                    st.write(f"📎 {file}")
                    if file.lower().endswith((".jpg", ".jpeg", ".png")):
                        st.image(Image.open(file_path), caption=file, use_column_width=True)
                    with open(file_path, "rb") as f:
                        st.download_button("⬇️ Tải xuống", f.read(), file_name=file, key=f"dl_{idx}_{file}")
            with st.form(f"delete_form_{idx}"):
                delete = st.form_submit_button("🗑️ Xoá cuộc họp này")
                if delete:
                    df.drop(index=idx, inplace=True)
                    df.to_csv(DATA_FILE, index=False)
                    st.experimental_rerun()
