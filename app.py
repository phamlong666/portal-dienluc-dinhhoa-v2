# ================== STREAMLIT SETUP ==================
from pathlib import Path
import streamlit as st
st.set_page_config(page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa", layout="wide")

# ================== IMPORT THƯ VIỆN ==================
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from fpdf import FPDF
import base64

# ================== HÀM VẼ BIỂU ĐỒ ==================
def draw_combined_chart(data):
    fig, ax = plt.subplots(figsize=(6, 4))
    bar_width = 0.35
    x = range(len(data))

    actuals = [d['actual'] for d in data]
    plans = [d['plan'] for d in data]
    labels = [d['label'] for d in data]

    ax.bar(x, actuals, width=bar_width, label='Thực hiện', color='orange')
    ax.bar([p + bar_width for p in x], plans, width=bar_width, label='Kế hoạch', color='green')

    ax.set_xticks([p + bar_width / 2 for p in x])
    ax.set_xticklabels(labels, fontsize=11)
    ax.legend(fontsize=10)
    plt.tight_layout()
    return fig

# ================== HÀM XUẤT PDF ==================
def export_pdf(chart_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="BÁO CÁO PHÂN TÍCH TỔN THẤT", ln=True, align="C")

    for i, fig in enumerate(chart_data):
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=150, bbox_inches='tight')
        buf.seek(0)
        img_path = f"chart_{i}.png"
        with open(img_path, "wb") as f:
            f.write(buf.getbuffer())
        pdf.image(img_path, x=10, w=pdf.w * 0.7)
        buf.close()

    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    b64 = base64.b64encode(pdf_buffer.read()).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="bao_cao_ton_that.pdf">📄 Tải báo cáo PDF</a>'
    st.markdown(href, unsafe_allow_html=True)

# ================== GIAO DIỆN STREAMLIT ==================
st.title("📊 Biểu đồ tổn thất - Điện lực Định Hóa")

sample_data = [
    {"label": "Theo Tháng", "actual": 0.0312, "plan": 0.0712},
    {"label": "Lũy kế", "actual": 0.0389, "plan": 0.0712},
    {"label": "Cùng kỳ", "actual": 0.0444, "plan": 0.0712},
]

st.subheader("🔎 So sánh tỷ lệ tổn thất")
fig1 = draw_combined_chart(sample_data)
st.pyplot(fig1)

# ================== XUẤT PDF ==================
if st.button("📤 Tải báo cáo PDF"):
    export_pdf([fig1])
