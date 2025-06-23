
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
from docx import Document
from docx.shared import Inches
from pptx import Presentation
from pptx.util import Inches as PptInches, Pt

st.set_page_config(page_title="Báo cáo tổn thất TBA", layout="wide")
st.title("📊 Báo cáo tổn thất các TBA công cộng")  # đã cắt bỏ nút phân tích tổng thể

def read_mapping_sheet(uploaded_file):
    try:
        xls = pd.ExcelFile(uploaded_file)
        sheet_name = [s for s in xls.sheet_names if "ánh xạ" in s.lower()][0]
        df = pd.read_excel(xls, sheet_name=sheet_name)
        return df
    except Exception as e:
        st.warning(f"Lỗi khi đọc file {uploaded_file.name}: {e}")
        return None

def format_percent_cols(df):
    percent_cols = [col for col in df.columns if "%" in col]
    for col in percent_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].map(lambda x: f"{x:.2f}%" if pd.notna(x) else "")
    return df

def calc_overall_rate(df):
    try:
        total_input = df["Điện nhận (kWh)"].sum()
        total_loss = df["Điện tổn thất (kWh)"].sum()
        actual_rate = (total_loss / total_input * 100) if total_input else 0.0
        plan_col = [col for col in df.columns if "kế hoạch" in col.lower()][0]
        plan_series = df[plan_col]
        plan_rate = (
            ((plan_series / 100) * df["Điện nhận (kWh)"]).sum() / total_input * 100
            if total_input
            else 0.0
        )
        return round(actual_rate, 2), round(plan_rate, 2)
    except:
        return 0.0, 0.0

def export_powerpoint(title, actual, plan):
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    shapes = slide.shapes
    title_shape = shapes.title
    title_shape.text = title

    txBox = shapes.add_textbox(PptInches(1), PptInches(1.5), PptInches(8), PptInches(5))
    tf = txBox.text_frame
    tf.text = f"Tỷ lệ tổn thất thực tế: {actual:.2f}%"
    p = tf.add_paragraph()
    p.text = f"Tỷ lệ tổn thất kế hoạch: {plan:.2f}%"
    return prs

# Cấu hình giao diện tải file
col_uploads = st.columns(3)
file_keys = ["Theo Tháng", "Lũy kế", "Cùng kỳ"]
uploaded_files = {}

for i, key in enumerate(file_keys):
    with col_uploads[i]:
        file = st.file_uploader(f"📁 File {key}", type=["xlsx"], key=f"tba_{key}")
        if file:
            st.session_state[f"df_{key}"] = read_mapping_sheet(file)

# Hiển thị bảng, biểu đồ và tạo báo cáo cho từng loại file
for key in file_keys:
    if f"df_{key}" in st.session_state:
        df = st.session_state[f"df_{key}"]
        df = format_percent_cols(df)
        st.markdown(f"### 📄 Bảng dữ liệu: {key}")
        st.dataframe(df.style.set_properties(**{'font-size': '18pt'}), use_container_width=True)

        actual, plan = calc_overall_rate(df)
        st.markdown(f"#### 📊 Biểu đồ tổn thất - {key}")
        fig, ax = plt.subplots(figsize=(3.5, 2))
        x = np.arange(2)
        ax.bar(x, [actual, plan], width=0.4, tick_label=["Thực tế", "Kế hoạch"], color=["#2E86C1", "#F4D03F"])
        for i, v in enumerate([actual, plan]):
            ax.text(i, v + 0.2, f"{v:.2f}%", ha="center", fontsize=10)
        ax.set_ylim(0, max(actual, plan) * 1.4 if max(actual, plan) > 0 else 5)
        st.pyplot(fig)

        # Xuất Word
        doc = Document()
        doc.add_heading(f"Báo cáo tổn thất TBA - {key}", 0)
        doc.add_paragraph(f"Tỷ lệ tổn thất thực tế: {actual:.2f}%")
        doc.add_paragraph(f"Tỷ lệ tổn thất kế hoạch: {plan:.2f}%")
        img_stream = io.BytesIO()
        fig.savefig(img_stream, format="png")
        img_stream.seek(0)
        doc.add_picture(img_stream, width=Inches(4))
        doc_bytes = io.BytesIO()
        doc.save(doc_bytes)
        st.download_button(f"⬇️ Tải báo cáo Word ({key})", doc_bytes.getvalue(), f"BaoCao_{key}.docx")

        # Xuất PowerPoint
        ppt = export_powerpoint(f"Báo cáo tổn thất TBA - {key}", actual, plan)
        ppt_bytes = io.BytesIO()
        ppt.save(ppt_bytes)
        st.download_button(f"⬇️ Tải báo cáo PowerPoint ({key})", ppt_bytes.getvalue(), f"BaoCao_{key}.pptx")

# Tổng hợp biểu đồ 3 file nếu đầy đủ
if all(f"df_{k}" in st.session_state for k in file_keys):
    st.markdown("### 📊 Biểu đồ hợp nhất tổn thất các file")
    data_total = []
    for key in file_keys:
        df = st.session_state[f"df_{key}"]
        act, plan = calc_overall_rate(df)
        data_total.append((key, act, plan))
    fig2, ax2 = plt.subplots(figsize=(5, 3))
    x = np.arange(len(file_keys))
    actuals = [d[1] for d in data_total]
    plans = [d[2] for d in data_total]
    ax2.bar(x - 0.2, actuals, width=0.4, label="Thực tế", color="#3498DB")
    ax2.bar(x + 0.2, plans, width=0.4, label="Kế hoạch", color="#F1C40F")
    ax2.set_xticks(x)
    ax2.set_xticklabels(file_keys)
    ax2.legend()
    for i, (a, p) in enumerate(zip(actuals, plans)):
        ax2.text(i - 0.2, a + 0.1, f"{a:.2f}%", ha="center", fontsize=8)
        ax2.text(i + 0.2, p + 0.1, f"{p:.2f}%", ha="center", fontsize=8)
    st.pyplot(fig2)
