import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Báo cáo tổn thất TBA", layout="wide")
st.title("📥 Tải dữ liệu đầu vào - Báo cáo tổn thất")

st.markdown("### 🔍 Chọn loại dữ liệu tổn thất để tải lên:")

# --- Khởi tạo Session State cho dữ liệu tải lên ---
if 'df_tba_thang' not in st.session_state:
    st.session_state.df_tba_thang = None
if 'df_tba_luyke' not in st.session_state:
    st.session_state.df_tba_luyke = None
if 'df_tba_ck' not in st.session_state:
    st.session_state.df_tba_ck = None
# Thêm khởi tạo cho các loại dữ liệu khác nếu cần


# --- Nút "Làm mới" ---
if st.button("🔄 Làm mới dữ liệu"):
    st.session_state.df_tba_thang = None
    st.session_state.df_tba_luyke = None
    st.session_state.df_tba_ck = None
    # Đặt lại tất cả các biến Session State khác về None nếu có
    st.experimental_rerun()


# Hàm phân loại tổn thất theo ngưỡng (di chuyển lên đầu để dễ tái sử dụng)
def phan_loai_nghiem(x):
    try:
        x = float(str(x).replace(",", ".")) # Chuyển đổi sang string trước khi replace để xử lý giá trị NaN
    except (ValueError, AttributeError):
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

# Hàm xử lý DataFrame và trả về số lượng TBA theo ngưỡng
def process_tba_data(df):
    if df is None:
        return None, None
    df_temp = pd.DataFrame()
    df_temp["Tỷ lệ tổn thất"] = df.iloc[:, 14].map(lambda x: f"{x:.2f}".replace(".", ",") if pd.notna(x) else "")
    df_temp["Ngưỡng"] = df_temp["Tỷ lệ tổn thất"].apply(phan_loai_nghiem)
    tong_so = len(df_temp)
    tong_theo_nguong = df_temp["Ngưỡng"].value_counts().reindex(["<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%", ">=5 và <7%", ">=7%"], fill_value=0)
    return tong_so, tong_theo_nguong


# Tạo các tiện ích con theo phân nhóm
with st.expander("🔌 Tổn thất các TBA công cộng"):
    temp_upload_tba_thang = st.file_uploader("📅 Tải dữ liệu TBA công cộng - Theo tháng", type=["xlsx"], key="tba_thang")
    if temp_upload_tba_thang:
        st.session_state.df_tba_thang = pd.read_excel(temp_upload_tba_thang, skiprows=6)
        st.success("✅ Đã tải dữ liệu tổn thất TBA công cộng theo tháng!")

    temp_upload_tba_luyke = st.file_uploader("📊 Tải dữ liệu TBA công cộng - Lũy kế", type=["xlsx"], key="tba_luyke")
    if temp_upload_tba_luyke:
        st.session_state.df_tba_luyke = pd.read_excel(temp_upload_tba_luyke, skiprows=6)
        st.success("✅ Đã tải dữ liệu tổn thất TBA công cộng - Lũy kế!")

    temp_upload_tba_ck = st.file_uploader("📈 Tải dữ liệu TBA công cộng - Cùng kỳ", type=["xlsx"], key="tba_ck")
    if temp_upload_tba_ck:
        st.session_state.df_tba_ck = pd.read_excel(temp_upload_tba_ck, skiprows=6)
        st.success("✅ Đã tải dữ liệu tổn thất TBA công cộng - Cùng kỳ!")

# --- Xử lý và hiển thị dữ liệu tổng hợp nếu có ít nhất một file được tải lên ---
if st.session_state.df_tba_thang is not None or \
   st.session_state.df_tba_luyke is not None or \
   st.session_state.df_tba_ck is not None:

    st.markdown("### 📊 Kết quả ánh xạ dữ liệu:")

    # Xử lý dữ liệu từng loại và chuẩn bị cho biểu đồ
    tong_so_thang, tong_theo_nguong_thang = process_tba_data(st.session_state.df_tba_thang)
    tong_so_luyke, tong_theo_nguong_luyke = process_tba_data(st.session_state.df_tba_luyke)
    tong_so_ck, tong_theo_nguong_ck = process_tba_data(st.session_state.df_tba_ck)

    col1, col2 = st.columns([2,2])

    with col1:
        st.markdown("#### 📊 Số lượng TBA theo ngưỡng tổn thất")
        fig_bar = go.Figure()
        colors = ['steelblue', 'darkorange', 'forestgreen', 'goldenrod', 'teal', 'red'] # Màu sắc cho từng ngưỡng

        # Thêm các thanh cho "Theo tháng"
        if tong_theo_nguong_thang is not None:
            fig_bar.add_trace(go.Bar(
                name='Theo tháng',
                x=tong_theo_nguong_thang.index,
                y=tong_theo_nguong_thang.values,
                #marker_color=colors, # Nếu muốn mỗi nhóm có màu riêng biệt cho mỗi cột
                text=tong_theo_nguong_thang.values,
                textposition='outside',
                textfont=dict(color='black')
            ))

        # Thêm các thanh cho "Lũy kế"
        if tong_theo_nguong_luyke is not None:
            fig_bar.add_trace(go.Bar(
                name='Lũy kế',
                x=tong_theo_nguong_luyke.index,
                y=tong_theo_nguong_luyke.values,
                #marker_color=colors,
                text=tong_theo_nguong_luyke.values,
                textposition='outside',
                textfont=dict(color='black')
            ))

        # Thêm các thanh cho "Cùng kỳ"
        if tong_theo_nguong_ck is not None:
            fig_bar.add_trace(go.Bar(
                name='Cùng kỳ',
                x=tong_theo_nguong_ck.index,
                y=tong_theo_nguong_ck.values,
                #marker_color=colors,
                text=tong_theo_nguong_ck.values,
                textposition='outside',
                textfont=dict(color='black')
            ))

        fig_bar.update_layout(
            barmode='group', # Hiển thị các thanh cạnh nhau
            height=400,
            xaxis_title='Ngưỡng tổn thất',
            yaxis_title='Số lượng TBA',
            margin=dict(l=20, r=20, t=40, b=40),
            legend_title_text='Loại dữ liệu'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.markdown("#### 🧩 Tỷ trọng TBA theo ngưỡng tổn thất")
        # Biểu đồ tròn sẽ phức tạp hơn khi kết hợp 3 loại dữ liệu.
        # Thường thì biểu đồ tròn chỉ hiển thị tỷ trọng của MỘT tập dữ liệu.
        # Nếu muốn hiển thị 3 biểu đồ tròn, bạn có thể làm như sau:

        if tong_theo_nguong_thang is not None:
            st.markdown(f"##### Theo tháng (Tổng số: {tong_so_thang})")
            fig_pie_thang = go.Figure(data=[
                go.Pie(
                    labels=tong_theo_nguong_thang.index,
                    values=tong_theo_nguong_thang.values,
                    hole=0.5,
                    marker=dict(colors=colors),
                    textinfo='percent+label',
                    name='Theo tháng'
                )
            ])
            fig_pie_thang.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=40), showlegend=False)
            st.plotly_chart(fig_pie_thang, use_container_width=True)

        if tong_theo_nguong_luyke is not None:
            st.markdown(f"##### Lũy kế (Tổng số: {tong_so_luyke})")
            fig_pie_luyke = go.Figure(data=[
                go.Pie(
                    labels=tong_theo_nguong_luyke.index,
                    values=tong_theo_nguong_luyke.values,
                    hole=0.5,
                    marker=dict(colors=colors),
                    textinfo='percent+label',
                    name='Lũy kế'
                )
            ])
            fig_pie_luyke.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=40), showlegend=False)
            st.plotly_chart(fig_pie_luyke, use_container_width=True)

        if tong_theo_nguong_ck is not None:
            st.markdown(f"##### Cùng kỳ (Tổng số: {tong_so_ck})")
            fig_pie_ck = go.Figure(data=[
                go.Pie(
                    labels=tong_theo_nguong_ck.index,
                    values=tong_theo_nguong_ck.values,
                    hole=0.5,
                    marker=dict(colors=colors),
                    textinfo='percent+label',
                    name='Cùng kỳ'
                )
            ])
            fig_pie_ck.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=40), showlegend=False)
            st.plotly_chart(fig_pie_ck, use_container_width=True)


    # Hiển thị DataFrame ánh xạ cho file "Theo tháng" nếu nó tồn tại
    if st.session_state.df_tba_thang is not None:
        st.markdown("##### Dữ liệu TBA công cộng - Theo tháng:")
        df_test = st.session_state.df_tba_thang
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
        st.dataframe(df_result)

    # Bạn có thể thêm hiển thị DataFrame ánh xạ cho Lũy kế và Cùng kỳ tương tự ở đây
    # if st.session_state.df_tba_luyke is not None:
    #     st.markdown("##### Dữ liệu TBA công cộng - Lũy kế:")
    #     # ... xử lý và hiển thị df_result cho lũy kế
    #     st.dataframe(df_result_luyke)

    # if st.session_state.df_tba_ck is not None:
    #     st.markdown("##### Dữ liệu TBA công cộng - Cùng kỳ:")
    #     # ... xử lý và hiển thị df_result cho cùng kỳ
    #     st.dataframe(df_result_ck)


with st.expander("⚡ Tổn thất hạ thế"):
    upload_ha_thang = st.file_uploader("📅 Tải dữ liệu hạ áp - Theo tháng", type=["xlsx"], key="ha_thang")
    upload_ha_luyke = st.file_uploader("📊 Tải dữ liệu hạ áp - Lũy kế", type=["xlsx"], key="ha_luyke")
    upload_ha_ck = st.file_uploader("📈 Tải dữ liệu hạ áp - Cùng kỳ", type=["xlsx"], key="ha_ck")

with st.expander("⚡ Tổn thất trung thế"):
    upload_trung_thang_tt = st.file_uploader("📅 Tải dữ liệu Trung áp - Theo tháng", type=["xlsx"], key="trung_thang_tt")
    upload_trung_luyke_tt = st.file_uploader("📊 Tải dữ liệu Trung áp - Lũy kế", type=["xlsx"], key="trung_luyke_tt")
    upload_trung_ck_tt = st.file_uploader("📈 Tải dữ liệu Trung áp - Cùng kỳ", type=["xlsx"], key="trung_ck_tt")

with st.expander("⚡ Tổn thất các đường dây trung thế"):
    upload_trung_thang_dy = st.file_uploader("📅 Tải dữ liệu Trung áp - Theo tháng", type=["xlsx"], key="trung_thang_dy")
    upload_trung_luyke_dy = st.file_uploader("📊 Tải dữ liệu Trung áp - Lũy kế", type=["xlsx"], key="trung_luyke_dy")
    upload_trung_ck_dy = st.file_uploader("📈 Tải dữ liệu Trung áp - Cùng kỳ", type=["xlsx"], key="trung_ck_dy")

with st.expander("🏢 Tổn thất toàn đơn vị"):
    upload_dv_thang = st.file_uploader("📅 Tải dữ liệu Đơn vị - Theo tháng", type=["xlsx"], key="dv_thang")
    upload_dv_luyke = st.file_uploader("📊 Tải dữ liệu Đơn vị - Lũy kế", type=["xlsx"], key="dv_luyke")
    upload_dv_ck = st.file_uploader("📈 Tải dữ liệu Đơn vị - Cùng kỳ", type=["xlsx"], key="dv_ck")