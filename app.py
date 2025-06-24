import streamlit as st
import pandas as pd
import numpy as np
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
            sheet_name = [s for s in xls.sheet_names if "ánh xạ" in s.lower()][0]
            df = pd.read_excel(xls, sheet_name=sheet_name)
            st.session_state.uploaded_data[key] = df

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
                st.dataframe(df_copy.style.set_properties(**{"font-size": "18pt"}), use_container_width=True)

                total_input = df["Điện nhận (kWh)"].sum()
                total_loss = df["Điện tổn thất (kWh)"].sum()
                actual = (total_loss / total_input * 100) if total_input else 0
                plan_col = [c for c in df.columns if "kế hoạch" in c.lower()][0]
                plan_series = df[plan_col]
                plan = ((plan_series / 100 * df["Điện nhận (kWh)"]).sum() / total_input * 100) if total_input else 0

                fig = go.Figure(data=[
                    go.Bar(
                        x=["Thực tế", "Kế hoạch"],
                        y=[actual, plan],
                        marker=dict(
                            color=marker_colors.get(key, ["#888", "#ccc"]),
                            line=dict(color='black', width=1.2)
                        ),
                        text=[f"{actual:.2f}%", f"{plan:.2f}%"],
                        textposition='auto',
                        textfont=dict(size=18),
                        width=[0.4, 0.4],
                        opacity=0.95
                    )
                ])
                fig.update_layout(
                    title=f"Tỷ lệ tổn thất – {key}",
                    margin=dict(l=20, r=20, t=40, b=20),
                    height=350,
                    font=dict(size=16),
                    showlegend=False,
                    yaxis=dict(title="Tỷ lệ (%)", range=[0, max(actual, plan) * 1.2 if max(actual, plan) > 0 else 5]),
                    plot_bgcolor='rgba(245,245,245,1)'
                )
                st.plotly_chart(fig, use_container_width=True)

        if len(st.session_state.uploaded_data) == 3:
            st.markdown("### 📊 Biểu đồ hợp nhất tổn thất các file")
            data_total = []
            for key in file_keys:
                df = st.session_state.uploaded_data[key]
                total_input = df["Điện nhận (kWh)"].sum()
                total_loss = df["Điện tổn thất (kWh)"].sum()
                actual = (total_loss / total_input * 100) if total_input else 0
                plan_col = [c for c in df.columns if "kế hoạch" in c.lower()][0]
                plan_series = df[plan_col]
                plan = ((plan_series / 100 * df["Điện nhận (kWh)"]).sum() / total_input * 100) if total_input else 0
                data_total.append((key, actual, plan))

            fig2 = go.Figure()
            for i, (label, actual, plan) in enumerate(data_total):
                fig2.add_trace(go.Bar(
                    x=[label],
                    y=[actual],
                    name=f"Thực tế - {label}",
                    marker=dict(color=marker_colors[label][0], line=dict(color='black', width=1.2)),
                    text=f"{actual:.2f}%",
                    textposition='auto',
                    textfont=dict(size=18),
                    opacity=0.95
                ))
                fig2.add_trace(go.Bar(
                    x=[label],
                    y=[plan],
                    name=f"Kế hoạch - {label}",
                    marker=dict(color=marker_colors[label][1], line=dict(color='black', width=1.2)),
                    text=f"{plan:.2f}%",
                    textposition='auto',
                    textfont=dict(size=18),
                    opacity=0.85
                ))

            fig2.update_layout(
                barmode='group',
                height=400,
                margin=dict(l=30, r=30, t=40, b=30),
                font=dict(size=16),
                yaxis=dict(title="Tỷ lệ (%)", range=[0, max(actual + plan for _, actual, plan in data_total) * 1.2]),
                plot_bgcolor='rgba(240,240,240,1)'
            )
            st.plotly_chart(fig2, use_container_width=True)

            if st.button("📊 Biểu đồ theo ngưỡng tổn thất"):
                categories = ["<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%", ">=5 và <7%", ">=7%"]
                values_cungky = [4, 10, 34, 46, 68, 31]
                values_thuchien = [105, 44, 27, 16, 11, 0]
                sizes = [51.72, 21.67, 13.30, 7.88, 5.42, 0.00]

                fig3 = go.Figure()
                fig3.add_trace(go.Bar(name="Cùng kỳ", x=categories, y=values_cungky, marker_color="lightgray",
                                      text=values_cungky, textposition='auto', textfont=dict(size=18)))
                fig3.add_trace(go.Bar(name="Thực hiện", x=categories, y=values_thuchien, marker_color="#1f77b4",
                                      text=values_thuchien, textposition='auto', textfont=dict(size=18)))
                fig3.update_layout(
                    barmode='group',
                    title="📊 Số lượng TBA theo ngưỡng tổn thất",
                    height=400,
                    margin=dict(l=30, r=30, t=40, b=30),
                    font=dict(size=16),
                    plot_bgcolor='rgba(245,245,245,1)'
                )
                st.plotly_chart(fig3, use_container_width=True)

                fig4 = go.Figure(data=[
                    go.Pie(labels=categories, values=sizes, hole=.4, textinfo='label+percent',
                           marker=dict(colors=["#1f77b4", "#ff9900", "#2ca02c", "#bcbd22", "#17becf", "#d62728"]),
                           textfont=dict(size=16))
                ])
                fig4.update_layout(title="🔄 Tỷ trọng TBA theo ngưỡng tổn thất", height=400)
                st.plotly_chart(fig4, use_container_width=True)
