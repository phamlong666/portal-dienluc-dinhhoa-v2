
import streamlit as st
import pandas as pd
from PIL import Image
import datetime
from docx import Document
from pptx import Presentation
from io import BytesIO
import csv

st.set_page_config(page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa", layout="wide")

st.markdown("""
    <style>
        section[data-testid="stSidebar"] > div:first-child {
            max-height: 95vh;
            overflow-y: auto;
        }

        .sidebar-button {
            display: block;
            background-color: #66a3ff;
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
            background-color: #3385ff !important;
            transform: translateY(-2px);
            box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
        }

        .main-button {
            display: inline-block;
            background-color: #66a3ff;
            color: white;
            text-align: center;
            padding: 22px 30px;
            border-radius: 14px;
            font-weight: bold;
            text-decoration: none;
            margin: 14px;
            transition: 0.3s;
            font-size: 24px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        }

        .main-button:hover {
            transform: scale(1.07);
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
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
👋 Chào mừng bạn đến với Trung tâm điều hành số - phần mềm Điện lực Định Hóa

📌 **Các tính năng nổi bật:**
- Phân tích tổn thất, báo cáo kỹ thuật
- Lưu trữ và truy xuất lịch sử GPT
- Truy cập hệ thống nhanh chóng qua Sidebar

✅ Mọi bản cập nhật chỉ cần chỉnh sửa Google Sheet đều tự động hiển thị!
""")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="display: flex; justify-content: center; flex-wrap: wrap;">
    <a href="https://terabox.com/s/1cegqu7nP7rd0BdL_MIyrtA" target="_blank" class="main-button">📦 Bigdata_Terabox</a>
    <a href="https://chat.openai.com" target="_blank" class="main-button">💬 ChatGPT công khai</a>
    <a href="https://www.youtube.com/@dienlucdinhhoa" target="_blank" class="main-button">🎬 video tuyên truyền</a>
    <a href="https://www.dropbox.com/home/3.%20Bao%20cao/4.%20B%C3%A1o%20c%C3%A1o%20CMIS" target="_blank" class="main-button">📄 Báo cáo CMIS</a>
</div>
""", unsafe_allow_html=True)

# === TÍNH NĂNG PHỤC VỤ HỌP ===
st.markdown("---")
st.header("📋 Phục vụ họp – Ghi báo cáo và xuất file")

ten = st.text_input("Tên cuộc họp")
ngay = st.date_input("Ngày họp", value=datetime.date.today())
nd = st.text_area("Nội dung cuộc họp", height=300)

col1, col2, col3 = st.columns(3)

def save_to_csv(ten, ngay, nd):
    csv_file = "lich_su_cuoc_hop.csv"
    header = ["ten_cuoc_hop", "ngay_hop", "noi_dung", "ngay_ghi"]
    with open(csv_file, mode="a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=header)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow({
            "ten_cuoc_hop": ten,
            "ngay_hop": ngay.strftime("%d/%m/%Y"),
            "noi_dung": nd,
            "ngay_ghi": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        })
    return csv_file

def tao_word(ten, ngay, nd):
    doc = Document()
    doc.add_heading("BÁO CÁO CUỘC HỌP", 0)
    doc.add_paragraph(f"Tên cuộc họp: {ten}")
    doc.add_paragraph(f"Ngày họp: {ngay.strftime('%d/%m/%Y')}")
    doc.add_paragraph("\nNội dung chính:")
    doc.add_paragraph(nd)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def tao_ppt(ten, ngay, nd):
    prs = Presentation()
    title_slide = prs.slides.add_slide(prs.slide_layouts[0])
    title_slide.shapes.title.text = "BÁO CÁO CUỘC HỌP"
    title_slide.placeholders[1].text = f"{ten}\nNgày họp: {ngay.strftime('%d/%m/%Y')}"
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Nội dung chính"
    slide.placeholders[1].text = nd
    buffer = BytesIO()
    prs.save(buffer)
    buffer.seek(0)
    return buffer

with col1:
    if st.button("📤 Tạo Word"):
        if ten and nd:
            file = tao_word(ten, ngay, nd)
            st.download_button("📥 Tải Word", file, file_name=f"{ten.replace(' ','_')}.docx")
            save_to_csv(ten, ngay, nd)
        else:
            st.warning("❗ Nhập đầy đủ thông tin")

with col2:
    if st.button("📽️ Tạo PowerPoint"):
        if ten and nd:
            file = tao_ppt(ten, ngay, nd)
            st.download_button("📥 Tải PowerPoint", file, file_name=f"{ten.replace(' ','_')}.pptx")
            save_to_csv(ten, ngay, nd)
        else:
            st.warning("❗ Nhập đầy đủ thông tin")

with col3:
    if st.button("📜 Lưu lịch sử"):
        path = save_to_csv(ten, ngay, nd)
        st.success(f"✅ Đã lưu vào {path}")

# Hiển thị lịch sử nếu có
st.markdown("---")
st.subheader("📚 Lịch sử cuộc họp đã lưu")
try:
    with open("lich_su_cuoc_hop.csv", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
        for row in rows[1:]:
            st.markdown(f"**🗓 {row[1]}** – `{row[0]}`  \n{row[2]}")
except:
    st.info("Chưa có cuộc họp nào được lưu.")

