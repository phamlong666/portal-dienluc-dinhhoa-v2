
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# ----------------- CONFIG -------------------
st.set_page_config(page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa", layout="wide")

if "view" not in st.session_state:
    st.session_state["view"] = "home"

# ----------------- SIDEBAR -------------------
# Menu lấy từ Google Sheet cột E
st.sidebar.markdown("## 📁 Menu chức năng")
try:
    menu_link = "https://docs.google.com/spreadsheets/d/18kYr8DmDLnUUYzJJVHxzit5KCY286YozrrrIpOeojXI/export?format=csv"
    df_menu = pd.read_csv(menu_link)
    for item in df_menu["E"].dropna():
        st.sidebar.markdown(f"- {item}")
except:
    st.sidebar.warning("⚠️ Không thể tải menu từ Google Sheet.")

# ----------------- HEADER -------------------
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

# ----------------- STYLE NÚT CHÍNH -------------------
st.markdown("""
    <style>
        .main-button {
            display: inline-block;
            background-color: #66a3ff;
            color: white;
            text-align: center;
            padding: 22px 30px;
            border-radius: 14px;
            font-weight: bold;
            text-decoration: none;
            margin: 14px;
            transition: 0.3s;
            font-size: 24px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        }
        .main-button:hover {
            transform: scale(1.07);
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        }
    </style>
""", unsafe_allow_html=True)

# ----------------- GIAO DIỆN CHÍNH -------------------
params = st.query_params
if params.get("view") == ["ton_that"]:
    st.session_state["view"] = "ton_that"

if st.session_state["view"] == "home":
    st.markdown("""
    <div style="display: flex; justify-content: center; flex-wrap: wrap;">
        <a href="https://terabox.com/s/1cegqu7nP7rd0BdL_MIyrtA" target="_blank" class="main-button">📦 Bigdata_Terabox</a>
        <a href="https://chat.openai.com" target="_blank" class="main-button">💬 ChatGPT công khai</a>
        <a href="https://www.youtube.com/@dienlucdinhhoa" target="_blank" class="main-button">🎬 video tuyên truyền</a>
        <a href="https://www.dropbox.com/home/3.%20Bao%20cao/4.%20B%C3%A1o%20c%C3%A1o%20CMIS" target="_blank" class="main-button">📄 Báo cáo CMIS</a>
        <a href="?view=ton_that" class="main-button">📊 TỔN THẤT</a>
    </div>
    """, unsafe_allow_html=True)

# ----------------- GIAO DIỆN TỔN THẤT -------------------
elif st.session_state["view"] == "ton_that":
    st.markdown("## 📊 PHÂN TÍCH TỔN THẤT")

    tab1, tab2, tab3 = st.tabs(["📊 Toàn đơn vị", "⚡ Trung áp", "🔌 Hạ áp"])

    with tab1:
        col1, col2 = st.columns(2)
        month = col1.selectbox("Chọn tháng", list(range(1, 13)), index=4)
        year = col2.selectbox("Chọn năm", list(range(2018, 2026)), index=7)
        data = pd.DataFrame({
            "Tháng": list(range(1, 13)),
            "Tỷ lệ tổn thất": [round(7.2 + (i % 4) * 0.25 + (year - 2020) * 0.05, 2) for i in range(12)]
        })
        st.line_chart(data.set_index("Tháng"))
        st.dataframe(data)
        if st.button("📥 Xuất PDF", key="export1"):
            st.success("✅ Sẽ tích hợp chức năng xuất PDF sau.")

    with tab2:
        st.info("🔧 Đang phát triển tính năng tổn thất trung áp...")

    with tab3:
        st.info("🔧 Đang phát triển tính năng tổn thất hạ áp...")
