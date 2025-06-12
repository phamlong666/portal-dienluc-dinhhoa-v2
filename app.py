
import streamlit as st
import pandas as pd
from PIL import Image
import datetime

st.set_page_config(page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa", layout="wide")

# ================== GIAO DIỆN CHÍNH ==================
st.title("🧠 Trung tâm điều hành số - Điện lực Định Hóa")

# ================== NÚT CHỨC NĂNG ==================
col1, col2 = st.columns(2)
with col1:
    if st.button("📑 Phục vụ họp"):
        with st.form("phuc_vu_hop_form"):
            ten = st.text_input("Tên cuộc họp")
            ngay = st.date_input("Ngày họp", format="DD/MM/YYYY")
            gio = st.time_input("Giờ họp")
            noi_dung = st.text_area("Nội dung cuộc họp")
            file_upload = st.file_uploader("📎 Tải file đính kèm", accept_multiple_files=True)

            submit = st.form_submit_button("💾 Lưu nội dung họp")

            if submit:
                st.success("✅ Lịch sử cuộc họp đã được lưu")
                st.write(f"📅 {ngay.strftime('%d/%m/%Y')} {gio} – {ten}")
                st.write(noi_dung)
                if file_upload:
                    for f in file_upload:
                        if f.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                            st.image(f, width=250)
                        else:
                            st.write(f"📎 Tệp: {f.name}")

with col2:
    if st.button("⏰ Nhắc việc"):
        with st.form("nhac_viec_form"):
            viec = st.text_input("Công việc cần nhắc")
            thoi_gian = st.time_input("Giờ cần nhắc")
            ngay_nhac = st.date_input("Ngày nhắc", datetime.date.today(), format="DD/MM/YYYY")
            submit_nhac = st.form_submit_button("🔔 Tạo nhắc việc")
            if submit_nhac:
                st.success(f"✅ Đã tạo nhắc việc vào {ngay_nhac.strftime('%d/%m/%Y')} lúc {thoi_gian}")
