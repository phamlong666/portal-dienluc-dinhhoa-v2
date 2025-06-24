
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Báo cáo tổn thất TBA", layout="wide")
st.title("📥 Tải dữ liệu đầu vào - Báo cáo tổn thất")

st.markdown("### 🔍 Chọn loại dữ liệu tổn thất để tải lên:")

# Tạo các tiện ích con theo phân nhóm
with st.expander("🔌 Tổn thất các TBA công cộng"):
    upload_tba_thang = st.file_uploader("📅 Tải dữ liệu TBA công cộng - Theo tháng", type=["xlsx"], key="tba_thang")
    upload_tba_luyke = st.file_uploader("📊 Tải dữ liệu TBA công cộng - Lũy kế", type=["xlsx"], key="tba_luyke")
    upload_tba_cungkyd = st.file_uploader("📈 Tải dữ liệu TBA công cộng - Cùng kỳ", type=["xlsx"], key="tba_ck")

with st.expander("⚡ Tổn thất các đường dây trung thế"):
    upload_trung_thang = st.file_uploader("📅 Tải dữ liệu Trung áp - Theo tháng", type=["xlsx"], key="trung_thang")
    upload_trung_luyke = st.file_uploader("📊 Tải dữ liệu Trung áp - Lũy kế", type=["xlsx"], key="trung_luyke")
    upload_trung_ck = st.file_uploader("📈 Tải dữ liệu Trung áp - Cùng kỳ", type=["xlsx"], key="trung_ck")

with st.expander("🏢 Tổn thất toàn đơn vị"):
    upload_dv_thang = st.file_uploader("📅 Tải dữ liệu Đơn vị - Theo tháng", type=["xlsx"], key="dv_thang")
    upload_dv_luyke = st.file_uploader("📊 Tải dữ liệu Đơn vị - Lũy kế", type=["xlsx"], key="dv_luyke")
    upload_dv_ck = st.file_uploader("📈 Tải dữ liệu Đơn vị - Cùng kỳ", type=["xlsx"], key="dv_ck")

# Kết quả chạy thử: kiểm tra dữ liệu đầu vào tổn thất TBA công cộng theo tháng
if upload_tba_thang:
    df_test = pd.read_excel(upload_tba_thang, skiprows=6)
    st.success("✅ Đã tải dữ liệu tổn thất TBA công cộng theo tháng!")
    st.dataframe(df_test.head())

    # Ánh xạ nhanh theo bảng chuẩn đã tạo
    df_result = pd.DataFrame()
    df_result["STT"] = range(1, len(df_test) + 1)
    df_result["Tên TBA"] = df_test.iloc[:, 2]
    df_result["Công suất"] = df_test.iloc[:, 3]
    df_result["Điện nhận"] = df_test.iloc[:, 6]
    df_result["Thương phẩm"] = df_test.iloc[:, 6] - df_test.iloc[:, 7]
    df_result["Điện tổn thất"] = df_test.iloc[:, 13].round(0).astype("Int64")
    df_result["Tỷ lệ tổn thất"] = df_test.iloc[:, 14].map(lambda x: f"{x:.2f}".replace(".", ",") if pd.notna(x) else "")
    df_result["Kế hoạch"] = df_test.iloc[:, 15].map(lambda x: f"{x:.2f}".replace(".", ",") if pd.notna(x) else "")
    df_result["So sánh"] = df_test.iloc[:, 16].map(lambda x: f"{x:.2f}".replace(".", ",") if pd.notna(x) else "")

    st.markdown("### 📊 Kết quả ánh xạ dữ liệu:")
    st.dataframe(df_result)

    # Hiển thị biểu đồ minh họa nhanh
    st.markdown("### 📉 Biểu đồ tổn thất theo TBA")
    fig, ax = plt.subplots()
    ax.bar(df_result["Tên TBA"], df_result["Điện tổn thất"])
    ax.set_xlabel("Tên TBA")
    ax.set_ylabel("Điện tổn thất (kWh)")
    ax.set_title("Biểu đồ tổn thất các TBA công cộng")
    ax.tick_params(axis='x', labelrotation=90)
    for i, v in enumerate(df_result["Điện tổn thất"]):
        ax.text(i, v, str(v), ha='center', va='bottom', fontsize=8)
    st.pyplot(fig)
