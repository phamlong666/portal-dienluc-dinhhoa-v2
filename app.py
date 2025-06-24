import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
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

if st.session_state.uploaded_data and len(st.session_state.uploaded_data) == 3:
    if st.button("📊 Biểu đồ lũy kế theo tháng như mẫu"):
        df_2023 = st.session_state.uploaded_data["Theo Tháng"]
        df_kh = st.session_state.uploaded_data["Lũy kế"]
        df_ck = st.session_state.uploaded_data["Cùng kỳ"]

        # Giả định có cột 'Tháng' và 'Số lượng'
        months = sorted(list(set(df_2023['Tháng'].unique()) | set(df_kh['Tháng'].unique()) | set(df_ck['Tháng'].unique())))

        def get_month_data(df):
            return df.groupby('Tháng')['Số lượng'].sum().reindex(months, fill_value=0).tolist()

        values_2023 = get_month_data(df_2023)
        values_kh = get_month_data(df_kh)
        values_ck = get_month_data(df_ck)

        data_values = {"Năm 2023": values_2023,
                       "Kế hoạch giao": values_kh,
                       "Cùng kỳ năm 2022": values_ck}
        colors = {"Năm 2023": "#f1c40f", "Kế hoạch giao": "#2ecc71", "Cùng kỳ năm 2022": "#3498db"}

        fig, ax = plt.subplots(figsize=(12, 6))
        bar_width = 0.25
        index = np.arange(len(months))

        for i, (label, values) in enumerate(data_values.items()):
            ax.bar(index + i * bar_width, values, bar_width, label=label,
                   color=colors[label], edgecolor='black')
            for j, val in enumerate(values):
                ax.text(index[j] + i * bar_width, val + 0.1, str(val), ha='center', va='bottom', fontsize=12, fontweight='bold')

        ax.set_title("Lũy kế cùng kỳ năm 2022", fontsize=16, weight='bold', color='white')
        ax.set_xticks(index + bar_width)
        ax.set_xticklabels(months, fontsize=12)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_facecolor('#001f99')
        fig.patch.set_facecolor('#001f99')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.tick_params(axis='y', colors='white')
        ax.tick_params(axis='x', colors='white')
        ax.yaxis.label.set_color('white')
        ax.legend(loc='upper left', fontsize=12)

        st.pyplot(fig)

st.session_state.setdefault("dummy", 1)
