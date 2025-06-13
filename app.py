import streamlit as st
import pandas as pd
from PIL import Image
import datetime
st.markdown("""st.set_page_config(page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa", layout="wide")""", unsafe_allow_html=True)
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
"""
# ================== HEADER ==================
col1, col2 = st.columns([1, 10])
with col1:
    try:
        logo = Image.open("assets/logo_hinh_tron_hoan_chinh.png")
        st.image(logo, width=70)
    except:
st.markdown("""st.warning("⚠️ Không tìm thấy logo.")""", unsafe_allow_html=True)
with col2:
        st.markdown("""
st.markdown("""
<h1 style='color:#003399; font-size:42px; margin-top:18px;'>
        Trung tâm điều hành số - phần mềm Điện lực Định Hóa
        </h1>
        <p style='font-size:13px; color:gray;'>Bản quyền &copy; 2025 by Phạm Hồng Long & Brown Eyes</p>
"""
"""
st.markdown("""# ================== MENU TỪ GOOGLE SHEET ==================""", unsafe_allow_html=True)
sheet_url = "https://docs.google.com/spreadsheets/d/18kYr8DmDLnUUYzJJVHxzit5KCY286YozrrrIpOeojXI/gviz/tq?tqx=out:csv"
try:
    df = pd.read_csv(sheet_url)
st.markdown("""df = df[['Tên ứng dụng', 'Liên kết', 'Nhóm chức năng']].dropna()""", unsafe_allow_html=True)
st.markdown("""grouped = df.groupby('Nhóm chức năng')""", unsafe_allow_html=True)
st.markdown("""st.sidebar.markdown("<h3 style='color:#003399'>📚 Danh mục hệ thống</h3>", unsafe_allow_html=True)""", unsafe_allow_html=True)
    for group_name, group_data in grouped:
st.markdown("""with st.sidebar.expander(f"📂 {group_name}", expanded=False):""", unsafe_allow_html=True)
            for _, row in group_data.iterrows():
                label = row['Tên ứng dụng']
                link = row['Liên kết']
                    <a href="{link}" target="_blank" class="sidebar-button">
st.markdown("""🚀 {label}""", unsafe_allow_html=True)
                    </a>
"""
except Exception as e:
st.markdown("""st.sidebar.error(f"🚫 Không thể tải menu từ Google Sheet. Lỗi: {e}")""", unsafe_allow_html=True)
# ================== GIỚI THIỆU ==================
st.info("""
st.markdown("""👋 Chào mừng anh Long đến với Trung tâm điều hành số - phần mềm Điện lực Định Hóa""", unsafe_allow_html=True)
st.markdown("""📌 **Các tính năng nổi bật:**""", unsafe_allow_html=True)
- Phân tích thất bại, báo cáo kỹ thuật
- Lưu trữ và truy xuất lịch sử GPT
- Truy cập hệ thống nhanh chóng qua Sidebar
✅ Mọi bản cập nhật chỉ cần chỉnh sửa Google Sheet đều tự động hiển thị!
""")
st.markdown("""# ================== NÚT CHỨC NĂNG CHÍNH ==================""", unsafe_allow_html=True)
<div style="display: flex; justify-content: center; flex-wrap: wrap;">
st.markdown("""<a href="https://terabox.com/s/1cegqu7nP7rd0BdL_MIyrtA" target="_blank" class="main-button">📦 Bigdata_Terabox</a>""", unsafe_allow_html=True)
st.markdown("""<a href="https://chat.openai.com/c/2d132e26-7b53-46b3-bbd3-8a5229e77973" target="_blank" class="main-button">🤖 AI. PHẠM HỒNG LONG</a>""", unsafe_allow_html=True)
st.markdown("""<a href="https://www.youtube.com" target="_blank" class="main-button">🎬 video tuyên truyền</a>""", unsafe_allow_html=True)
st.markdown("""<a href="https://www.dropbox.com/scl/fo/yppcs3fy1sxrilyzjbvxa/APan4-c_N5NwbIDtTzUiuKo?dl=0" target="_blank" class="main-button">📄 Báo cáo CMIS</a>""", unsafe_allow_html=True)
</div>
"""
st.markdown("""# ================== FORM PHỤC VỤ HỌP & NHẮC VIỆC ==================""", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
st.markdown("""ten = st.text_input("Tên cuộc họp")""", unsafe_allow_html=True)
st.markdown("""ngay = st.date_input("Ngày họp", format="DD/MM/YYYY")""", unsafe_allow_html=True)
st.markdown("""gio = st.time_input("Giờ họp")""", unsafe_allow_html=True)
st.markdown("""noi_dung = st.text_area("Nội dung cuộc họp")""", unsafe_allow_html=True)
st.markdown("""file_upload = st.file_uploader("📎 Tải file đính kèm", accept_multiple_files=True)""", unsafe_allow_html=True)
st.markdown("""submit = st.form_submit_button("💾 Lưu nội dung họp")""", unsafe_allow_html=True)
        if submit:
            st.success("✅ Lịch sử cuộc họp đã được lưu")
st.markdown("""st.write(f"📅 {ngay.strftime('%d/%m/%Y')} {gio} – {ten}")""", unsafe_allow_html=True)
            st.write(noi_dung)
            if file_upload:
                for f in file_upload:
                    if f.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                        st.image(f, width=250)
                    else:
st.markdown("""st.write(f"📎 Tệp: {f.name}")""", unsafe_allow_html=True)
with col2:
        viec = st.text_input("Công việc cần nhắc")
        thoi_gian = st.time_input("Giờ cần nhắc")
        ngay_nhac = st.date_input("Ngày nhắc", datetime.date.today(), format="DD/MM/YYYY")
st.markdown("""submit_nhac = st.form_submit_button("🔔 Tạo nhắc việc")""", unsafe_allow_html=True)
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
with st.form("form_hop"):
st.markdown("""ten = st.text_input("📌 Tên cuộc họp")""", unsafe_allow_html=True)
st.markdown("""ngay = st.date_input("📅 Ngày họp", format="DD/MM/YYYY")""", unsafe_allow_html=True)
    gio = st.time_input("⏰ Giờ họp", time(8, 0))
st.markdown("""noidung = st.text_area("📝 Nội dung cuộc họp")""", unsafe_allow_html=True)
st.markdown("""files = st.file_uploader("📎 Tải file đính kèm", accept_multiple_files=True)""", unsafe_allow_html=True)
st.markdown("""submit = st.form_submit_button("💾 Lưu nội dung họp")""", unsafe_allow_html=True)
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
st.markdown("""st.subheader("📚 Lịch sử cuộc họp đã được lưu")""", unsafe_allow_html=True)
    for idx, row in df.iterrows():
            file_list = row["File đính kèm"].split(";") if row["File đính kèm"] else []
            for file in file_list:
                file_path = os.path.join(UPLOAD_FOLDER, file)
                col1, col2, col3 = st.columns([4,1,1])
                with col1:
st.markdown("""st.write(f"📎 {file}")""", unsafe_allow_html=True)
                with col2:
st.markdown("""if st.button("👁️ Xem", key=f"xem_{idx}_{file}"):""", unsafe_allow_html=True)
                        if file.lower().endswith(('.png','.jpg','.jpeg')):
                            st.image(file_path)
                        elif file.lower().endswith('.pdf'):
                with col3:
                    with open(file_path, "rb") as f:
                        st.download_button("⬇️ Tải", f.read(), file_name=file)
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                file = create_word_report(row)
st.markdown("""st.download_button("📤 Xuất Word", file, file_name=f"{row['Tên cuộc họp']}.docx")""", unsafe_allow_html=True)
            with col_b:
                file = create_pdf_report(row)
st.markdown("""st.download_button("📤 Xuất PDF", file, file_name=f"{row['Tên cuộc họp']}.pdf")""", unsafe_allow_html=True)
            with col_c:
st.markdown("""if st.button("🗑️ Xóa cuộc họp", key=f"delete_{idx}"):""", unsafe_allow_html=True)
                    df.to_csv(CSV_FILE, index=False)
                    st.experimental_rerun()
# --- Nhắc việc ---
with st.form("form_nhac"):
st.markdown("""viec = st.text_input("🔔 Việc cần nhắc")""", unsafe_allow_html=True)
st.markdown("""ngay_nhac = st.date_input("📅 Ngày nhắc", date.today())""", unsafe_allow_html=True)
    gio_nhac = st.time_input("⏰ Giờ nhắc", time(7,30))
st.markdown("""submit_nhac = st.form_submit_button("📌 Tạo nhắc việc")""", unsafe_allow_html=True)
    if submit_nhac:
        st.success(f"✅ Đã tạo nhắc việc: {viec} lúc {gio_nhac.strftime('%H:%M')} ngày {ngay_nhac.strftime('%d/%m/%Y')}")
""", unsafe_allow_html=True)



import streamlit as st
import pandas as pd
import os
from datetime import time
from io import BytesIO
from PIL import Image

DATA_FILE = "lich_su_cuoc_hop.csv"
UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.markdown("""st.title("📑 Phục vụ họp")""", unsafe_allow_html=True)

if "temp_files" not in st.session_state:
    st.session_state["temp_files"] = []

with st.expander("➕ Thêm cuộc họp mới / Xem lại", expanded=False):
    with st.form("form_hop"):
st.markdown("""ten = st.text_input("📌 Tên cuộc họp")""", unsafe_allow_html=True)
st.markdown("""ngay = st.date_input("📅 Ngày họp")""", unsafe_allow_html=True)
        gio = st.time_input("⏰ Giờ họp", time(8, 0))
st.markdown("""noidung = st.text_area("📝 Nội dung")""", unsafe_allow_html=True)
st.markdown("""uploaded_files = st.file_uploader("📎 Đính kèm file", accept_multiple_files=True)""", unsafe_allow_html=True)

        if uploaded_files:
            for f in uploaded_files:
                if f.name not in [f.name for f in st.session_state["temp_files"]]:
                    st.session_state["temp_files"].append(f)

st.markdown("""st.markdown("#### 📁 File đã chọn:")""", unsafe_allow_html=True)
        updated_files = []
        for f in st.session_state["temp_files"]:
            col1, col2 = st.columns([6, 1])
            with col1:
st.markdown("""st.write(f"📎 {f.name}")""", unsafe_allow_html=True)
            with col2:
                if not st.checkbox(f"Xoá", key=f"remove_{f.name}"):
                    updated_files.append(f)
        st.session_state["temp_files"] = updated_files

st.markdown("""submit = st.form_submit_button("💾 Lưu cuộc họp")""", unsafe_allow_html=True)

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
st.markdown("""st.markdown("#### 📚 Danh sách cuộc họp đã lưu")""", unsafe_allow_html=True)
    df = pd.read_csv(DATA_FILE)

    # Đảm bảo chỉ số tuần tự không bị lỗi sau khi xóa
    df.reset_index(drop=True, inplace=True)

    for idx, row in df.iterrows():
st.markdown("""with st.expander(f"📌 {row.get('Tên cuộc họp', '')} – {row.get('Ngày', '')} {row.get('Giờ', '')}", expanded=False):""", unsafe_allow_html=True)
st.markdown("""st.write("📝", row.get("Nội dung", "Không có nội dung"))""", unsafe_allow_html=True)

            file_list = str(row.get("Tệp", "")).split(";") if pd.notna(row.get("Tệp", "")) else []
            for file in file_list:
                file_path = os.path.join(UPLOAD_FOLDER, file)
                if os.path.exists(file_path):
st.markdown("""st.write(f"📎 {file}")""", unsafe_allow_html=True)
                    if file.lower().endswith((".jpg", ".jpeg", ".png")):
                        st.image(Image.open(file_path), caption=file, use_column_width=True)
                    with open(file_path, "rb") as f:
                        st.download_button("⬇️ Tải xuống", f.read(), file_name=file, key=f"dl_{idx}_{file}")

            # Form xác nhận xoá cuộc họp
            with st.form(f"form_xoa_{idx}"):
st.markdown("""confirm_delete = st.checkbox("🗑️ Chọn xoá cuộc họp này", key=f"xoa_{idx}")""", unsafe_allow_html=True)
                submit_delete = st.form_submit_button("❗ Xác nhận xoá")
                if confirm_delete and submit_delete:
                    df.drop(index=idx, inplace=True)
                    df.reset_index(drop=True, inplace=True)
                    df.to_csv(DATA_FILE, index=False)
st.markdown("""st.success("🗑️ Đã xoá cuộc họp.")""", unsafe_allow_html=True)
                    st.experimental_rerun()


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
st.markdown("""viec = st.text_input("🔔 Việc cần nhắc")""", unsafe_allow_html=True)
st.markdown("""ngay = st.date_input("📅 Ngày nhắc", date.today())""", unsafe_allow_html=True)
        gio = st.time_input("⏰ Giờ nhắc", time(7, 30))
st.markdown("""email = st.text_input("📧 Gửi tới", value=EMAIL_MACC_DINH)""", unsafe_allow_html=True)
st.markdown("""submit = st.form_submit_button("📌 Tạo nhắc việc")""", unsafe_allow_html=True)

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
st.markdown("""st.markdown("#### 📋 Việc cần nhắc")""", unsafe_allow_html=True)
    df = pd.read_csv(REMINDERS_FILE)
    for idx, row in df.iterrows():
        col1, col2 = st.columns([6,1])
        with col1:
st.markdown("""st.write(f"📌 **{row['Việc']}** lúc {row['Giờ']} ngày {row['Ngày']} → {row['Email']}")""", unsafe_allow_html=True)
        with col2:
            if st.button("❌", key=f"xoa_{idx}"):
                df.drop(index=idx, inplace=True)
                df.to_csv(REMINDERS_FILE, index=False)
                st.experimental_rerun()