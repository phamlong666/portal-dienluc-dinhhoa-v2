# ✅ Cập nhật bản xử lý lỗi KeyError, tăng font chữ bảng, bổ sung biểu đồ nâng cao và nút tải báo cáo

from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
from docx import Document
from docx.shared import Pt

st.set_page_config(page_title="Báo cáo tổn thất TBA", layout="wide")
st.title("📊 Báo cáo tổn thất các TBA công cộng")

# ====== Session State ======
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = {"Theo Tháng": None, "Lũy kế": None, "Cùng kỳ": None}

# ====== Hàm đọc file ánh xạ ======
def read_mapping_sheet(uploaded_file):
    try:
        xls = pd.ExcelFile(uploaded_file)
        sheet_name = [s for s in xls.sheet_names if "ánh xạ" in s.lower()][0]
        df = pd.read_excel(xls, sheet_name=sheet_name)

        df.columns = df.columns.str.strip()
        percent_cols = [col for col in df.columns if "%" in col or "tỷ lệ" in col.lower()]
        for col in percent_cols:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace("%", "", regex=False).str.replace(",", ".", regex=False),
                errors="coerce")

        return df
    except Exception as e:
        st.warning(f"Lỗi đọc file {uploaded_file.name}: {e}")
        return None

# ====== Tải dữ liệu ======
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

# ====== Làm mới dữ liệu ======
if st.button("🔄 Làm mới dữ liệu"):
    st.session_state.uploaded_data = {"Theo Tháng": None, "Lũy kế": None, "Cùng kỳ": None}
    st.experimental_rerun()

# ====== Hàm tính toán tỉ lệ tổn thất ======
def calc_overall_rate(df):
    col_dien_nhan = [col for col in df.columns if "điện nhận" in col.lower()][0]
    col_ton_that = [col for col in df.columns if "tổn thất" in col.lower() and "kwh" in col.lower()][0]
    total_input = df[col_dien_nhan].sum()
    total_loss = df[col_ton_that].sum()
    actual = (total_loss / total_input * 100) if total_input else 0.0
    col_kh = [col for col in df.columns if "kế hoạch" in col.lower()]
    plan = df[col_kh[0]].mean() if col_kh else 0.0
    return round(actual, 2), round(plan, 2)

# ====== Hiển thị dữ liệu và biểu đồ ======
for label, file in st.session_state.uploaded_data.items():
    if file:
        df = read_mapping_sheet(file)
        st.markdown(f"<h3 style='font-size:26px;'>📂 Dữ liệu tổn thất - {label}</h3>", unsafe_allow_html=True)
        with st.expander(f"📋 Mở rộng bảng - {label}", expanded=True):
            st.dataframe(df.style.set_table_styles([
                {'selector': 'th', 'props': [('font-size', '18px')]},
                {'selector': 'td', 'props': [('font-size', '16px')]},
            ]), height=300, use_container_width=True)

        actual, plan = calc_overall_rate(df)
        fig, ax = plt.subplots(figsize=(2, 1.2))
        bars = ax.bar(["Thực hiện", "Kế hoạch"], [actual, plan], color=["#1976D2", "#FFC107"])
        ax.set_ylim(0, max(actual, plan) * 1.5 + 1)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 0.1, f"{height:.2f}%", ha='center', fontsize=8)
        st.pyplot(fig)

# ====== Tổng hợp và Tải báo cáo ======
if any(st.session_state.uploaded_data.values()):
    combined_df = pd.DataFrame()
    for label, file in st.session_state.uploaded_data.items():
        if file:
            df = read_mapping_sheet(file)
            df["Loại"] = label
            combined_df = pd.concat([combined_df, df], ignore_index=True)

    st.markdown("<h3 style='font-size:26px;'>📊 So sánh tổn thất tổng hợp</h3>", unsafe_allow_html=True)
    st.dataframe(combined_df, height=350, use_container_width=True)

    # ====== Nút tải báo cáo Word ======
    if st.button("📥 Tải báo cáo Word"):
        doc = Document()
        doc.add_heading("Báo cáo tổn thất TBA công cộng", level=1)
        t = doc.add_table(rows=1, cols=len(combined_df.columns))
        hdr_cells = t.rows[0].cells
        for i, col in enumerate(combined_df.columns):
            hdr_cells[i].text = str(col)
        for _, row in combined_df.iterrows():
            row_cells = t.add_row().cells
            for i, val in enumerate(row):
                row_cells[i].text = str(val)
        buffer = io.BytesIO()
        doc.save(buffer)
        st.download_button("📄 Tải báo cáo Word", buffer.getvalue(), file_name="bao_cao_ton_that.docx")
