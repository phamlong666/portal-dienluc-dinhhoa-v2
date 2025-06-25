import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Báo cáo tổn thất TBA", layout="wide")
st.title("📥 AI_Trợ lý tổn thất")

st.markdown("### 🔍 Chọn loại dữ liệu tổn thất để tải lên:")

# --- Khởi tạo Session State cho dữ liệu tải lên ---
df_keys = ["df_tba_thang", "df_tba_luyke", "df_tba_ck"]
for key in df_keys:
    if key not in st.session_state:
        st.session_state[key] = None

if st.button("🔄 Làm mới dữ liệu"):
    for key in df_keys:
        st.session_state[key] = None
    st.experimental_rerun()

def phan_loai_nghiem(x):
    try:
        x = float(str(x).replace(",", "."))
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

def process_tba_data(df):
    if df is None or df.shape[1] < 10:
        return None, None, None
    df_temp = pd.DataFrame()
    df_temp["Tên TBA"] = df.iloc[:, 1]
    df_temp["Công suất"] = df.iloc[:, 2]
    df_temp["Số KH"] = df.iloc[:, 3]
    df_temp["Điện nhận"] = df.iloc[:, 4]
    df_temp["Điện thương phẩm"] = df.iloc[:, 5]
    df_temp["Điện tổn thất"] = df.iloc[:, 6]
    df_temp["Tỷ lệ tổn thất"] = df.iloc[:, 7]
    df_temp["Kế hoạch"] = df.iloc[:, 8]
    df_temp["So sánh"] = df.iloc[:, 9]
    df_temp["Ngưỡng"] = df_temp["Tỷ lệ tổn thất"].apply(phan_loai_nghiem)
    tong_so = len(df_temp)
    tong_theo_nguong = df_temp["Ngưỡng"].value_counts().reindex(["<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%", ">=5 và <7%", ">=7%"], fill_value=0)
    return tong_so, tong_theo_nguong, df_temp

with st.expander("🔌 Tổn thất các TBA công cộng"):
    temp_upload_tba_thang = st.file_uploader("📅 Tải dữ liệu TBA công cộng - Theo tháng", type=["xlsx"], key="tba_thang")
    if temp_upload_tba_thang:
        st.session_state.df_tba_thang = pd.read_excel(temp_upload_tba_thang, sheet_name="dữ liệu", skiprows=6)

    temp_upload_tba_luyke = st.file_uploader("📊 Tải dữ liệu TBA công cộng - Lũy kế", type=["xlsx"], key="tba_luyke")
    if temp_upload_tba_luyke:
        st.session_state.df_tba_luyke = pd.read_excel(temp_upload_tba_luyke, sheet_name="dữ liệu", skiprows=6)

    temp_upload_tba_ck = st.file_uploader("📈 Tải dữ liệu TBA công cộng - Cùng kỳ", type=["xlsx"], key="tba_ck")
    if temp_upload_tba_ck:
        st.session_state.df_tba_ck = pd.read_excel(temp_upload_tba_ck, sheet_name="dữ liệu", skiprows=6)

if st.session_state.df_tba_thang is not None or st.session_state.df_tba_luyke is not None or st.session_state.df_tba_ck is not None:
    st.markdown("### 📊 Kết quả ánh xạ dữ liệu:")

    tong_so_thang, tong_theo_nguong_thang, df_tba_thang = process_tba_data(st.session_state.df_tba_thang)
    tong_so_luyke, tong_theo_nguong_luyke, _ = process_tba_data(st.session_state.df_tba_luyke)
    tong_so_ck, tong_theo_nguong_ck, _ = process_tba_data(st.session_state.df_tba_ck)

    col1, col2 = st.columns([2, 2])
    colors = ['steelblue', 'darkorange', 'forestgreen', 'goldenrod', 'teal', 'red']

    with col1:
        st.markdown("#### 📊 Số lượng TBA theo ngưỡng tổn thất")
        fig_bar = go.Figure()
        if tong_theo_nguong_thang is not None:
            fig_bar.add_bar(name="Theo tháng", x=tong_theo_nguong_thang.index, y=tong_theo_nguong_thang.values, text=tong_theo_nguong_thang.values, textposition='outside', marker_color='black')
        if tong_theo_nguong_luyke is not None:
            fig_bar.add_bar(name="Lũy kế", x=tong_theo_nguong_luyke.index, y=tong_theo_nguong_luyke.values, text=tong_theo_nguong_luyke.values, textposition='outside', marker_color='black')
        if tong_theo_nguong_ck is not None:
            fig_bar.add_bar(name="Cùng kỳ", x=tong_theo_nguong_ck.index, y=tong_theo_nguong_ck.values, text=tong_theo_nguong_ck.values, textposition='outside', marker_color='black')

        fig_bar.update_layout(barmode='group', height=400, xaxis_title='Ngưỡng tổn thất', yaxis_title='Số lượng TBA', font=dict(color='black', size=14, family='Arial', bold=True))
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.markdown("#### 🧩 Tỷ trọng TBA theo ngưỡng tổn thất")
        for label, tong, data in [("Theo tháng", tong_so_thang, tong_theo_nguong_thang), ("Lũy kế", tong_so_luyke, tong_theo_nguong_luyke), ("Cùng kỳ", tong_so_ck, tong_theo_nguong_ck)]:
            if data is not None:
                st.markdown(f"##### {label} (Tổng số: {tong})")
                fig_pie = go.Figure(data=[
                    go.Pie(labels=data.index, values=data.values, hole=0.5, marker=dict(colors=colors), textinfo='percent+label')
                ])
                fig_pie.update_layout(height=300, showlegend=False, font=dict(color='black', size=14, family='Arial', bold=True))
                st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("#### 📋 Danh sách TBA đã ánh xạ")
    nguong_options = ["(All)"] + ["<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%", ">=5 và <7%", ">=7%"]
    selected_nguong = st.selectbox("Ngưỡng tổn thất", nguong_options)
    if selected_nguong != "(All)":
        df_tba_thang = df_tba_thang[df_tba_thang["Ngưỡng"] == selected_nguong]
    if df_tba_thang is not None:
        st.dataframe(df_tba_thang, use_container_width=True)
