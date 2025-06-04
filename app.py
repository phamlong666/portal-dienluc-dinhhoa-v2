
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa", layout="wide")

if "view" not in st.session_state:
    st.session_state["view"] = "home"

# Lấy query param nếu có
params = st.query_params
if params.get("view") == ["ton_that"]:
    st.session_state["view"] = "ton_that"

# Sidebar từ Google Sheet
st.sidebar.markdown("## 📁 Menu chức năng")
try:
    menu_link = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSErV8WZ7kq-3BT7i77tbmTuWqfYgEZtV-kPjJvHgS0eYknUPoEK9hruXNWPE5_EBT02TrdDIW0a4NW/pub?output=csv"
    df_menu = pd.read_csv(menu_link)
    if "E" in df_menu.columns:
        for item in df_menu["E"].dropna():
            st.sidebar.markdown(f"- {item}")
    else:
        st.sidebar.warning("⚠️ Không tìm thấy cột E trong Google Sheet.")
except Exception as e:
    st.sidebar.warning(f"⚠️ Không thể tải menu: {e}")

# Style nút chính
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

# Header logo
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

# Giao diện chính
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

# Giao diện tổn thất tách riêng
elif st.session_state["view"] == "ton_that":
    st.markdown("## 📊 PHÂN TÍCH TỔN THẤT TOÀN ĐƠN VỊ")

    mode = st.radio("Hiển thị dữ liệu:", ["Tháng", "Lũy kế"], horizontal=True)

    col1, col2 = st.columns(2)
    year = col1.selectbox("Chọn năm", list(range(2018, 2026)), index=7)
    month = col2.selectbox("Chọn tháng", list(range(1, 13)), index=4)

    # Dữ liệu mẫu
    if mode == "Tháng":
        data = pd.DataFrame({
            "STT": list(range(1, 13)),
            "Tháng": [f"Tháng {i}" for i in range(1, 13)],
            "Tỷ lệ tổn thất (%)": [round(7.1 + (i % 4) * 0.3 + (year - 2021)*0.05, 2) for i in range(1, 13)]
        })
    else:
        data = pd.DataFrame({
            "STT": [1],
            "Tháng": [f"Lũy kế đến tháng {month}"],
            "Tỷ lệ tổn thất (%)": [round(7.8 + (year - 2021) * 0.1, 2)]
        })

    with st.expander("📈 Biểu đồ tổn thất", expanded=True):
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(data["Tháng"], data["Tỷ lệ tổn thất (%)"], color="#3399FF")
        ax.set_title(f"Tỷ lệ tổn thất năm {year}")
        ax.set_ylabel("Tỷ lệ tổn thất (%)")
        st.pyplot(fig, use_container_width=True)

    st.dataframe(data, use_container_width=True)

    if st.button("📥 Xuất báo cáo PDF"):
        st.success("✅ Đang phát triển chức năng xuất PDF.")
