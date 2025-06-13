
import streamlit as st
import pandas as pd
from PIL import Image
import os
from datetime import date, time
from io import BytesIO
from fpdf import FPDF
from docx import Document

# Cấu hình trang
st.set_page_config(page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa", layout="wide")

# ========== HEADER ==========
def render_header():
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

# ========== SIDEBAR MENU ==========
def render_sidebar():
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
    </style>
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

# ========== MAIN BUTTONS ==========
def render_main_buttons():
    st.markdown("""
    <div style="display: flex; justify-content: center; flex-wrap: wrap;">
        <a href="https://terabox.com/s/1cegqu7nP7rd0BdL_MIyrtA" target="_blank" class="sidebar-button">📦 Bigdata_Terabox</a>
        <a href="https://chat.openai.com/c/2d132e26-7b53-46b3-bbd3-8a5229e77973" target="_blank" class="sidebar-button">🤖 AI. PHẠM HỒNG LONG</a>
        <a href="https://www.youtube.com" target="_blank" class="sidebar-button">🎬 video tuyên truyền</a>
        <a href="https://www.dropbox.com/scl/fo/yppcs3fy1sxrilyzjbvxa/APan4-c_N5NwbIDtTzUiuKo?dl=0" target="_blank" class="sidebar-button">📄 Báo cáo CMIS</a>
    </div>
    """, unsafe_allow_html=True)

# ========== PHỤC VỤ HỌP ==========
def render_meeting_form():
    CSV_FILE = "lich_su_cuoc_hop.csv"
    UPLOAD_FOLDER = "uploaded_files"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    def load_data():
        if os.path.exists(CSV_FILE):
            return pd.read_csv(CSV_FILE)
        return pd.DataFrame(columns=["Ngày", "Giờ", "Tên cuộc họp", "Nội dung", "File đính kèm"])

    def save_data(row):
        df = load_data()
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)

    def create_word_report(row):
        doc = Document()
        doc.add_heading("Biên bản cuộc họp", 0)
        doc.add_paragraph(f"Ngày: {row.get('Ngày', '')} {row.get('Giờ', '')}")
        doc.add_paragraph(f"Tên cuộc họp: {row.get('Tên cuộc họp', '')}")
        doc.add_paragraph("Nội dung:")
        doc.add_paragraph(str(row.get("Nội dung", "") or ""))
        stream = BytesIO()
        doc.save(stream)
        stream.seek(0)
        return stream

    def create_pdf_report(row):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, f"Biên bản cuộc họp\n\nNgày: {row['Ngày']} {row['Giờ']}\nTên cuộc họp: {row['Tên cuộc họp']}\n\nNội dung:\n{row['Nội dung']}")
        stream = BytesIO()
        pdf.output(stream)
        stream.seek(0)
        return stream

    with st.expander("📑 Phục vụ họp – Ghi nội dung và xuất báo cáo", expanded=False):
        with st.form("form_hop"):
            ten = st.text_input("📌 Tên cuộc họp")
            ngay = st.date_input("📅 Ngày họp")
            gio = st.time_input("⏰ Giờ họp", time(8, 0))
            noidung = st.text_area("📝 Nội dung cuộc họp")
            files = st.file_uploader("📎 Tải file đính kèm", accept_multiple_files=True)
            submit = st.form_submit_button("💾 Lưu nội dung họp")

        if submit:
            filenames = []
            for f in files:
                save_path = os.path.join(UPLOAD_FOLDER, f.name)
                with open(save_path, "wb") as out_file:
                    out_file.write(f.read())
                filenames.append(f.name)
            save_data({
                "Ngày": ngay.strftime("%d/%m/%Y"),
                "Giờ": gio.strftime("%H:%M"),
                "Tên cuộc họp": ten,
                "Nội dung": noidung,
                "File đính kèm": ";".join(filenames)
            })
            st.success("✅ Đã lưu nội dung cuộc họp")

        df = load_data()
        if not df.empty:
            st.subheader("📚 Lịch sử cuộc họp đã được lưu")
            for idx, row in df.iterrows():
                file_list = row["File đính kèm"].split(";") if row["File đính kèm"] else []
                for file in file_list:
                    st.write(f"📎 {file}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    file = create_word_report(row)
                    st.download_button("📤 Xuất Word", file, file_name=f"{row['Tên cuộc họp']}.docx")
                with col2:
                    file = create_pdf_report(row)
                    st.download_button("📤 Xuất PDF", file, file_name=f"{row['Tên cuộc họp']}.pdf")
                with col3:
                    if st.button("🗑️ Xóa cuộc họp", key=f"delete_{idx}"):
                        df.drop(index=idx, inplace=True)
                        df.to_csv(CSV_FILE, index=False)
                        st.experimental_rerun()

# ========== NHẮC VIỆC ==========
def render_reminder_form():
    with st.expander("⏰ Nhắc việc", expanded=False):
        with st.form("form_nhac"):
            viec = st.text_input("🔔 Việc cần nhắc")
            ngay_nhac = st.date_input("📅 Ngày nhắc", date.today())
            gio_nhac = st.time_input("⏰ Giờ nhắc", time(7,30))
            submit_nhac = st.form_submit_button("📌 Tạo nhắc việc")

        if submit_nhac:
            st.success(f"✅ Đã tạo nhắc việc: {viec} lúc {gio_nhac.strftime('%H:%M')} ngày {ngay_nhac.strftime('%d/%m/%Y')}")

# ========== MAIN ==========
def main():
    render_sidebar()
    render_header()
    render_main_buttons()
    render_meeting_form()
    render_reminder_form()

main()
