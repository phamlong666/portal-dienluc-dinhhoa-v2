
import streamlit as st
import pandas as pd
import os
import datetime
from io import BytesIO
from docx import Document
from fpdf import FPDF
from PIL import Image

st.set_page_config(page_title="Trung tâm điều hành số - Phục vụ họp", layout="wide")

# CSV chứa lịch sử họp
CSV_FILE = "lich_su_cuoc_hop.csv"

def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=["Ngày", "Giờ", "Tên cuộc họp", "Nội dung", "Tệp"])

def save_data(row):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

def create_word_report(row):
    doc = Document()
    doc.add_heading("Biên bản cuộc họp", 0)
    doc.add_paragraph(f"Ngày: {row['Ngày']} {row['Giờ']}")
    doc.add_paragraph(f"Tên cuộc họp: {row['Tên cuộc họp']}")
    doc.add_paragraph("Nội dung cuộc họp:")
    doc.add_paragraph(row['Nội dung'])
    file_stream = BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return file_stream

def create_pdf_report(row):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Biên bản cuộc họp\n\nNgày: {row['Ngày']} {row['Giờ']}\nTên cuộc họp: {row['Tên cuộc họp']}\n\nNội dung:\n{row['Nội dung']}")
    file_stream = BytesIO()
    pdf.output(file_stream)
    file_stream.seek(0)
    return file_stream

# Giao diện nhập thông tin cuộc họp
with st.form("phuc_vu_hop_form"):
    st.subheader("📑 Phục vụ họp")
    ten = st.text_input("Tên cuộc họp")
    ngay = st.date_input("Ngày họp", format="DD/MM/YYYY")
    gio = st.time_input("Giờ họp")
    noi_dung = st.text_area("Nội dung cuộc họp")
    tep = st.file_uploader("📎 Tải file đính kèm", accept_multiple_files=True)
    submit = st.form_submit_button("💾 Lưu nội dung họp")

if submit:
    ten_file = ";".join([f.name for f in tep]) if tep else ""
    new_row = {
        "Ngày": ngay.strftime("%d/%m/%Y"),
        "Giờ": str(gio),
        "Tên cuộc họp": ten,
        "Nội dung": noi_dung,
        "Tệp": ten_file
    }
    save_data(new_row)
    for f in tep:
        with open(f"upload_{f.name}", "wb") as out_file:
            out_file.write(f.read())
    st.success("✅ Lịch sử cuộc họp đã được lưu")

# Hiển thị lịch sử cuộc họp
df = load_data()
if not df.empty:
    st.subheader("📚 Lịch sử cuộc họp")
    for i, row in df.iterrows():
        with st.expander(f"📅 {row['Ngày']} {row['Giờ']} – {row['Tên cuộc họp']}"):
            st.markdown(row["Nội dung"])
            if row["Tệp"]:
                files = row["Tệp"].split(";")
                for file_name in files:
                    file_path = f"upload_{file_name}"
                    if os.path.exists(file_path):
                        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                            st.image(file_path, width=300)
                        else:
                            st.write(f"📎 {file_name}")
                            with open(file_path, "rb") as f:
                                st.download_button("📥 Tải xuống", f.read(), file_name=file_name)

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📝 Xuất Word", key=f"word_{i}"):
                    file = create_word_report(row)
                    st.download_button("📥 Tải file Word", file, file_name="bao_cao_cuoc_hop.docx")
            with col2:
                if st.button("📝 Xuất PDF", key=f"pdf_{i}"):
                    file = create_pdf_report(row)
                    st.download_button("📥 Tải file PDF", file, file_name="bao_cao_cuoc_hop.pdf")
            with col3:
                if st.button("❌ Xóa cuộc họp", key=f"xoa_{i}"):
                    df = df.drop(index=i)
                    df.to_csv(CSV_FILE, index=False)
                    st.experimental_rerun()
