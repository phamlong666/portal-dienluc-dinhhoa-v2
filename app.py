
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa", layout="wide")

if "view" not in st.session_state:
    st.session_state["view"] = "home"

# Style
st.markdown("""
    <style>
        section[data-testid="stSidebar"] > div:first-child {
            max-height: 95vh;
            overflow-y: auto;
        }

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
    </div>
    """, unsafe_allow_html=True)

    if st.button("📊 TỔN THẤT", key="btn-ton-that"):
        st.session_state["view"] = "ton_that"

# Giao diện phân tích tổn thất
elif st.session_state["view"] == "ton_that":
    st.markdown("## 📊 PHÂN TÍCH TỔN THẤT TOÀN ĐƠN VỊ")

    col1, col2 = st.columns(2)
    month = col1.selectbox("Chọn tháng", list(range(1, 13)))
    year = col2.selectbox("Chọn năm", list(range(2018, 2026)))

    data = pd.DataFrame({
        "Tháng": list(range(1, 13)),
        "Tỷ lệ tổn thất": [round(7.5 + (i % 4) * 0.3 + (year - 2020) * 0.05, 2) for i in range(12)]
    })

    fig, ax = plt.subplots()
    ax.plot(data["Tháng"], data["Tỷ lệ tổn thất"], marker='o')
    ax.set_title(f"Tỷ lệ tổn thất năm {year}")
    ax.set_xlabel("Tháng")
    ax.set_ylabel("Tỷ lệ tổn thất (%)")
    st.pyplot(fig)

    st.markdown("### 📊 Bảng dữ liệu tổn thất")
    st.dataframe(data)

    if st.button("📥 Xuất báo cáo PDF"):
        st.success("✅ Đã chuẩn bị xuất PDF (chức năng sẽ tích hợp sau).")
