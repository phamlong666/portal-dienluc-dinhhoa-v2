import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import io
from docx import Document
from docx.shared import Inches
from pptx import Presentation
from pptx.util import Inches as PptInches

st.set_page_config(page_title="Báo cáo tổn thất TBA", layout="wide")
st.title("📊 Báo cáo tổn thất các TBA công cộng")

file_keys = ["Theo Tháng", "Lũy kế", "Cùng kỳ"]
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = {}
uploaded_data = st.session_state.uploaded_data

col_uploads = st.columns(3)
for i, key in enumerate(file_keys):
    with col_uploads[i]:
        file = st.file_uploader(f"📁 File {key}", type=["xlsx"], key=f"upload_{key}")
        if file:
            xls = pd.ExcelFile(file)
            sheet_name = [s for s in xls.sheet_names if "ánh xạ" in s.lower()][0]
            df = pd.read_excel(xls, sheet_name=sheet_name)
            uploaded_data[key] = df

st.button("🔄 Làm mới", on_click=lambda: st.session_state.clear())

if uploaded_data:
    if st.button("📌 Tạo báo cáo"):

        def export_powerpoint(title, actual, plan):
            prs = Presentation()
            slide = prs.slides.add_slide(prs.slide_layouts[5])
            shapes = slide.shapes
            title_shape = shapes.title
            title_shape.text = title

            txBox = shapes.add_textbox(PptInches(1), PptInches(1.5), PptInches(8), PptInches(5))
            tf = txBox.text_frame
            tf.text = f"Tỷ lệ tổn thất thực tế: {actual:.2f}%"
            p = tf.add_paragraph()
            p.text = f"Tỷ lệ tổn thất kế hoạch: {plan:.2f}%"
            return prs

        for key, df in uploaded_data.items():
            with st.expander(f"🔍 Dữ liệu: {key}", expanded=True):
            df_copy = df.copy()
            percent_cols = [col for col in df_copy.columns if "%" in col]
            for col in percent_cols:
                df_copy[col] = pd.to_numeric(df_copy[col], errors="coerce")
                df_copy[col] = df_copy[col].map(lambda x: f"{x:.2f}%" if pd.notna(x) else "")
            st.dataframe(df_copy.style.set_properties(**{"font-size": "18pt"}), use_container_width=True)

            total_input = df["Điện nhận (kWh)"].sum()
            total_loss = df["Điện tổn thất (kWh)"].sum()
            actual = (total_loss / total_input * 100) if total_input else 0
            plan_col = [c for c in df.columns if "kế hoạch" in c.lower()][0]
            plan_series = df[plan_col]
            plan = ((plan_series / 100 * df["Điện nhận (kWh)"]).sum() / total_input * 100) if total_input else 0

            st.markdown(f"#### 📉 Biểu đồ tổn thất - {key}")
            fig = go.Figure(data=[
                go.Bar(
                    x=["Thực tế", "Kế hoạch"],
                    y=[actual, plan],
                    marker=dict(
                        color=random.sample(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'], 2),
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

        if len(uploaded_data) == 3:
            st.markdown("### 📊 Biểu đồ hợp nhất tổn thất các file")
            data_total = []
            for key in file_keys:
                df = uploaded_data[key]
                total_input = df["Điện nhận (kWh)"].sum()
                total_loss = df["Điện tổn thất (kWh)"].sum()
                actual = (total_loss / total_input * 100) if total_input else 0
                plan_col = [c for c in df.columns if "kế hoạch" in c.lower()][0]
                plan_series = df[plan_col]
                plan = ((plan_series / 100 * df["Điện nhận (kWh)"]).sum() / total_input * 100) if total_input else 0
                data_total.append((key, actual, plan))

            fig2 = go.Figure()
            x = file_keys
            actuals = [d[1] for d in data_total]
            plans = [d[2] for d in data_total]
            fig2.add_trace(go.Bar(
                x=x,
                y=actuals,
                name='Thực tế',
                marker_color=random.choice(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']),
                text=[f"{v:.2f}%" for v in actuals],
                textposition='auto'
            ))
            fig2.add_trace(go.Bar(
                x=x,
                y=plans,
                name='Kế hoạch',
                marker_color=random.choice(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']),
                text=[f"{v:.2f}%" for v in plans],
                textposition='auto'
            ))
            fig2.update_layout(
                barmode='group',
                height=350,
                margin=dict(l=30, r=30, t=30, b=30),
                font=dict(size=16),
                yaxis=dict(title="Tỷ lệ (%)", range=[0, max(actuals + plans) * 1.2 if actuals else 5])
            )
            st.plotly_chart(fig2, use_container_width=True)
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