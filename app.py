import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Báo cáo tổn thất TBA", layout="wide")
st.markdown("""
    <style>
    .big-font {
        font-size:24px !important;
    }
    .stButton>button, .stFileUploader label div {
        font-size: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='big-font'>📥 Tải dữ liệu đầu vào - Báo cáo tổn thất</h1>", unsafe_allow_html=True)

st.markdown("### 🔍 Chọn loại dữ liệu tổn thất để tải lên:")

with st.expander("🔌 Tổn thất các TBA công cộng"):
    upload_tba_thang = st.file_uploader("📅 Tải dữ liệu TBA công cộng - Theo tháng", type=["xlsx"], key="tba_thang")
    upload_tba_luyke = st.file_uploader("📊 Tải dữ liệu TBA công cộng - Lũy kế", type=["xlsx"], key="tba_luyke")
    upload_tba_cungkyd = st.file_uploader("📈 Tải dữ liệu TBA công cộng - Cùng kỳ", type=["xlsx"], key="tba_ck")

if upload_tba_thang:
    df_test = pd.read_excel(upload_tba_thang, skiprows=6)
    bo_qua = [
        "Xuat tuyen PA04DAF1223701",
        "Xuat tuyen PA04DAF1224701",
        "Xuat tuyen PA04DAF1224702",
        "Xuat tuyen PA04DAF1224703",
        "Tổng cộng"
    ]

    df_test = df_test[df_test.iloc[:, 2].notna()]
    df_test["Tên"] = df_test.iloc[:, 2].astype(str).str.strip()
    df_test = df_test[~df_test["Tên"].str.contains("Xuat tuyen|Tổng cộng", case=False, na=False)]

    df_result = pd.DataFrame()
    df_result["Tên TBA"] = df_test["Tên"]
    df_result["Công suất"] = df_test.iloc[:, 3]
    df_result["Điện nhận"] = df_test.iloc[:, 6]
    df_result["Thương phẩm"] = df_test.iloc[:, 6] - df_test.iloc[:, 7]
    df_result["Điện tổn thất"] = df_test.iloc[:, 13].round(0).astype("Int64")
    df_result["Tỷ lệ tổn thất"] = pd.to_numeric(df_test.iloc[:, 14], errors='coerce') / 100
    df_result["Kế hoạch"] = pd.to_numeric(df_test.iloc[:, 15], errors='coerce') / 100
    df_result["So sánh"] = pd.to_numeric(df_test.iloc[:, 16], errors='coerce') / 100
    df_result.reset_index(drop=True, inplace=True)
    df_result.insert(0, "STT", range(1, len(df_result) + 1))

    with st.expander("📊 Kết quả ánh xạ dữ liệu (click để mở/thu gọn)", expanded=True):
        st.dataframe(df_result.style.format({"Tỷ lệ tổn thất": "{:.2%}", "Kế hoạch": "{:.2%}", "So sánh": "{:.2%}"}))

    st.markdown("### 📉 Biểu đồ tổn thất theo TBA")
    fig, ax = plt.subplots(figsize=(14, 2))
    try:
        tba_names = df_result["Tên TBA"].astype(str)
        ton_that = df_result["Điện tổn thất"].astype(float) / 1000
        ax.bar(tba_names, ton_that)
        ax.set_xlabel("Tên TBA", fontsize=12)
        ax.set_ylabel("Tổn thất (x1000 kWh)", fontsize=12)
        ax.set_title("Biểu đồ tổn thất các TBA công cộng", fontsize=14)
        ax.tick_params(axis='x', labelrotation=90)
        for i, v in enumerate(ton_that):
            ax.text(i, v, str(int(v*1000)), ha='center', va='bottom', fontsize=8)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Lỗi khi vẽ biểu đồ: {e}")

    st.markdown("### 📈 Biểu đồ tổn thất theo ngưỡng")
    def classify_threshold(val):
        if pd.isna(val): return "Không xác định"
        if val < 0.02:
            return "<2%"
        elif val < 0.03:
            return ">=2 và <3%"
        elif val < 0.04:
            return ">=3 và <4%"
        elif val < 0.05:
            return ">=4 và <5%"
        elif val < 0.07:
            return ">=5 và <7%"
        else:
            return ">=7%"

    df_result["Ngưỡng"] = df_result["Tỷ lệ tổn thất"].apply(classify_threshold)
    threshold_count = df_result["Ngưỡng"].value_counts().sort_index()

    fig2, ax2 = plt.subplots()
    bars = ax2.bar(threshold_count.index, threshold_count.values)
    for bar in bars:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom', ha='center', fontsize=10)
    ax2.set_title("Số lượng TBA theo ngưỡng tổn thất")
    st.pyplot(fig2)

    fig3, ax3 = plt.subplots()
    wedges, texts, autotexts = ax3.pie(
        threshold_count.values,
        labels=threshold_count.index,
        autopct="%.2f%%",
        startangle=90,
        wedgeprops=dict(width=0.4)
    )
    ax3.set_title("Tỷ trọng TBA theo ngưỡng tổn thất")
    st.pyplot(fig3)

    st.markdown("### 📤 Xuất báo cáo")
    csv = df_result.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Tải bảng tổn thất dưới dạng CSV",
        data=csv,
        file_name='BaoCao_TonThat_TBA.csv',
        mime='text/csv'
    )
