
# ================== CỔNG TRUNG TÂM ĐIỀU HÀNH SỐ - ĐIỆN LỰC ĐỊNH HÓA ==================
import streamlit as st
import pandas as pd
from datetime import datetime, time
import os
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="Trung tâm điều hành số - Điện lực Định Hóa", layout="wide")
st.title("🧠 Trung tâm điều hành số - Điện lực Định Hóa")

# ================== NÚT CHỨC NĂNG ==================
col1, col2 = st.columns(2)
with col1:
    if st.button("📑 Phục vụ họp"):
        st.subheader("📋 Nhập thông tin cuộc họp")
        with st.form("form_hop", clear_on_submit=True):
            ten = st.text_input("Tên cuộc họp")
            ngay = st.date_input("📅 Ngày họp", format="DD/MM/YYYY")
            gio = st.time_input("⏰ Giờ họp", time(8, 0))
            noi_dung = st.text_area("📝 Nội dung cuộc họp")
            files = st.file_uploader("📎 Tải file đính kèm", accept_multiple_files=True)

            submit = st.form_submit_button("💾 Lưu và tạo báo cáo")
            if submit:
                new_row = {
                    "Tên cuộc họp": ten,
                    "Ngày": ngay.strftime("%d/%m/%Y"),
                    "Giờ": gio.strftime("%H:%M"),
                    "Nội dung": noi_dung
                }
                df = pd.DataFrame([new_row])
                if os.path.exists("lich_su_cuoc_hop.csv"):
                    old = pd.read_csv("lich_su_cuoc_hop.csv")
                    df = pd.concat([old, df], ignore_index=True)
                df.to_csv("lich_su_cuoc_hop.csv", index=False)

                if files:
                    Path("uploaded_files").mkdir(exist_ok=True)
                    for f in files:
                        with open(f"uploaded_files/{f.name}", "wb") as out:
                            out.write(f.read())

                st.success("✅ Lịch sử cuộc họp đã được lưu")

                # Xuất file PDF đơn giản
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, f"Cuộc họp: {ten}
Ngày: {ngay.strftime('%d/%m/%Y')} {gio.strftime('%H:%M')}

Nội dung:
{noi_dung}")
                pdf_output = BytesIO()
                pdf.output(pdf_output)
                st.download_button("📄 Tải báo cáo PDF", data=pdf_output.getvalue(), file_name=f"{ten}.pdf")

with col2:
    if st.button("⏰ Nhắc việc"):
        with st.form("nhacviec", clear_on_submit=True):
            viec = st.text_input("Tên công việc")
            thoi_diem = st.date_input("📆 Ngày nhắc", format="DD/MM/YYYY")
            gio_nhac = st.time_input("⏰ Giờ nhắc", time(7, 0))
            submit_nhac = st.form_submit_button("🔔 Tạo nhắc việc")
            if submit_nhac:
                st.success(f"✅ Đã tạo nhắc việc: {viec} lúc {gio_nhac.strftime('%H:%M')} ngày {thoi_diem.strftime('%d/%m/%Y')}")

# ================== XEM LỊCH SỬ ==================
if os.path.exists("lich_su_cuoc_hop.csv"):
    st.subheader("📚 Lịch sử cuộc họp")
    df = pd.read_csv("lich_su_cuoc_hop.csv")
    for idx, row in df.iterrows():
        with st.expander(f"📅 {row['Ngày']} {row['Giờ']} – {row['Tên cuộc họp']}"):
            st.write(row["Nội dung"])
            folder = Path("uploaded_files")
            if folder.exists():
                files = list(folder.glob("*"))
                for f in files:
                    if f.name.startswith(row['Tên cuộc họp']):
                        if f.suffix in [".png", ".jpg", ".jpeg"]:
                            st.image(str(f), width=300)
                        else:
                            st.download_button(f"Tải xuống {f.name}", f.read_bytes(), file_name=f.name)

    if st.button("🗑️ Xóa toàn bộ lịch sử"):
        os.remove("lich_su_cuoc_hop.csv")
        st.experimental_rerun()
