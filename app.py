from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
from docx import Document
from docx.shared import Inches

st.set_page_config(page_title="Báo cáo tổn thất TBA", layout="wide")
st.title("📊 Báo cáo tổn thất các TBA công cộng")

# ==== Hàm xử lý dữ liệu ====
def read_mapping_sheet(uploaded_file):
    try:
        xls = pd.ExcelFile(uploaded_file)
        sheet_name = [s for s in xls.sheet_names if "ánh xạ" in s.lower()][0]
        df = pd.read_excel(xls, sheet_name=sheet_name)

        for col in df.columns:
            if df[col].dtype in [np.float64, np.int64]:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        percent_cols = [col for col in df.columns if "%" in col]
        for col in percent_cols:
            df[col] = pd.to_numeric(
                df[col].astype(str)
                .str.replace("%", "", regex=False)
                .str.replace(",", ".", regex=False)
                .replace("", np.nan),
                errors="coerce",
            )
        return df
    except Exception as e:
        st.warning(f"Lỗi khi đọc file {uploaded_file.name}: {e}")
        return None


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

# ==== Giao diện tải file ====
col_uploads = st.columns(3)
with col_uploads[0]:
    file_thang = st.file_uploader("📅 File Theo Tháng", type=["xlsx"], key="tba_thang")
with col_uploads[1]:
    file_luyke = st.file_uploader("📊 File Lũy kế", type=["xlsx"], key="tba_luyke")
with col_uploads[2]:
    file_cungky = st.file_uploader("📈 File Cùng kỳ", type=["xlsx"], key="tba_ck")

uploaded_files = {
    "Theo Tháng": file_thang,
    "Lũy kế": file_luyke,
    "Cùng kỳ": file_cungky,
}

# ==== Ghép phân tích nhiều file vào bảng chung ====
combined_df = []
result_summary = []

for label, file in uploaded_files.items():
    if file:
        df = read_mapping_sheet(file)
        if df is not None:
            df["Nguồn dữ liệu"] = label
            combined_df.append(df)
            act, plan = calc_overall_rate(df)
            result_summary.append({"Loại dữ liệu": label, "Tổn thất thực tế (%)": act, "Tổn thất kế hoạch (%)": plan})

if combined_df:
    st.markdown("<h3 style='font-size:20px;'>📄 Bảng dữ liệu tổng hợp</h3>", unsafe_allow_html=True)
    final_df = pd.concat(combined_df, ignore_index=True)
    st.markdown("<style>div[data-testid='stDataFrame'] table {font-size: 16px;}</style>", unsafe_allow_html=True)
    st.dataframe(final_df, use_container_width=True)

    df_chart = pd.DataFrame(result_summary)
    st.markdown("#### 📉 So sánh tổn thất giữa các loại dữ liệu")
    fig, ax = plt.subplots(figsize=(5, 2.5))
    x = np.arange(len(df_chart))
    width = 0.35
    ax.bar(x - width/2, df_chart["Tổn thất thực tế (%)"], width, label="Thực tế")
    ax.bar(x + width/2, df_chart["Tổn thất kế hoạch (%)"], width, label="Kế hoạch")
    ax.set_xticks(x)
    ax.set_xticklabels(df_chart["Loại dữ liệu"])
    ax.legend()
    for i in range(len(df_chart)):
        ax.text(x[i] - width/2, df_chart["Tổn thất thực tế (%)"][i] + 0.2, f"{df_chart["Tổn thất thực tế (%)"][i]:.2f}%", ha="center", fontsize=7)
        ax.text(x[i] + width/2, df_chart["Tổn thất kế hoạch (%)"][i] + 0.2, f"{df_chart["Tổn thất kế hoạch (%)"][i]:.2f}%", ha="center", fontsize=7)
    ax.set_ylim(0, max(df_chart[["Tổn thất thực tế (%)", "Tổn thất kế hoạch (%)"]].max()) * 1.4)
    st.pyplot(fig)
else:
    st.info("Vui lòng tải lên ít nhất một file dữ liệu để phân tích.")
