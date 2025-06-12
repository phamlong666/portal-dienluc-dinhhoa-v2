import streamlit as st
import pandas as pd
from PIL import Image
import datetime
st.set_page_config(page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa", layout="wide")
# ================== CUSTOM CSS ==================
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
""", unsafe_allow_html=True)
# ================== HEADER ==================
col1, col2 = st.columns([1, 10])
with col1:
    try:
        logo = Image.open("assets/logo_hinh_tron_hoan_chinh.png")
        st.image(logo, width=70)
    except:
        st.warning("⚠️ Không tìm thấy logo.")
with col2:
        <h1 style='color:#003399; font-size:42px; margin-top:18px;'>
        Trung tâm điều hành số - phần mềm Điện lực Định Hóa
        </h1>
        <p style='font-size:13px; color:gray;'>Bản quyền © 2025 by Phạm Hồng Long & Brown Eyes</p>
    """, unsafe_allow_html=True)
# ================== MENU TỪ GOOGLE SHEET ==================
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
                    <a href="{link}" target="_blank" class="sidebar-button">
                        🚀 {label}
                    </a>
                """, unsafe_allow_html=True)
except Exception as e:
    st.sidebar.error(f"🚫 Không thể tải menu từ Google Sheet. Lỗi: {e}")
# ================== GIỚI THIỆU ==================
st.info("""
👋 Chào mừng anh Long đến với Trung tâm điều hành số - phần mềm Điện lực Định Hóa
📌 **Các tính năng nổi bật:**
- Phân tích thất bại, báo cáo kỹ thuật
- Lưu trữ và truy xuất lịch sử GPT
- Truy cập hệ thống nhanh chóng qua Sidebar
✅ Mọi bản cập nhật chỉ cần chỉnh sửa Google Sheet đều tự động hiển thị!
""")
# ================== NÚT CHỨC NĂNG CHÍNH ==================
<div style="display: flex; justify-content: center; flex-wrap: wrap;">
    <a href="https://terabox.com/s/1cegqu7nP7rd0BdL_MIyrtA" target="_blank" class="main-button">📦 Bigdata_Terabox</a>
    <a href="https://chat.openai.com/c/2d132e26-7b53-46b3-bbd3-8a5229e77973" target="_blank" class="main-button">🤖 AI. PHẠM HỒNG LONG</a>
    <a href="https://www.youtube.com" target="_blank" class="main-button">🎬 video tuyên truyền</a>
    <a href="https://www.dropbox.com/scl/fo/yppcs3fy1sxrilyzjbvxa/APan4-c_N5NwbIDtTzUiuKo?dl=0" target="_blank" class="main-button">📄 Báo cáo CMIS</a>
</div>
""", unsafe_allow_html=True)
# ================== FORM PHỤC VỤ HỌP & NHẮC VIỆC ==================
col1, col2 = st.columns(2)
with col1:
    st.subheader("📑 Phục vụ họp")
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
    st.subheader("⏰ Nhắc việc")
    with st.form("nhac_viec_form"):
        viec = st.text_input("Công việc cần nhắc")
        thoi_gian = st.time_input("Giờ cần nhắc")
        ngay_nhac = st.date_input("Ngày nhắc", datetime.date.today(), format="DD/MM/YYYY")
        submit_nhac = st.form_submit_button("🔔 Tạo nhắc việc")
        if submit_nhac:
            st.success(f"✅ Đã tạo nhắc việc vào {ngay_nhac.strftime('%d/%m/%Y')} lúc {thoi_gian}")
import streamlit as st
import pandas as pd
import os
from datetime import datetime, date, time
from io import BytesIO
from fpdf import FPDF
from docx import Document
st.set_page_config(page_title="Trung tâm điều hành số - Phục vụ họp", layout="wide")
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
    doc.add_paragraph(f"Ngày: {row['Ngày']} {row['Giờ']}")
    doc.add_paragraph(f"Tên cuộc họp: {row['Tên cuộc họp']}")
    doc.add_paragraph("Nội dung:")
    doc.add_paragraph(row["Nội dung"])
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
st.title("📑 Phục vụ họp – Ghi nội dung và xuất báo cáo")
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
                file_path = os.path.join(UPLOAD_FOLDER, file)
                col1, col2, col3 = st.columns([4,1,1])
                with col1:
                    st.write(f"📎 {file}")
                with col2:
                    if st.button("👁️ Xem", key=f"xem_{idx}_{file}"):
                        if file.lower().endswith(('.png','.jpg','.jpeg')):
                            st.image(file_path)
                        elif file.lower().endswith('.pdf'):
                with col3:
                    with open(file_path, "rb") as f:
                        st.download_button("⬇️ Tải", f.read(), file_name=file)
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                file = create_word_report(row)
                st.download_button("📤 Xuất Word", file, file_name=f"{row['Tên cuộc họp']}.docx")
            with col_b:
                file = create_pdf_report(row)
                st.download_button("📤 Xuất PDF", file, file_name=f"{row['Tên cuộc họp']}.pdf")
            with col_c:
                if st.button("🗑️ Xóa cuộc họp", key=f"delete_{idx}"):
                    df.to_csv(CSV_FILE, index=False)
                    st.experimental_rerun()
# --- Nhắc việc ---
st.subheader("⏰ Nhắc việc")
with st.form("form_nhac"):
    viec = st.text_input("🔔 Việc cần nhắc")
    ngay_nhac = st.date_input("📅 Ngày nhắc", date.today())
    gio_nhac = st.time_input("⏰ Giờ nhắc", time(7,30))
    submit_nhac = st.form_submit_button("📌 Tạo nhắc việc")
    if submit_nhac:
        st.success(f"✅ Đã tạo nhắc việc: {viec} lúc {gio_nhac.strftime('%H:%M')} ngày {ngay_nhac.strftime('%d/%m/%Y')}")