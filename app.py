
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Báo cáo tổn thất TBA", layout="wide")
st.title("📥 Tải dữ liệu đầu vào - Báo cáo tổn thất")

st.markdown("### 🔍 Chọn loại dữ liệu tổn thất để tải lên:")

with st.expander("🔌 Tổn thất các TBA công cộng"):
    upload_tba_thang = st.file_uploader("📅 Tải dữ liệu TBA công cộng - Theo tháng", type=["xlsx"], key="tba_thang")

if upload_tba_thang:
    df_raw = pd.read_excel(upload_tba_thang, skiprows=6)

    # Bỏ các dòng có tên TBA trống hoặc là các dòng tổng hợp
    df_raw = df_raw[df_raw.iloc[:, 2].notna()]
    excluded_keywords = ["Xuất tuyến", "Tổng cộng"]
    df_raw = df_raw[~df_raw.iloc[:, 2].astype(str).str.contains('|'.join(excluded_keywords))]

    # Tạo bảng kết quả ánh xạ
    df_result = pd.DataFrame()
    df_result["STT"] = range(1, len(df_raw) + 1)
    df_result["Tên TBA"] = df_raw.iloc[:, 2]
    df_result["Công suất"] = df_raw.iloc[:, 3]
    df_result["Điện nhận"] = df_raw.iloc[:, 6]
    df_result["Thương phẩm"] = df_raw.iloc[:, 6] - df_raw.iloc[:, 7]
    df_result["Điện tổn thất"] = df_raw.iloc[:, 13].round(0).astype("Int64")
    df_result["Tỷ lệ tổn thất"] = df_raw.iloc[:, 14].map(lambda x: f"{x:.2f}".replace(".", ",") if pd.notna(x) else "")
    df_result["Kế hoạch"] = df_raw.iloc[:, 15].map(lambda x: f"{x:.2f}".replace(".", ",") if pd.notna(x) else "")
    df_result["So sánh"] = df_raw.iloc[:, 16].map(lambda x: f"{x:.2f}".replace(".", ",") if pd.notna(x) else "")

    st.markdown("### 📊 Kết quả ánh xạ dữ liệu:")
    st.dataframe(df_result)

    # Biểu đồ tổn thất
    st.markdown("### 📉 Biểu đồ tổn thất theo TBA")
    df_plot = df_result[["Tên TBA", "Điện tổn thất"]].dropna()
    fig, ax = plt.subplots(figsize=(14, 6))
    bars = ax.bar(df_plot["Tên TBA"], df_plot["Điện tổn thất"])
    ax.set_xlabel("Tên TBA", fontsize=16)
    ax.set_ylabel("Điện tổn thất (kWh)", fontsize=16)
    ax.set_title("Biểu đồ tổn thất các TBA công cộng", fontsize=20)
    ax.tick_params(axis='x', labelrotation=45, labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height, str(int(height)), ha='center', va='bottom', fontsize=10)
    st.pyplot(fig)
