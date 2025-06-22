# File: bao_cao_nhanh.py

import streamlit as st
import pandas as pd
from io import BytesIO
from docx import Document
from docx.shared import Inches
from pptx import Presentation
from pptx.util import Inches
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# ====================== CẤU HÌNH GIAO DIỆN ========================
st.set_page_config(page_title="📑 Báo cáo nhanh", layout="wide")

st.markdown("""
    <style>
        .main .block-container {
            padding-top: 20px;
            padding-bottom: 0px;
        }
        .stButton button {
            border-radius: 12px;
            box-shadow: 1px 1px 5px rgba(0,0,0,0.2);
            transition: 0.2s;
        }
        .stButton button:hover {
            transform: scale(1.02);
            background-color: #0d6efd;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# ====================== KHUNG GIAO DIỆN CHÍNH ========================

with st.expander("📁 Chọn loại báo cáo và mẫu (thu gọn/mở rộng)", expanded=True):
    loai_bao_cao = st.selectbox("Chọn loại báo cáo:", [
        "Tổn thất", "Sự cố", "SXKD", "Công đoàn", "ATVSV", "QLVH"])

    mau_bao_cao = st.selectbox("Chọn mẫu báo cáo:", [
        "Mau_TonThat_1.docx", "Mau_SuCo_ThietBi.docx",
        "Mau_SXKD_Quy1.docx", "Mau_CongDoan.docx",
        "Mau_ATVSV.docx", "Mau_QLVH.pptx"])

with st.expander("📂 Tải dữ liệu đầu vào + ảnh/video minh họa", expanded=True):
    data_file = st.file_uploader("🗂 Tải dữ liệu (Excel/Word)", type=["xlsx", "xls", "csv", "docx"])
    media_files = st.file_uploader("🖼 Tải ảnh/video minh họa", type=["png", "jpg", "jpeg", "mp4"], accept_multiple_files=True)

# ====================== XỬ LÝ TẠO BÁO CÁO ========================
if st.button("🚀 Tạo báo cáo thử nghiệm"):
    if mau_bao_cao.endswith(".docx"):
        doc = Document()
        doc.add_heading("BÁO CÁO NHANH", 0)

        if data_file is not None:
            try:
                df = pd.read_excel(data_file)
                st.success("Đã đọc dữ liệu Excel thành công!")

                # Vẽ biểu đồ 3D cột
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                xs = np.arange(len(df))
                ys = np.zeros(len(df))
                zs = np.zeros(len(df))
                dx = dy = 0.5
                heights = df.iloc[:, 1]
                ax.bar3d(xs, ys, zs, dx, dy, heights, shade=True)
                for i, h in enumerate(heights):
                    ax.text(xs[i], ys[i], h, str(h), ha='center')
                fig_path = "bieu_do_3d.png"
                fig.savefig(fig_path)
                doc.add_paragraph("Biểu đồ minh họa dữ liệu:")
                doc.add_picture(fig_path, width=Inches(5))
            except Exception as e:
                st.error(f"Lỗi xử lý dữ liệu: {e}")

        if media_files:
            doc.add_heading("Hình ảnh minh họa", level=2)
            for mf in media_files:
                if mf.type.startswith("image"):
                    img_stream = BytesIO(mf.read())
                    doc.add_picture(img_stream, width=Inches(4))
                    doc.add_paragraph(f"Ảnh: {mf.name}")
                elif mf.type.startswith("video"):
                    doc.add_paragraph(f"[Video đính kèm: {mf.name}]")

        output_path = "BaoCaoNhanh.docx"
        doc.save(output_path)
        st.success("✅ Đã tạo xong bản báo cáo nháp (.docx)")
        with open(output_path, "rb") as f:
            st.download_button("📥 Tải báo cáo .docx", f, file_name=output_path)

    elif mau_bao_cao.endswith(".pptx"):
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[5])
        title = slide.shapes.title
        title.text = "BÁO CÁO NHANH - DỮ LIỆU MINH HỌA"

        if media_files:
            for mf in media_files:
                if mf.type.startswith("image"):
                    img_stream = BytesIO(mf.read())
                    slide.shapes.add_picture(img_stream, Inches(1), Inches(2), height=Inches(3))
                elif mf.type.startswith("video"):
                    txBox = slide.shapes.add_textbox(Inches(1), Inches(5), Inches(5), Inches(1))
                    txBox.text = f"Video: {mf.name} (không chèn được trong bản demo)"

        output_path = "BaoCaoNhanh.pptx"
        prs.save(output_path)
        st.success("✅ Đã tạo xong bản báo cáo nháp (.pptx)")
        with open(output_path, "rb") as f:
            st.download_button("📥 Tải báo cáo .pptx", f, file_name=output_path)

# ====================== KẾT ========================
st.info("Chức năng đang trong giai đoạn thử nghiệm. Góp ý của anh Long sẽ giúp Mắt Nâu hoàn thiện tốt hơn!")
