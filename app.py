
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
    # ===== BIỂU ĐỒ THEO NGƯỠNG TỔN THẤT =====
    import plotly.graph_objects as go
    import numpy as np

    # Hàm phân loại tổn thất theo ngưỡng
    def phan_loai_nghiem(x):
        try:
            x = float(x.replace(",", "."))
        except:
            return "Không rõ"
        if x < 2:
            return "<2%"
        elif 2 <= x < 3:
            return ">=2 và <3%"
        elif 3 <= x < 4:
            return ">=3 và <4%"
        elif 4 <= x < 5:
            return ">=4 và <5%"
        elif 5 <= x < 7:
            return ">=5 và <7%"
        else:
            return ">=7%"

    df_result["Ngưỡng"] = df_result["Tỷ lệ tổn thất"].apply(phan_loai_nghiem)

    tong_so = len(df_result)
    tong_theo_nguong = df_result["Ngưỡng"].value_counts().reindex(["<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%", ">=5 và <7%", ">=7%"], fill_value=0)

    col1, col2 = st.columns([2,2])
    with col1:
        st.markdown("#### 📊 Số lượng TBA theo ngưỡng tổn thất")
        fig_bar = go.Figure(data=[
            go.Bar(name='Thực hiện', x=tong_theo_nguong.index, y=tong_theo_nguong.values, marker_color='steelblue'),
        ])
        fig_bar.update_layout(
            height=400,
            xaxis_title='Ngưỡng tổn thất',
            yaxis_title='Số lượng TBA',
            margin=dict(l=20, r=20, t=40, b=40)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.markdown(f"#### 🧩 Tỷ trọng TBA theo ngưỡng tổn thất (Tổng số: {tong_so})")
        fig_pie = go.Figure(data=[
            go.Pie(
                labels=tong_theo_nguong.index,
                values=tong_theo_nguong.values,
                hole=0.5,
                marker=dict(colors=['steelblue', 'darkorange', 'forestgreen', 'goldenrod', 'teal', 'red']),
                textinfo='percent+label',
            )
        ])
        fig_pie.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=40))
        st.plotly_chart(fig_pie, use_container_width=True)

with st.expander("⚡ Tổn thất ha thế"):
    upload_ha_thang = st.file_uploader("📅 Tải dữ liệu hạ áp - Theo tháng", type=["xlsx"], key="ha_thang")
    upload_ha_luyke = st.file_uploader("📊 Tải dữ liệu hạ áp - Lũy kế", type=["xlsx"], key="ha_luyke")
    upload_ha_ck = st.file_uploader("📈 Tải dữ liệu hạ áp - Cùng kỳ", type=["xlsx"], key="ha_ck")

with st.expander("⚡ Tổn thất trung thế"):
    upload_trung_thang = st.file_uploader("📅 Tải dữ liệu Trung áp - Theo tháng", type=["xlsx"], key="trung_thang")
    upload_trung_luyke = st.file_uploader("📊 Tải dữ liệu Trung áp - Lũy kế", type=["xlsx"], key="trung_luyke")
    upload_trung_ck = st.file_uploader("📈 Tải dữ liệu Trung áp - Cùng kỳ", type=["xlsx"], key="trung_ck")

with st.expander("⚡ Tổn thất các đường dây trung thế"):
    upload_trung_thang = st.file_uploader("📅 Tải dữ liệu Trung áp - Theo tháng", type=["xlsx"], key="trung_thang")
    upload_trung_luyke = st.file_uploader("📊 Tải dữ liệu Trung áp - Lũy kế", type=["xlsx"], key="trung_luyke")
    upload_trung_ck = st.file_uploader("📈 Tải dữ liệu Trung áp - Cùng kỳ", type=["xlsx"], key="trung_ck")

with st.expander("🏢 Tổn thất toàn đơn vị"):
    upload_dv_thang = st.file_uploader("📅 Tải dữ liệu Đơn vị - Theo tháng", type=["xlsx"], key="dv_thang")
    upload_dv_luyke = st.file_uploader("📊 Tải dữ liệu Đơn vị - Lũy kế", type=["xlsx"], key="dv_luyke")
    upload_dv_ck = st.file_uploader("📈 Tải dữ liệu Đơn vị - Cùng kỳ", type=["xlsx"], key="dv_ck")



  
