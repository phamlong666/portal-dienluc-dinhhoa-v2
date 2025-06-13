
import streamlit as st
from datetime import time, date
from modules.supabase_client import (
    insert_cuoc_hop, get_cuoc_hop, delete_cuoc_hop,
    insert_nhac_viec, get_nhac_viec, delete_nhac_viec
)
from PIL import Image
import os

st.set_page_config(layout="wide", page_title="Trung tâm điều hành số – Điện lực Định Hóa")

st.title("💼 Trung tâm điều hành số – EVNNPC Điện lực Định Hóa")
tab1, tab2 = st.tabs(["📑 Phục vụ họp", "⏰ Nhắc việc"])

# TAB 1 – PHỤC VỤ HỌP
with tab1:
    st.subheader("📑 Quản lý nội dung cuộc họp")

    if "upload_files" not in st.session_state:
        st.session_state["upload_files"] = []

    with st.expander("➕ Thêm cuộc họp mới"):
        with st.form("form_hop"):
            ten = st.text_input("📌 Tên cuộc họp")
            ngay = st.date_input("📅 Ngày họp")
            gio = st.time_input("⏰ Giờ họp", time(8, 0))
            noidung = st.text_area("📝 Nội dung")
            files = st.file_uploader("📎 Đính kèm file", accept_multiple_files=True)

            submit = st.form_submit_button("💾 Lưu cuộc họp")

        if submit:
            file_names = [f.name for f in files]
            insert_cuoc_hop(ten, ngay, gio, noidung, file_names)
            st.success("✅ Đã lưu cuộc họp!")

    st.markdown("### 📚 Danh sách cuộc họp")
    cuoc_hop_list = get_cuoc_hop()

    for item in cuoc_hop_list:
        with st.expander(f"📌 {item['ten']} – {item['ngay']} {item['gio']}", expanded=False):
            st.write("📝", item["noidung"])
            for file in item["tep"]:
                st.write(f"📎 {file}")
            if st.button("🗑️ Xoá cuộc họp này", key=f"xoa_hop_{item['id']}"):
                delete_cuoc_hop(item["id"])
                st.experimental_rerun()

# TAB 2 – NHẮC VIỆC
with tab2:
    st.subheader("⏰ Quản lý việc cần nhắc")

    with st.expander("➕ Thêm việc cần nhắc"):
        with st.form("form_nhac"):
            viec = st.text_input("🔔 Việc cần nhắc")
            ngay = st.date_input("📅 Ngày nhắc", date.today())
            gio = st.time_input("⏰ Giờ nhắc", time(7, 30))
            email = st.text_input("📧 Gửi tới", value="phamlong666@gmail.com")
            submit = st.form_submit_button("📌 Tạo nhắc việc")

        if submit:
            insert_nhac_viec(viec, ngay, gio, email)
            st.success("✅ Đã tạo nhắc việc!")

    st.markdown("### 📋 Danh sách việc cần nhắc")
    nhac_list = get_nhac_viec()

    for item in nhac_list:
        col1, col2 = st.columns([6, 1])
        with col1:
            st.write(f"📌 **{item['viec']}** lúc {item['gio']} ngày {item['ngay']} → {item['email']}")
        with col2:
            if st.button("❌", key=f"xoa_{item['id']}"):
                delete_nhac_viec(item["id"])
                st.experimental_rerun()
