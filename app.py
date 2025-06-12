
import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa", layout="wide")

st.markdown("""
    <style>
        section[data-testid="stSidebar"] > div:first-child {
            max-height: 95vh;
            overflow-y: auto;
        }

        .sidebar-button {
            display: block;
            background-color: #42A5F5;
            color: white;
            padding: 10px;
            border-radius: 8px;
            margin: 5px 0;
            font-weight: bold;
            box-shadow: 1px 1px 3px rgba(0,0,0,0.3);
            transition: all 0.2s ease-in-out;
            text-decoration: none;
        }

        .sidebar-button:hover {
            background-color: #1E88E5 !important;
            transform: translateY(-2px);
            box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
        }

        .main-button {
            display: inline-block;
            background-color: #FFCC80;
            color: white;
            text-align: center;
            padding: 22px 30px;
            border-radius: 14px;
            font-weight: bold;
            text-decoration: none;
            margin: 14px;
            transition: 0.3s;
            font-size: 24px;
        }

        .main-button:hover {
            transform: scale(1.05);
            box-shadow: 3px 3px 12px rgba(0,0,0,0.3);
        }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 10])
with col1:
    try:
        logo = Image.open("assets/logo_hinh_tron_hoan_chinh.png")
        st.image(logo, width=70)
    except:
        st.warning("⚠️ Không tìm thấy logo.")

with col2:
    st.markdown("""
        <h1 style='color:#003399; font-size:42px; margin-top:18px;'>
        Trung tâm điều hành số - phần mềm Điện lực Định Hóa
        </h1>
        <p style='font-size:13px; color:gray;'>Bản quyền © 2025 by Phạm Hồng Long & Brown Eyes</p>
    """, unsafe_allow_html=True)

sheet_url = "https://docs.google.com/spreadsheets/d/18kYr8DmDLnUUYzJJVHxzit5KCY286YozrrrIpOeojXI/gviz/tq?tqx=out:csv"

try:
    df = pd.read_csv(sheet_url)
    df = df[['Tên ứng dụng', 'Liên kết', 'Nhóm chức năng']].dropna()

    grouped = df.groupby('Nhóm chức năng')

    st.sidebar.markdown("<h3 style='color:#003399'>📚 Danh mục hệ thống</h3>", unsafe_allow_html=True)

    for group_name, group_data in grouped:
        with st.sidebar.expander(f"📂 {group_name}", expanded=False):
            for _, row in group_data.iterrows():
                label = row['Tên ứng dụng']
                link = row['Liên kết']
                st.markdown(f"""
                    <a href="{link}" target="_blank" class="sidebar-button">
                        🚀 {label}
                    </a>
                """, unsafe_allow_html=True)
except Exception as e:
    st.sidebar.error(f"🚫 Không thể tải menu từ Google Sheet. Lỗi: {e}")

st.info("""
👋 Chào mừng anh Long đến với Trung tâm điều hành số - phần mềm Điện lực Định Hóa

📌 **Các tính năng nổi bật:**
- Phân tích thất bại, báo cáo kỹ thuật
- Lưu trữ và truy xuất lịch sử GPT
- Truy cập hệ thống nhanh chóng qua Sidebar

✅ Mọi bản cập nhật chỉ cần chỉnh sửa Google Sheet đều tự động hiển thị!
""")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="display: flex; justify-content: center; flex-wrap: wrap;">
    <a href="https://terabox.com/s/1cegqu7nP7rd0BdL_MIyrtA" target="_blank" class="main-button">📦 Bigdata_Terabox</a>
    <a href="https://chat.openai.com/c/2d132e26-7b53-46b3-bbd3-8a5229e77973" target="_blank" class="main-button">🤖 AI. PHẠM HỒNG LONG</a>
    <a href="https://www.youtube.com" target="_blank" class="main-button">🎬 video tuyên truyền</a>
    <a href="https://www.dropbox.com/scl/fo/yppcs3fy1sxrilyzjbvxa/APan4-c_N5NwbIDtTzUiuKo?dl=0" target="_blank" class="main-button">📄 Báo cáo CMIS</a>
</div>
""", unsafe_allow_html=True)



# ================== PHỤC VỤ HỌP ==================
with st.expander("📝 Phục vụ họp – Ghi nội dung và xuất báo cáo", expanded=False):
    with st.form("form_phuc_vu_hop"):
        col1, col2 = st.columns(2)
        with col1:
            ten = st.text_input("Tên cuộc họp")
            ngay = st.date_input("Ngày họp")
            gio = st.time_input("Giờ họp")
        with col2:
            dia_diem = st.text_input("Địa điểm họp")
            nguoi_chu_tri = st.text_input("Người chủ trì")
            nguoi_ghi = st.text_input("Người ghi")

        noi_dung = st.text_area("Nội dung chính", height=180)
        ket_luan = st.text_area("Kết luận / Giao việc", height=180)
        submit = st.form_submit_button("💾 Lưu và tạo báo cáo")
    
        submit = st.form_submit_button("💾 Lưu và tạo báo cáo")
    # --- Tải file đính kèm nâng cao ---
    uploaded_files = st.file_uploader("📎 Tải lên tài liệu đính kèm (Word, PDF, Excel, ảnh...)", accept_multiple_files=True)
    file_states = {}

    if uploaded_files:
        for i, f in enumerate(uploaded_files):
            col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
            with col1:
                st.write(f"📄 **{f.name}**")
            with col2:
                if f.type.startswith("image/"):
                    st.image(f, width=150)
                elif f.type == "application/pdf":
                    st.write("📄 Xem PDF không hỗ trợ trực tiếp.")
            with col3:
                st.download_button("⬇️", f, file_name=f.name, key=f"download_{i}")
            with col4:
                if st.button("❌", key=f"delete_{i}"):
                    st.warning(f"Đã xoá tạm file: {f.name}")

    uploaded_files = st.file_uploader("📎 Tải lên tài liệu đính kèm (Word, PDF, Excel, ảnh...)", accept_multiple_files=True)

    if uploaded_files:
        for f in uploaded_files:
            st.write(f"📄 {f.name}")
            if f.type.startswith("image/"):
                st.image(f, width=300)
            elif f.type == "application/pdf":
                st.download_button(f"📥 Tải {f.name}", f, file_name=f.name)
            else:
                st.download_button(f"📥 Tải {f.name}", f, file_name=f.name)

    # --- Nút xóa cuộc họp (xóa nội dung đang nhập) ---
    if st.button("🗑️ Xóa nội dung cuộc họp đang nhập"):
        st.success('Đã xoá nội dung đang nhập. Hãy làm mới trang nếu cần.')


    if submit:
        import os
        from docx import Document
        from datetime import datetime

        doc = Document()
        doc.add_heading(f'BÁO CÁO CUỘC HỌP', 0)
        doc.add_paragraph(f"📅 Thời gian: {ngay.strftime('%d/%m/%y')} lúc {gio.strftime('%H:%M')}")
        doc.add_paragraph(f"📍 Địa điểm: {dia_diem}")
        doc.add_paragraph(f"👤 Người chủ trì: {nguoi_chu_tri}")
        doc.add_paragraph(f"📝 Người ghi: {nguoi_ghi}")
        doc.add_paragraph(f"🔖 Tên cuộc họp: {ten}")
        doc.add_heading("1. Nội dung chính", level=1)
        doc.add_paragraph(noi_dung)
        doc.add_heading("2. Kết luận & Giao việc", level=1)
        doc.add_paragraph(ket_luan)

        file_name = f"bao_cao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        doc.save(file_name)
        with open(file_name, "rb") as f:
            st.success("📚 Lịch sử cuộc họp đã được lưu")
            st.download_button("📥 Tải file Word", f, file_name, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
