import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Báo cáo tổn thất TBA", layout="wide")
st.title("📥 Tải dữ liệu đầu vào - Báo cáo tổn thất")

st.markdown("### 🔍 Chọn loại dữ liệu tổn thất để tải lên:")

# --- Khởi tạo Session State cho dữ liệu tải lên ---
# Dùng để lưu trữ DataFrame sau khi đọc file
if 'df_tba_thang' not in st.session_state:
    st.session_state.df_tba_thang = None
if 'df_tba_luyke' not in st.session_state:
    st.session_state.df_tba_luyke = None
# ... (Bạn sẽ cần khởi tạo tương tự cho tất cả các loại dữ liệu khác nếu muốn giữ chúng lại)


# --- Nút "Làm mới" ---
if st.button("🔄 Làm mới dữ liệu"):
    st.session_state.df_tba_thang = None # Đặt lại dữ liệu TBA tháng về None
    st.session_state.df_tba_luyke = None # Đặt lại dữ liệu TBA lũy kế về None
    # ... (Đặt lại tất cả các biến Session State khác về None nếu có)
    st.experimental_rerun() # Chạy lại ứng dụng để cập nhật giao diện


# Tạo các tiện ích con theo phân nhóm
with st.expander("🔌 Tổn thất các TBA công cộng"):
    # Sử dụng biến tạm thời để xử lý file_uploader
    temp_upload_tba_thang = st.file_uploader("📅 Tải dữ liệu TBA công cộng - Theo tháng", type=["xlsx"], key="tba_thang")
    if temp_upload_tba_thang:
        st.session_state.df_tba_thang = pd.read_excel(temp_upload_tba_thang, skiprows=6)
        st.success("✅ Đã tải dữ liệu tổn thất TBA công cộng theo tháng!")

    upload_tba_luyke = st.file_uploader("📊 Tải dữ liệu TBA công cộng - Lũy kế", type=["xlsx"], key="tba_luyke")
    if upload_tba_luyke:
        st.session_state.df_tba_luyke = pd.read_excel(upload_tba_luyke, skiprows=6)
        st.success("✅ Đã tải dữ liệu tổn thất TBA công cộng - Lũy kế!")

    upload_tba_cungkyd = st.file_uploader("📈 Tải dữ liệu TBA công cộng - Cùng kỳ", type=["xlsx"], key="tba_ck")
    # Tương tự cho các file khác nếu bạn muốn lưu vào session_state


# Kết quả chạy thử: kiểm tra dữ liệu đầu vào tổn thất TBA công cộng theo tháng
# Bây giờ chúng ta kiểm tra dữ liệu từ session_state thay vì biến cục bộ
if st.session_state.df_tba_thang is not None:
    df_test = st.session_state.df_tba_thang
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
        # Định nghĩa màu cho từng cột
        colors = ['steelblue', 'darkorange', 'forestgreen', 'goldenrod', 'teal', 'red']
        fig_bar = go.Figure(data=[
            go.Bar(
                name='Thực hiện',
                x=tong_theo_nguong.index,
                y=tong_theo_nguong.values,
                marker_color=colors, # Áp dụng màu riêng biệt
                text=tong_theo_nguong.values, # Hiển thị giá trị
                textposition='outside', # Vị trí hiển thị giá trị (trên cùng của cột)
                textfont=dict(color='black') # Màu chữ của giá trị
            )
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

with st.expander("⚡ Tổn thất hạ thế"):
    upload_ha_thang = st.file_uploader("📅 Tải dữ liệu hạ áp - Theo tháng", type=["xlsx"], key="ha_thang")
    # ... (Tương tự, bạn có thể lưu dữ liệu hạ áp vào session_state)
    upload_ha_luyke = st.file_uploader("📊 Tải dữ liệu hạ áp - Lũy kế", type=["xlsx"], key="ha_luyke")
    upload_ha_ck = st.file_uploader("📈 Tải dữ liệu hạ áp - Cùng kỳ", type=["xlsx"], key="ha_ck")

with st.expander("⚡ Tổn thất trung thế"):
    upload_trung_thang_tt = st.file_uploader("📅 Tải dữ liệu Trung áp - Theo tháng", type=["xlsx"], key="trung_thang_tt")
    # ... (Tương tự, bạn có thể lưu dữ liệu trung thế vào session_state)
    upload_trung_luyke_tt = st.file_uploader("📊 Tải dữ liệu Trung áp - Lũy kế", type=["xlsx"], key="trung_luyke_tt")
    upload_trung_ck_tt = st.file_uploader("📈 Tải dữ liệu Trung áp - Cùng kỳ", type=["xlsx"], key="trung_ck_tt")

with st.expander("⚡ Tổn thất các đường dây trung thế"):
    upload_trung_thang_dy = st.file_uploader("📅 Tải dữ liệu Trung áp - Theo tháng", type=["xlsx"], key="trung_thang_dy")
    # ... (Tương tự, bạn có thể lưu dữ liệu đường dây trung thế vào session_state)
    upload_trung_luyke_dy = st.file_uploader("📊 Tải dữ liệu Trung áp - Lũy kế", type=["xlsx"], key="trung_luyke_dy")
    upload_trung_ck_dy = st.file_uploader("📈 Tải dữ liệu Trung áp - Cùng kỳ", type=["xlsx"], key="trung_ck_dy")

with st.expander("🏢 Tổn thất toàn đơn vị"):
    upload_dv_thang = st.file_uploader("📅 Tải dữ liệu Đơn vị - Theo tháng", type=["xlsx"], key="dv_thang")
    # ... (Tương tự, bạn có thể lưu dữ liệu đơn vị vào session_state)
    upload_dv_luyke = st.file_uploader("📊 Tải dữ liệu Đơn vị - Lũy kế", type=["xlsx"], key="dv_luyke")
    upload_dv_ck = st.file_uploader("📈 Tải dữ liệu Đơn vị - Cùng kỳ", type=["xlsx"], key="dv_ck")