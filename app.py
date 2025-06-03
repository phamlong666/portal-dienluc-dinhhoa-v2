
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide", page_title="Trung tâm điều hành số - phần mềm Điện lực Định Hóa")

# === SIDEBAR DANH MỤC HỆ THỐNG ===
with st.sidebar:
    st.markdown("## 📚 Danh mục hệ thống")
    selected = option_menu(
        menu_title=None,
        options=[
            "An toàn", "An toàn, điều độ", "Báo cáo", "Công nghệ thông tin",
            "Kinh doanh", "Kỹ thuật", "Quản trị nội bộ", "Thiên tai - cứu nạn", "Điều chỉnh độ"
        ],
        icons=["folder"] * 9,
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f0f2f6"},
            "icon": {"color": "blue", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "4px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#cfe2ff", "font-weight": "bold"},
        }
    )

# === HEADER CHÍNH VÀ LOGO ===
col_logo, col_title = st.columns([1, 9])
with col_logo:
    st.image("https://i.imgur.com/EK9V7i6.png", width=80)
with col_title:
    st.markdown("<h1 style='color:#003399;'>Trung tâm điều hành số – phần mềm Điện lực Định Hóa</h1>", unsafe_allow_html=True)
    st.caption("Bản quyền © 2025 by Phạm Hồng Long & Brown Eyes")

# === GIỚI THIỆU VÀ TÍNH NĂNG ===
with st.container():
    st.success("👋 Chào mừng bạn đến với Trung tâm điều hành số - phần mềm Điện lực Định Hóa")
    st.markdown("""
    ### ✨ Các tính năng nổi bật:
    - 📊 Phân tích tổn thất, báo cáo kỹ thuật
    - 📁 Lưu trữ và truy xuất lịch sử GPT
    - 🧭 Truy cập hệ thống nhanh chóng qua Sidebar
    """)
    st.info("✅ Mọi bản cập nhật hoặc chỉ cần chỉnh sửa Google Sheet đều tự động hiển thị!")

# === NÚT CHÍNH DƯỚI TRANG ===
st.markdown("### ")
col1, col2, col3, col4 = st.columns(4)
button_style = "display:inline-block;background-color:#003399;padding:1em 1em;border-radius:12px;color:white;text-align:center;font-weight:bold;text-decoration:none;font-size:16px;width:100%"

with col1:
    st.markdown(f'<a href="https://terabox.com/s/1cegqu7nP7rd0BdL_MIyrtA" target="_blank" style="{button_style}">📦 Dữ liệu lớn_Terabox</a>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<a href="https://chat.openai.com" target="_blank" style="{button_style}">💬 ChatGPT công khai</a>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<a href="https://www.youtube.com/@dienlucdinhhoa" target="_blank" style="{button_style}">🎬 video tuyên truyền</a>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<a href="https://www.dropbox.com/home/3.%20Bao%20cao/4.%20B%C3%A1o%20c%C3%A1o%20CMIS" target="_blank" style="{button_style}">📄 Báo cáo CMIS</a>', unsafe_allow_html=True)
