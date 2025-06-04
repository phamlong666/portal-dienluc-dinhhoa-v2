
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

st.set_page_config(page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa", layout="wide")

if "view" not in st.session_state:
    st.session_state["view"] = "home"

sheet_url = "https://docs.google.com/spreadsheets/d/18kYr8DmDLnUUYzJJVHxzit5KCY286YozrrrIpOeojXI/gviz/tq?tqx=out:csv"
try:
    df = pd.read_csv(sheet_url)
    df = df[['Tên ứng dụng', 'Liên kết', 'Nhóm chức năng']].dropna()
    grouped = df.groupby('Nhóm chức năng')
    st.sidebar.markdown("<h3 style='color:#003399'>📚 Danh mục hệ thống</h3>", unsafe_allow_html=True)
    for group_name, group_data in grouped:
        with st.sidebar.expander(f"📂 {group_name}", expanded=False):
            for _, row in group_data.iterrows():
                st.markdown(f"<a href='{row['Liên kết']}' target='_blank' class='sidebar-button'>🚀 {row['Tên ứng dụng']}</a>", unsafe_allow_html=True)
except Exception as e:
    st.sidebar.error(f"🚫 Không thể tải menu: {e}")

st.markdown("""
    <style>
        .sidebar-button {
            display: block;
            background-color: #66a3ff;
            color: white;
            padding: 10px;
            border-radius: 8px;
            margin: 5px 0;
            font-weight: bold;
            text-decoration: none;
        }
        .main-button {
            background-color: #66a3ff;
            color: white;
            padding: 20px 30px;
            border-radius: 14px;
            font-weight: bold;
            font-size: 24px;
            margin: 14px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            text-decoration: none;
            width: 100%;
        }
        .main-button:hover {
            transform: scale(1.07);
            background-color: #3399ff;
        }
        div[data-testid="column"] div:has(button) {
            display: flex;
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([1, 10])
with col1:
    try:
        logo = Image.open("assets/logo_hinh_tron_hoan_chinh.png")
        st.image(logo, width=70)
    except:
        st.warning("⚠️ Không tìm thấy logo.")
with col2:
    st.markdown("""
        <h1 style='color:#003399; font-size:42px; margin-top:18px;'>
        Trung tâm điều hành số - phần mềm Điện lực Định Hóa
        </h1>
        <p style='font-size:13px; color:gray;'>Bản quyền © 2025 by Phạm Hồng Long & Brown Eyes</p>
    """, unsafe_allow_html=True)

# Trang chính
if st.session_state["view"] == "home":
    st.markdown("### 🌟 Chức năng chính")
    colA, colB, colC, colD, colE = st.columns(5)
    with colA:
        st.markdown('<a href="https://terabox.com/s/1cegqu7nP7rd0BdL_MIyrtA" target="_blank"><button class="main-button">📦 Bigdata_Terabox</button></a>', unsafe_allow_html=True)
    with colB:
        st.markdown('<a href="https://chat.openai.com" target="_blank"><button class="main-button">💬 ChatGPT công khai</button></a>', unsafe_allow_html=True)
    with colC:
        st.markdown('<a href="https://www.youtube.com/@dienlucdinhhoa" target="_blank"><button class="main-button">🎬 video tuyên truyền</button></a>', unsafe_allow_html=True)
    with colD:
        st.markdown('<a href="https://www.dropbox.com/home/3.%20Bao%20cao/4.%20B%C3%A1o%20c%C3%A1o%20CMIS" target="_blank"><button class="main-button">📄 Báo cáo CMIS</button></a>', unsafe_allow_html=True)
    with colE:
        if st.button("📊 TỔN THẤT"):
            st.session_state["view"] = "ton_that"
            st.rerun()

# Trang tổn thất
elif st.session_state["view"] == "ton_that":
    st.markdown("🔙 [Quay về trang chính](#)", unsafe_allow_html=True)
    st.markdown("## 📊 PHÂN TÍCH TỔN THẤT")

    tab1, tab2, tab3 = st.tabs(["Tổn thất toàn đơn vị", "Tổn thất trung áp", "Tổn thất hạ áp"])

    def show_chart(view_name):
        col1, col2 = st.columns(2)
        year = col1.selectbox(f"{view_name} - Chọn năm", list(range(2018, 2026)), index=7)
        max_month = 5 if year == 2025 else 12
        month = col2.selectbox(f"{view_name} - Chọn tháng", list(range(1, max_month + 1)), index=max_month - 1)

        months = list(range(1, 13))
        values_now = [round(6 + np.random.rand() * 3, 2) if i <= max_month else None for i in months]
        values_last = [round(6 + np.random.rand() * 3, 2) for i in months]

        df = pd.DataFrame({
            "Tháng": months,
            "Tỷ lệ tổn thất": values_now,
            "Cùng kỳ năm trước": values_last
        })

        fig, ax = plt.subplots(figsize=(4.5, 1.5))
        ax.plot(months, values_now, marker='o', label=f"Năm {year}", linewidth=2)
        ax.plot(months, values_last, marker='s', label=f"Năm {year-1}", linewidth=2, color='gray')
        ax.set_xticks(months)
        ax.set_xlabel("Tháng")
        ax.set_ylabel("Tỷ lệ tổn thất (%)")
        ax.set_title(f"Tỷ lệ tổn thất năm {year}", pad=10)
        ax.grid(True)
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.12), ncol=2)
        st.pyplot(fig)

        st.dataframe(df.style.format({"Tỷ lệ tổn thất": "{:.2f}", "Cùng kỳ năm trước": "{:.2f}"}), use_container_width=True)

    with tab1:
        show_chart("Toàn đơn vị")
    with tab2:
        show_chart("Trung áp")
    with tab3:
        show_chart("Hạ áp")
