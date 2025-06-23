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
from pptx.util import Inches as PPTInches, Pt

st.set_page_config(page_title="Báo cáo tổn thất TBA", layout="wide")
st.title("📊 Báo cáo tổn thất các TBA công cộng")

# ====== Session State ======
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = {"Theo Tháng": None, "Lũy kế": None, "Cùng kỳ": None}

# ====== Hàm đọc và xử lý file ánh xạ ======
def read_mapping_sheet(uploaded_file):
    try:
        xls = pd.ExcelFile(uploaded_file)
        sheet_name = [s for s in xls.sheet_names if "ánh xạ" in s.lower()][0]
        df = pd.read_excel(xls, sheet_name=sheet_name)

        percent_cols = [col for col in df.columns if "%" in col or "tỷ lệ" in col.lower()]
        for col in percent_cols:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace("%", "", regex=False)
                                     .str.replace(",", ".", regex=False)
                                     .replace("", np.nan), errors="coerce")

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

if st.button("🔄 Làm mới"):
    st.session_state.uploaded_data = {"Theo Tháng": None, "Lũy kế": None, "Cùng kỳ": None}
    st.experimental_rerun()

# ====== Hàm tính toán ======
def calc_overall_rate(df):
    input_col = [c for c in df.columns if "điện nhận" in c.lower()]
    loss_col = [c for c in df.columns if "tổn thất" in c.lower() and "kwh" in c.lower()]
    plan_col = [c for c in df.columns if "kế hoạch" in c.lower()]
    if not input_col or not loss_col:
        return 0.0, 0.0
    total_input = df[input_col[0]].sum()
    total_loss = df[loss_col[0]].sum()
    actual = (total_loss / total_input * 100) if total_input else 0.0
    plan = df[plan_col[0]].mean() if plan_col else 0.0
    return round(actual, 2), round(plan, 2)

# ====== Hiển thị dữ liệu ======
chart_data = {}
for label, file in st.session_state.uploaded_data.items():
    if file:
        df = read_mapping_sheet(file)
        st.markdown(f"<h3 style='font-size:22px; color:blue;'>📂 Dữ liệu tổn thất - {label}</h3>", unsafe_allow_html=True)
        st.dataframe(df.style.set_properties(**{'font-size': '16px'}), use_container_width=True, height=350)

        actual, plan = calc_overall_rate(df)
        chart_data[label] = (actual, plan)

        st.markdown(f"<h4 style='font-size:18px;'>📉 Biểu đồ tổn thất - {label}</h4>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(2, 1))
        bars = ax.bar(["Thực hiện", "Kế hoạch"], [actual, plan], color=["#1976D2", "#FFC107"])
        ax.set_ylim(0, max(actual, plan) * 1.5 + 1)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 0.1, f"{height:.2f}%", ha='center', fontsize=6)
        st.pyplot(fig)

# ====== Biểu đồ tổng hợp so sánh ======
if chart_data:
    st.markdown("<h3 style='font-size:20px;'>📊 Biểu đồ so sánh tổng hợp</h3>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(3, 2))
    labels = list(chart_data.keys())
    actuals = [v[0] for v in chart_data.values()]
    plans = [v[1] for v in chart_data.values()]
    width = 0.35
    x = np.arange(len(labels))
    ax.bar(x - width/2, actuals, width, label='Thực hiện')
    ax.bar(x + width/2, plans, width, label='Kế hoạch')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    st.pyplot(fig)

# ====== Xuất báo cáo ======
def export_docx(data):
    doc = Document()
    doc.add_heading("Báo cáo tổn thất TBA", 0)
    for label, (actual, plan) in data.items():
        doc.add_heading(f"{label}", level=1)
        doc.add_paragraph(f"Tỷ lệ tổn thất thực hiện: {actual}%")
        doc.add_paragraph(f"Tỷ lệ tổn thất kế hoạch: {plan}%")
    buf = io.BytesIO()
    doc.save(buf)
    st.download_button("📄 Tải báo cáo Word", data=buf.getvalue(), file_name="bao_cao_ton_that.docx")

def export_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Báo cáo tổn thất TBA", ln=1, align='C')
    for label, (actual, plan) in data.items():
        pdf.cell(200, 10, txt=f"{label}: Thực hiện {actual}%, Kế hoạch {plan}%", ln=1)
    buf = io.BytesIO()
    pdf.output(buf)
    st.download_button("📄 Tải báo cáo PDF", data=buf.getvalue(), file_name="bao_cao_ton_that.pdf")

def export_pptx(data):
    ppt = Presentation()
    slide_layout = ppt.slide_layouts[1]
    slide = ppt.slides.add_slide(slide_layout)
    slide.shapes.title.text = "Báo cáo tổn thất TBA"
    content = ""
    for label, (actual, plan) in data.items():
        content += f"{label}: Thực hiện {actual}%, Kế hoạch {plan}%\n"
    slide.placeholders[1].text = content
    buf = io.BytesIO()
    ppt.save(buf)
    st.download_button("📊 Tải báo cáo PowerPoint", data=buf.getvalue(), file_name="bao_cao_ton_that.pptx")

if chart_data:
    export_docx(chart_data)
    export_pdf(chart_data)
    export_pptx(chart_data)

# ====== Gợi ý tiếp ======
st.markdown("""
---
📌 **Gợi ý:** Có thể thêm phân tích theo ngưỡng tổn thất hoặc xuất bảng chi tiết từng TBA theo yêu cầu.
""")
