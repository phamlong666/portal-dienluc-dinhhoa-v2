import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Báo cáo tổn thất TBA", layout="wide")
st.title("📊 Báo cáo tổn thất các TBA công cộng")

file_keys = ["Theo Tháng", "Lũy kế", "Cùng kỳ"]
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = {}

col_uploads = st.columns(3)
for i, key in enumerate(file_keys):
    with col_uploads[i]:
        file = st.file_uploader(f"📁 File {key}", type=["xlsx"], key=f"upload_{key}")
        if file:
            xls = pd.ExcelFile(file)
            found_sheet = None
            # Flexible search for sheet name
            for s_name in xls.sheet_names:
                if "bảng kết quả" in s_name.lower() and "ánh xạ dữ liệu" in s_name.lower():
                    found_sheet = s_name
                    break
            
            if found_sheet:
                df = pd.read_excel(xls, sheet_name=found_sheet)
                st.session_state.uploaded_data[key] = df
            else:
                st.error(f"File '{key}' không tìm thấy sheet chứa cả 'Bảng kết quả' và 'ánh xạ dữ liệu'. Vui lòng kiểm tra lại tên sheet trong file Excel.")
                st.write(f"Các sheet có sẵn trong file '{key}': {xls.sheet_names}") # Gợi ý các sheet có sẵn
                
def plot_dynamic_bar_chart(uploaded_data):
    try:
        common_col = [col for col in uploaded_data["Theo Tháng"].columns if "tháng" in col.lower()][0]
    except IndexError:
        common_col = uploaded_data["Theo Tháng"].columns[0]

    months = uploaded_data["Theo Tháng"][common_col].astype(str).tolist()
    datasets = []
    colors = {
        "Theo Tháng": "goldenrod",
        "Lũy kế": "forestgreen",
        "Cùng kỳ": "deepskyblue"
    }

    for key in file_keys:
        df = uploaded_data[key]
        y = []
        if "Tỷ lệ tổn thất (%)" in df.columns:
            y = df["Tỷ lệ tổn thất (%)"].tolist()
        else:
            st.warning(f"File '{key}' thiếu cột 'Tỷ lệ tổn thất (%)'. Biểu đồ 3D có thể không hiển thị đầy đủ.")
            continue

        datasets.append((key, y))

    fig = go.Figure()
    for label, y in datasets:
        fig.add_trace(go.Bar(
            name=label,
            x=months,
            y=y,
            marker=dict(color=colors[label], line=dict(color='black', width=1.2)),
            text=[f"{v:.2f}" if isinstance(v, (int, float)) else v for v in y],
            textposition='outside'
        ))

    fig.update_layout(
        barmode='group',
        title="📊 Biểu đồ tổn thất mô phỏng 3D theo nhóm",
        plot_bgcolor='rgba(240,240,255,1)',
        font=dict(size=16),
        height=500,
        margin=dict(t=50, l=20, r=20, b=40),
        yaxis=dict(title="Tỷ lệ / Giá trị", gridcolor="lightgray")
    )
    st.plotly_chart(fig, use_container_width=True)

if st.session_state.uploaded_data:
    if st.button("📌 Tạo báo cáo"):

        marker_colors = {
            "Theo Tháng": ["#3366cc", "#ff9900"],
            "Lũy kế": ["#2ca02c", "#d62728"],
            "Cùng kỳ": ["#8e44ad", "#f1c40f"]
        }

        for key, df in st.session_state.uploaded_data.items():
            with st.expander(f"🔍 Dữ liệu: {key}", expanded=True):
                df_copy = df.copy()
                percent_cols = [col for col in df_copy.columns if "%" in col]
                for col in percent_cols:
                    df_copy[col] = pd.to_numeric(df_copy[col], errors="coerce")
                    df_copy[col] = df_copy[col].map(lambda x: f"{x:.2f}%" if pd.notna(x) else "")
                st.dataframe(df_copy, use_container_width=True)

        if len(st.session_state.uploaded_data) == 3:
            # Biểu đồ hợp nhất
            st.markdown("### 📊 Biểu đồ hợp nhất tổn thất các file")
            data_total = []
            for key in file_keys:
                df = st.session_state.uploaded_data[key]
                
                actual = 0
                plan = 0

                if "Tỷ lệ tổn thất (%)" in df.columns and not df["Tỷ lệ tổn thất (%)"].empty:
                    actual = df["Tỷ lệ tổn thất (%)"].iloc[0] 
                else:
                    st.warning(f"File '{key}' thiếu hoặc rỗng cột 'Tỷ lệ tổn thất (%)'.")

                if "Kế hoạch (%)" in df.columns and not df["Kế hoạch (%)"].empty:
                    plan = df["Kế hoạch (%)"].iloc[0]
                else:
                    st.warning(f"File '{key}' thiếu hoặc rỗng cột 'Kế hoạch (%)'.")
                
                data_total.append((key, actual, plan))

            fig2 = go.Figure()
            for label, actual, plan in data_total:
                fig2.add_trace(go.Bar(
                    x=[f"{label} - Thực tế"],
                    y=[actual],
                    name=f"Thực tế - {label}",
                    marker=dict(color=marker_colors[label][0], line=dict(color='black', width=1.5)),
                    text=f"{actual:.2f}%",
                    textposition='auto'
                ))
                fig2.add_trace(go.Bar(
                    x=[f"{label} - Kế hoạch"],
                    y=[plan],
                    name=f"Kế hoạch - {label}",
                    marker=dict(color=marker_colors[label][1], line=dict(color='black', width=1.5)),
                    text=f"{plan:.2f}%",
                    textposition='auto'
                ))

            fig2.update_layout(
                barmode='group',
                height=500,
                font=dict(size=17),
                yaxis=dict(title="Tỷ lệ (%)"),
                plot_bgcolor='rgba(240,240,240,1)'
            )
            st.plotly_chart(fig2, use_container_width=True)

            st.markdown("### 📊 Biểu đồ mô phỏng 3D (cột nhóm theo tháng)")
            plot_dynamic_bar_chart(st.session_state.uploaded_data)

st.session_state.setdefault("dummy", 1)