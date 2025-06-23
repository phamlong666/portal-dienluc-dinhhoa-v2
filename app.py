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
    total_input = df["Điện nhận đầu nguồn"].sum()
    total_loss = df["Tổn thất (KWh)"].sum()
    actual = (total_loss / total_input * 100) if total_input else 0.0
    plan_col = [col for col in df.columns if "kế hoạch" in col.lower()]
    if plan_col:
        plan = df[plan_col[0]].mean()
    else:
        plan = 0.0
    return round(actual, 2), round(plan, 2)

for label, file in st.session_state.uploaded_data.items():
    if file:
        df = read_mapping_sheet(file)
        st.markdown(f"<h3 style='font-size:22px; color:blue;'>📂 Dữ liệu tổn thất - {label}</h3>", unsafe_allow_html=True)
        with st.expander(f"🧾 Mở rộng/Thu gọn bảng {label}"):
            st.dataframe(df, use_container_width=True, height=350)

        actual, plan = calc_overall_rate(df)

        # Vẽ biểu đồ
        st.markdown(f"<h4 style='font-size:18px;'>📉 Biểu đồ tổn thất - {label}</h4>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4,2))
        bars = ax.bar(["Thực hiện", "Kế hoạch"], [actual, plan], color=["#1976D2", "#FFC107"])
        ax.set_ylim(0, max(actual, plan) * 1.5 + 1)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 0.2, f"{height:.2f}%", ha='center', fontsize=8)
        st.pyplot(fig)

# ====== Gộp và so sánh (khi có nhiều file) ======
if all(st.session_state.uploaded_data.values()):
    st.markdown("<h3 style='font-size:22px;'>📊 So sánh tổn thất giữa các loại dữ liệu</h3>", unsafe_allow_html=True)
    combined_df = pd.DataFrame()
    for label, file in st.session_state.uploaded_data.items():
        df = read_mapping_sheet(file)
        if df is not None:
            df["Loại"] = label
            combined_df = pd.concat([combined_df, df], ignore_index=True)

    with st.expander("📋 Xem bảng tổng hợp so sánh"):
        st.dataframe(combined_df, use_container_width=True, height=400)

    # Xuất báo cáo Word/PDF/PowerPoint (chờ bước 2)
    # ... (sẽ bổ sung nếu anh Long yêu cầu cụ thể từng định dạng sau)

# ====== Gợi ý tiếp theo ======
st.markdown("""
---
📌 **Gợi ý:** Anh có thể yêu cầu xuất báo cáo giống hình ảnh mẫu, tạo file PDF/PPT, hoặc chia nhỏ các tổn thất theo ngưỡng.
""")
