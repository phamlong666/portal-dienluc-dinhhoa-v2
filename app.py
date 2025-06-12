import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime, date, time
from io import BytesIO
from pathlib import Path
from fpdf import FPDF
from docx import Document
from PIL import Image

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Trung tâm điều hành số - Điện lực Định Hóa", layout="wide")


# ========== TÙY CHỈNH CSS ===============
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

# ========== SIDEBAR TỪ GOOGLE SHEET ==========
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
                st.markdown(f'''
                    <a href="{link}" target="_blank" class="sidebar-button">
                        🚀 {label}
                    </a>
                ''', unsafe_allow_html=True)
except Exception as e:
    st.sidebar.error(f"🚫 Không thể tải menu từ Google Sheet. Lỗi: {e}")

# ========== HEADER LOGO + CHỮ ==========
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

# ========== NÚT CHÍNH GIỮA ==========
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="display: flex; justify-content: center; flex-wrap: wrap;">
    <a href="https://terabox.com/s/1cegqu7nP7rd0BdL_MIyrtA" target="_blank" class="main-button">📦 Bigdata_Terabox</a>
    <a href="https://chat.openai.com/c/2d132e26-7b53-46b3-bbd3-8a5229e77973" target="_blank" class="main-button">🤖 AI. PHẠM HỒNG LONG</a>
    <a href="https://www.youtube.com" target="_blank" class="main-button">🎬 video tuyên truyền</a>
    <a href="https://www.dropbox.com/scl/fo/yppcs3fy1sxrilyzjbvxa/APan4-c_N5NwbIDtTzUiuKo?dl=0" target="_blank" class="main-button">📄 Báo cáo CMIS</a>
</div>
""", unsafe_allow_html=True)
# --- BIẾN TOÀN CỤC ---
CSV_FILE = "lich_su_cuoc_hop.csv"
UPLOAD_FOLDER = "uploaded_files"
NHAC_VIEC_FILE = "nhac_viec.json"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- HÀM XỬ LÝ DỮ LIỆU HỌP ---
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
    doc.add_paragraph(f"Ngày: {row['Ngày']} {row['Giờ']}")
    doc.add_paragraph(f"Tên cuộc họp: {row['Tên cuộc họp']}")
    doc.add_paragraph("Nội dung:")
    doc.add_paragraph(str(row["Nội dung"]) if pd.notna(row["Nội dung"]) else "")
    stream = BytesIO()
    doc.save(stream)
    stream.seek(0)
    return stream


def create_pdf_report(row):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    text = f"""Biên bản cuộc họp\n
    
    Ngày: {row['Ngày']} {row['Giờ']}
    Tên cuộc họp: {row['Tên cuộc họp']}
    
    Nội dung:
    {row['Nội dung']}"
    """
    pdf.multi_cell(0, 10, text)
    stream = BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')
    stream.write(pdf_bytes)
    stream.seek(0)
    return stream


# --- HÀM NHẮC VIỆC ---
def load_reminders():
    if Path(NHAC_VIEC_FILE).exists():
        with open(NHAC_VIEC_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_reminder(reminder):
    data = load_reminders()
    data.append(reminder)
    with open(NHAC_VIEC_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- GIAO DIỆN CHÍNH ---
st.markdown("<h1 style='color:#003399'>🚀 Trung tâm điều hành số - Điện lực Định Hóa</h1>", unsafe_allow_html=True)

# --- FORM PHỤC VỤ HỌP ---
with st.expander("📑 Phục vụ họp", expanded=False):
    with st.form("form_hop"):
        ten = st.text_input("📌 Tên cuộc họp")
        ngay = st.date_input("📅 Ngày họp", format="DD/MM/YYYY")
        gio = st.time_input("⏰ Giờ họp", time(8, 0))
        noidung = st.text_area("📝 Nội dung cuộc họp")
        files = st.file_uploader("📎 Tải file đính kèm", accept_multiple_files=True)
        submit = st.form_submit_button("💾 Lưu nội dung họp")

        if submit:
            filenames = []
            for f in files:
                save_path = os.path.join(UPLOAD_FOLDER, f.name)
                with open(save_path, "wb") as out:
                    out.write(f.read())
                filenames.append(f.name)
            save_data({
                "Ngày": ngay.strftime("%d/%m/%Y"),
                "Giờ": gio.strftime("%H:%M"),
                "Tên cuộc họp": ten,
                "Nội dung": noidung,
                "File đính kèm": ";".join(filenames)
            })
            st.success("✅ Đã lưu nội dung cuộc họp")

    
# Outside expander: Hiển thị lịch sử
df = load_data()
if not df.empty:
        st.subheader("📚 Lịch sử cuộc họp")
        for idx, row in df.iterrows():
            with st.expander(f"📅 {row['Ngày']} {row['Giờ']} – {row['Tên cuộc họp']}"):
                st.markdown(row["Nội dung"])
                file_list = row["File đính kèm"].split(";") if row["File đính kèm"] else []
                for file in file_list:
                    file_path = os.path.join(UPLOAD_FOLDER, file)
                    col1, col2, col3 = st.columns([4,1,1])
                    with col1:
                        st.write(f"📎 {file}")
                    with col2:
                        if st.button("👁️ Xem", key=f"xem_{idx}_{file}"):
                                                with col3:
                        with open(file_path, "rb") as f:
                            st.download_button("⬇️ Tải", f.read(), file_name=file)
                        if st.button("🗑 Xóa tài liệu", key=f"xoa_{idx}_{file}"):
                            os.remove(file_path)
                            updated_files = [f for f in file_list if f != file]
                            df.at[idx, "File đính kèm"] = ";".join(updated_files)
                            df.to_csv(CSV_FILE, index=False)
                            st.experimental_rerun()
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    word_file = create_word_report(row)
                    st.download_button("📤 Xuất Word", word_file, file_name=f"{row['Tên cuộc họp']}.docx")
                with col_b:
                    pdf_file = create_pdf_report(row)
                    st.download_button("📤 Xuất PDF", pdf_file, file_name=f"{row['Tên cuộc họp']}.pdf")
                with col_c:
                    if st.button("🗑️ Xóa cuộc họp", key=f"delete_{idx}"):
                        df.drop(idx, inplace=True)
                        df.to_csv(CSV_FILE, index=False)
                        st.experimental_rerun()

# --- NHẮC VIỆC ---
with st.expander("⏰ Nhắc việc", expanded=False):
    with st.form("form_nhac"):
        viec = st.text_input("🔔 Việc cần nhắc")
        ngay_nhac = st.date_input("📅 Ngày nhắc", date.today())
        gio_nhac = st.time_input("⏰ Giờ nhắc", time(7,30))
        submit_nhac = st.form_submit_button("📌 Tạo nhắc việc")
        if submit_nhac:
            reminder = {
                "Việc": viec,
                "Ngày": ngay_nhac.strftime("%d/%m/%Y"),
                "Giờ": gio_nhac.strftime("%H:%M")
            }
            save_reminder(reminder)
            st.success(f"✅ Đã tạo nhắc việc: {viec} lúc {reminder['Giờ']} ngày {reminder['Ngày']}")

    reminders = load_reminders()
    if reminders:
        st.markdown("### 📋 Danh sách nhắc việc đã tạo")
        df_remind = pd.DataFrame(reminders)
        st.dataframe(df_remind)