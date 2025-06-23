import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Biểu đồ tổn thất điện năng", layout="wide")
st.title("📊 Biểu đồ tổn thất điện năng từ dữ liệu Excel")

if "uploaded_df" not in st.session_state:
    st.session_state.uploaded_df = None

uploaded_file = st.file_uploader("📁 Tải lên file Excel chứa bảng 'Bảng Kết quả ánh xạ dữ liệu'")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, sheet_name=[s for s in pd.ExcelFile(uploaded_file).sheet_names if "ánh xạ" in s.lower()][0])
        st.session_state.uploaded_df = df
    except Exception as e:
        st.error(f"Không đọc được file: {e}")

if st.session_state.uploaded_df is not None:
    df = st.session_state.uploaded_df
    with st.expander("📋 Dữ liệu đầu vào", expanded=False):
        st.dataframe(df)

    if "Tỷ lệ tổn thất" in df.columns and "Kế hoạch" in df.columns:
        actual = df["Tỷ lệ tổn thất"].iloc[0]
        plan = df["Kế hoạch"].iloc[0]

        fig = go.Figure(data=[
            go.Bar(
                x=["Thực tế", "Kế hoạch"],
                y=[actual, plan],
                marker=dict(
                    color=["#1f77b4", "#ff7f0e"],
                    line=dict(color='black', width=1)
                ),
                text=[f"{actual:.2f}%", f"{plan:.2f}%"],
                textposition='auto',
                width=[0.4, 0.4]
            )
        ])

        fig.update_layout(
            title="Tỷ lệ tổn thất điện năng",
            margin=dict(l=20, r=20, t=40, b=20),
            height=350,
            font=dict(size=16),
            showlegend=False,
            yaxis=dict(title="Tỷ lệ (%)", range=[0, max(actual, plan) * 1.2 if max(actual, plan) > 0 else 5])
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Không tìm thấy cột 'Tỷ lệ tổn thất' hoặc 'Kế hoạch' trong dữ liệu.")
else:
    st.info("📌 Vui lòng tải lên file Excel để bắt đầu.")