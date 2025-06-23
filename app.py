from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
from docx import Document
from docx.shared import Inches
from fpdf import FPDF
from pptx import Presentation
from pptx.util import Inches as PPTInches

st.set_page_config(page_title="Báo cáo tổn thất TBA", layout="wide")
st.title("📊 Báo cáo tổn thất các TBA công cộng")

# ====== Session State Duy Trì Dữ Liệu ======
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = {
        "Theo Tháng": None,
        "Lũy kế": None,
        "Cùng kỳ": None
    }

# ====== Hàm đọc và xử lý file ánh xạ ======
def read_mapping_sheet(uploaded_file):
    try:
        xls = pd.ExcelFile(uploaded_file)
        sheet_name = [s for s in xls.sheet_names if "ánh xạ" in s.lower()][0]
        df = pd.read_excel(xls, sheet_name=sheet_name)

        percent_cols = [col for col in df.columns if "%" in col or "tỷ lệ" in col.lower()]
        for col in percent_cols:
            df[col] = pd.to_numeric(
                df[col].astype(str)
                .str.replace("%", "", regex=False)
                .str.replace(",", ".", regex=False)
                .replace("", np.nan), errors="coerce"
            )

        float_cols = df.select_dtypes(include=[np.number]).columns
        df[float_cols] = df[float_cols].apply(lambda x: np.round(x, 2))
        return df
    except Exception as e:
        st.warning(f"Lỗi đọc file {uploaded_file.name}: {e}")
        return None

# ====== Giao diện tải file ======
col1, col2, col3 = st.columns(3)
with col1:
    file_thang = st.file_uploader("📅 Tải File Theo Tháng", type="xlsx")
    if file_thang: st.session_state.uploaded_data["Theo Tháng"] = file_thang
with col2:
    file_luyke = st.file_uploader("📊 Tải File Lũy Kế", type="xlsx")
    if file_luyke: st.session_state.uploaded_data["Lũy kế"] = file_luyke
with col3:
    file_cungky = st.file_uploader("📈 Tải File Cùng Kỳ", type="xlsx")
    if file_cungky: st.session_state.uploaded_data["Cùng kỳ"] = file_cungky

# ====== Nút làm mới dữ liệu ======
if st.button("🔄 Làm mới (Xóa dữ liệu đã tải)"):
    st.session_state.uploaded_data = {"Theo Tháng": None, "Lũy kế": None, "Cùng kỳ": None}
    st.experimental_rerun()

# ====== Xử lý và hiển thị từng bảng ======
def calc_overall_rate(df):
    total_input = df.get("Điện nhận đầu nguồn")
    total_loss = df.get("Tổn thất (KWh)")
    if total_input is None or total_loss is None:
        return 0.0, 0.0
    actual = (total_loss.sum() / total_input.sum() * 100) if total_input.sum() else 0.0
    plan_col = [col for col in df.columns if "kế hoạch" in col.lower()]
    plan = df[plan_col[0]].mean() if plan_col else 0.0
    return round(actual, 2), round(plan, 2)

chart_data = {}
for label, file in st.session_state.uploaded_data.items():
    if file:
        df = read_mapping_sheet(file)
        st.markdown(f"<h3 style='font-size:22px; color:blue;'>📂 Dữ liệu tổn thất - {label}</h3>", unsafe_allow_html=True)
        with st.expander(f"🧾 Mở rộng/Thu gọn bảng {label}"):
            st.markdown("<style> .element-container table { font-size: 16px !important; } </style>", unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True, height=350)

        actual, plan = calc_overall_rate(df)
        chart_data[label] = (actual, plan)

        # Vẽ biểu đồ
        st.markdown(f"<h4 style='font-size:18px;'>📉 Biểu đồ tổn thất - {label}</h4>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(2, 1))
        bars = ax.bar(["Thực hiện", "Kế hoạch"], [actual, plan], color=["#1976D2", "#FFC107"])
        ax.set_ylim(0, max(actual, plan) * 1.5 + 1)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 0.2, f"{height:.2f}%", ha='center', fontsize=8)
        st.pyplot(fig)

# ====== Vẽ biểu đồ hợp nhất ======
if chart_data:
    st.markdown("<h3 style='font-size:22px;'>📊 Biểu đồ so sánh tổng hợp</h3>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(3, 2))
    labels = list(chart_data.keys())
    actual_vals = [v[0] for v in chart_data.values()]
    plan_vals = [v[1] for v in chart_data.values()]
    width = 0.35
    x = np.arange(len(labels))
    ax.bar(x - width/2, actual_vals, width, label="Thực hiện", color="#42A5F5")
    ax.bar(x + width/2, plan_vals, width, label="Kế hoạch", color="#FFB300")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    st.pyplot(fig)

# ====== Nút tải báo cáo ======
def export_docx(data):
    doc = Document()
    doc.add_heading("Báo cáo tổn thất TBA", 0)
    for label, (a, p) in data.items():
        doc.add_paragraph(f"{label}: Thực hiện {a}% | Kế hoạch {p}%")
    buf = io.BytesIO()
    doc.save(buf)
    st.download_button("📄 Tải báo cáo Word", buf.getvalue(), file_name="bao_cao_ton_that.docx")

def export_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True)
    pdf.set_font("DejaVu", size=14)
    pdf.cell(200, 10, txt="Báo cáo tổn thất TBA", ln=True, align='C')
    for label, (a, p) in data.items():
        pdf.cell(200, 10, txt=f"{label}: Thực hiện {a}% | Kế hoạch {p}%", ln=True)
    buf = io.BytesIO()
    pdf.output(buf)
    st.download_button("📄 Tải báo cáo PDF", buf.getvalue(), file_name="bao_cao_ton_that.pdf")

def export_pptx(data):
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    title = slide.shapes.title
    title.text = "Báo cáo tổn thất TBA"
    top = PPTInches(1.5)
    for label, (a, p) in data.items():
        body_shape = slide.shapes.add_textbox(PPTInches(1), top, PPTInches(8), PPTInches(0.5))
        tf = body_shape.text_frame
        tf.text = f"{label}: Thực hiện {a}% | Kế hoạch {p}%"
        top += PPTInches(0.5)
    buf = io.BytesIO()
    prs.save(buf)
    st.download_button("📊 Tải báo cáo PowerPoint", buf.getvalue(), file_name="bao_cao_ton_that.pptx")

if chart_data:
    export_docx(chart_data)
    export_pdf(chart_data)
    export_pptx(chart_data)
