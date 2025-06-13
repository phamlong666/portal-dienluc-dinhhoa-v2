
# ========== MODULE: NHẮC VIỆC ==========
import streamlit as st
import pandas as pd
import os
from datetime import date, time, datetime
from PIL import Image

def nhac_viec():
        from datetime import date, time
        REMINDERS_FILE = "data/nhac_viec.csv"
    EMAIL_MAC_DINH = "phamlong666@gmail.com"
        st.header("⏰ Nhắc việc")
        if st.button("🆕 Tạo mới danh sách nhắc việc"):
    df = pd.DataFrame(columns=["Việc", "Ngày", "Giờ", "Email"])
    df.to_csv(REMINDERS_FILE, index=False)
    st.success("✅ Đã khởi tạo mới danh sách nhắc việc.")
        with st.expander("➕ Thêm việc cần nhắc", expanded=False):
    with st.form("form_nhac"):
    viec = st.text_input("🔔 Việc cần nhắc")
    ngay = st.date_input("📅 Ngày nhắc", date.today())
    gio = st.time_input("⏰ Giờ nhắc", time(7, 30))
    email = st.text_input("📧 Gửi tới", value=EMAIL_MAC_DINH)
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
        # ========== MODULE: PHỤC VỤ HỌP ==========
def phuc_vu_hop():
        from datetime import time
    from io import BytesIO
    from PIL import Image
        DATA_FILE = "data/lich_su_cuoc_hop.csv"
    UPLOAD_FOLDER = "uploaded_files"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        st.header("📑 Phục vụ họp")
        if "temp_files" not in st.session_state:
    st.session_state["temp_files"] = []
        with st.expander("➕ Thêm cuộc họp mới / Xem lại", expanded=False):
    with st.form("form_hop"):
    ten = st.text_input("📌 Tên cuộc họp")
    ngay = st.date_input("📅 Ngày họp")
    gio = st.time_input("⏰ Giờ họp", time(8, 0))
    noidung = st.text_area("📝 Nội dung")
    uploaded_files = st.file_uploader("📎 Đính kèm file", accept_multiple_files=True)
        if uploaded_files:
    for f in uploaded_files:
    if f.name not in [f.name for f in st.session_state["temp_files"]]:
    st.session_state["temp_files"].append(f)
        st.markdown("#### 📁 File đã chọn:")
    updated_files = []
    for f in st.session_state["temp_files"]:
    col1, col2 = st.columns([6, 1])
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
        if os.path.exists(DATA_FILE):
    st.markdown("#### 📚 Danh sách cuộc họp đã lưu")
    df = pd.read_csv(DATA_FILE)
    df.reset_index(drop=True, inplace=True)
        for idx, row in df.iterrows():
    with st.expander(f"📌 {row.get('Tên cuộc họp', '')} – {row.get('Ngày', '')} {row.get('Giờ', '')}", expanded=False):
    st.write("📝", row.get("Nội dung", "Không có nội dung"))
        file_list = str(row.get("Tệp", "")).split(";") if pd.notna(row.get("Tệp", "")) else []
    for file in file_list:
    file_path = os.path.join(UPLOAD_FOLDER, file)
    if os.path.exists(file_path):
    st.write(f"📎 {file}")
    if file.lower().endswith((".jpg", ".jpeg", ".png")):
    st.image(Image.open(file_path), caption=file, use_column_width=True)
    with open(file_path, "rb") as f:
    st.download_button("⬇️ Tải xuống", f.read(), file_name=file, key=f"dl_{idx}_{file}")
        with st.form(f"form_xoa_{idx}"):
    unique_key = f"xoa_{idx}_{row.get('Tên cuộc họp', '').replace(' ', '_')}_{row.get('Ngày', '')}_{row.get('Giờ', '')}"
    confirm_delete = st.checkbox("🗑️ Chọn xoá cuộc họp này", key=unique_key)
    submit_delete = st.form_submit_button("❗ Xác nhận xoá")
    if confirm_delete and submit_delete:
    df.drop(index=idx, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("🗑️ Đã xoá cuộc họp.")
    st.experimental_rerun()
    # ========== TRUNG TÂM ĐIỀU HÀNH SỐ ==========

import streamlit as st


st.set_page_config(page_title="Trung tâm điều hành số - EVNNPC Định Hóa", layout="wide")

st.title("🏠 Trung tâm điều hành số - EVNNPC Định Hóa")
st.markdown("### Chào mừng anh Long!")

tab = st.sidebar.radio("🔘 Chọn chức năng", ["⏰ Nhắc việc", "📑 Phục vụ họp"])

if tab == "⏰ Nhắc việc":
    nhac_viec()

elif tab == "📑 Phục vụ họp":
    phuc_vu_hop()

