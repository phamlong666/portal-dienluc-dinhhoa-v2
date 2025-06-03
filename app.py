
import streamlit as st

st.set_page_config(page_title="Trung tâm điều hành số - phần mềm Điện lực Định Hóa", layout="wide")

# Logo EVN
st.image("https://upload.wikimedia.org/wikipedia/vi/thumb/0/08/LogoEVN.svg/1200px-LogoEVN.svg.png", width=80)

# Sidebar với các liên kết trỏ về đúng Google Sheet menu
st.sidebar.title("📚 Danh mục")
menu_link = "https://docs.google.com/spreadsheets/d/18kYr8DmDLnUUYzJJVHxzit5KCY286YozrrrIpOeojXI/edit?gid=0#gid=0"
st.sidebar.markdown(f"- [Báo cáo CMIS]({menu_link})")
st.sidebar.markdown(f"- [Tiến độ SCL]({menu_link})")
st.sidebar.markdown(f"- [Tổn thất TBA]({menu_link})")
st.sidebar.markdown(f"- [Phân tích tổn thất]({menu_link})")
st.sidebar.markdown(f"- [Dữ liệu Terabox]({menu_link})")
st.sidebar.markdown(f"- [Trợ lý ChatGPT]({menu_link})")

# Header
st.markdown("## Trung tâm điều hành số – phần mềm Điện lực Định Hóa")
st.success("Chào mừng bạn đến với Trung tâm điều hành số - Điện lực Định Hóa")

st.markdown("### 🌟 Các tính năng nổi bật:")
st.markdown("- Phân tích tổn thất, báo cáo kỹ thuật")
st.markdown("- Lưu trữ và truy xuất lịch sử GPT")
st.markdown("- Truy cập hệ thống nhanh chóng qua Sidebar")

st.info("✅ Mọi bản cập nhật hoặc chỉnh sửa Google Sheet đều tự động hiển thị!")

# Nút điều hướng chính với liên kết thực tế
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<a href="https://www.dropbox.com/home/3.%20Bao%20cao/4.%20B%C3%A1o%20c%C3%A1o%20CMIS" target="_blank"><button style="width:100%">📄 Báo cáo CMIS</button></a>', unsafe_allow_html=True)

with col2:
    st.markdown('<a href="https://chat.openai.com/" target="_blank"><button style="width:100%">💬 ChatGPT công khai</button></a>', unsafe_allow_html=True)

with col3:
    st.markdown('<a href="https://www.youtube.com/@dienlucdinhhoa" target="_blank"><button style="width:100%">🎥 Các video</button></a>', unsafe_allow_html=True)

with col4:
    st.markdown('<a href="https://terabox.com/s/1cegqu7nP7rd0BdL_MIyrtA" target="_blank"><button style="width:100%;color:red;border:1px solid red;">📂 Dữ liệu lớn - Terabox</button></a>', unsafe_allow_html=True)

# Nút AI riêng trỏ đúng giao diện
st.markdown('<br><a href="https://chatgpt.com/g/g-68348227b0c48191baa3145a2fbb3c41-ai-pham-hong-long" target="_blank"><button style="width:100%;background-color:#4CAF50;color:white;font-weight:bold">🧠 Trợ lý riêng: AI PHẠM HỒNG LONG</button></a>', unsafe_allow_html=True)
