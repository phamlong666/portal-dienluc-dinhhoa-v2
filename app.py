
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa", layout="wide")

if "view" not in st.session_state:
    st.session_state["view"] = "home"

# Sidebar lấy từ Google Sheet
sheet_url = "https://docs.google.com/spreadsheets/d/18kYr8DmDLnUUYzJJVHxzit5KCY286YozrrrIpOeojXI/gviz/tq?tqx=out:csv"
try:
    df = pd.read_csv(sheet_url)
    df = df[['Tên ứng dụng', 'Liên kết', 'Nhóm chức năng']].dropna()
    grouped = df.groupby('Nhóm chức năng')

    st.sidebar.markdown("<h3 style='color:#003399'>📚 Danh mục hệ thống</h3>", unsafe_allow_html=True)
    for group_name, group_data in grouped:
        with st.sidebar.expander(f"📂 {group_name}", expanded=False):
            for _, row in group_data.iterrows():
                label = row['Tên ứng dụng']
                link = row['Liên kết']
                st.markdown(f"""
                    <a href="{link}" target="_blank" class="sidebar-button">
                        🚀 {label}
                    </a>
                """, unsafe_allow_html=True)
except Exception as e:
    st.sidebar.error(f"🚫 Không thể tải menu từ Google Sheet. Lỗi: {e}")

# Style
st.markdown("""
    <style>
        section[data-testid="stSidebar"] > div:first-child {
            max-height: 95vh;
            overflow-y: auto;
        }
        .sidebar-button {
            display: block;
            background-color: #66a3ff;
            color: white;
            padding: 10px;
            border-radius: 8px;
            margin: 5px 0;
            font-weight: bold;
            box-shadow: 1px 1px 3px rgba(0,0,0,0.3);
            transition: all 0.2s ease-in-out;
            text-decoration: none;
        }
        .sidebar-button:hover {
            background-color: #3385ff !important;
            transform: translateY(-2px);
            box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
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

# Giao diện chính
if st.session_state["view"] == "home":
    st.info("""
👋 Chào mừng bạn đến với Trung tâm điều hành số - phần mềm Điện lực Định Hóa

📌 **Các tính năng nổi bật:**
- Phân tích tổn thất, báo cáo kỹ thuật
- Lưu trữ và truy xuất lịch sử GPT
- Truy cập hệ thống nhanh chóng qua Sidebar
""")
    st.markdown("""
    <div style="display: flex; justify-content: center; flex-wrap: wrap;">
        <a href="https://terabox.com/s/1cegqu7nP7rd0BdL_MIyrtA" target="_blank" class="main-button">📦 Bigdata_Terabox</a>
        <a href="https://chat.openai.com" target="_blank" class="main-button">💬 ChatGPT công khai</a>
        <a href="https://www.youtube.com/@dienlucdinhhoa" target="_blank" class="main-button">🎬 video tuyên truyền</a>
        <a href="https://www.dropbox.com/home/3.%20Bao%20cao/4.%20B%C3%A1o%20c%C3%A1o%20CMIS" target="_blank" class="main-button">📄 Báo cáo CMIS</a>
    </div>
    """, unsafe_allow_html=True)

    if st.button("📊 TỔN THẤT"):
        st.session_state["view"] = "ton_that"
        st.rerun()

# Giao diện tổn thất
elif st.session_state["view"] == "ton_that":
    st.markdown("## 📊 PHÂN TÍCH TỔN THẤT TOÀN ĐƠN VỊ")
    col1, col2 = st.columns(2)
    year = col1.selectbox("Chọn năm", list(range(2018, 2026)), index=7)
    month = col2.selectbox("Chọn tháng", list(range(1, 13)), index=4)

    data = pd.DataFrame({
        "Tháng": list(range(1, 13)),
        "Tỷ lệ tổn thất": [round(7.1 + (i % 4) * 0.3 + (year - 2021)*0.05, 2) for i in range(1, 13)]
    })

    with st.expander("📈 Biểu đồ tổn thất dạng line (zích zắc)", expanded=True):
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(data["Tháng"], data["Tỷ lệ tổn thất"], marker='o', linestyle='-', color="#007acc")
        ax.set_title(f"Tỷ lệ tổn thất năm {year}", fontsize=16)
        ax.set_xlabel("Tháng")
        ax.set_ylabel("Tỷ lệ tổn thất (%)")
        ax.grid(True)
        st.pyplot(fig)

    st.dataframe(data)
