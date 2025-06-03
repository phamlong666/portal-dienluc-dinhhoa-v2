
import streamlit as st

st.set_page_config(page_title="Trung tâm điều hành số - phần mềm Điện lực Định Hóa", layout="wide")

# Sidebar navigation
st.sidebar.title("📚 Danh mục")
st.sidebar.markdown("- Báo cáo CMIS")
st.sidebar.markdown("- Tiến độ SCL")
st.sidebar.markdown("- Tổn thất TBA")
st.sidebar.markdown("- Phân tích tổn thất")
st.sidebar.markdown("- Dữ liệu Terabox")
st.sidebar.markdown("- Trợ lý ChatGPT")

# Header chào mừng
st.markdown("## Trung tâm điều hành số – phần mềm Điện lực Định Hóa")
st.success("Chào mừng bạn đến với Trung tâm điều hành số - Điện lực Định Hóa")

st.markdown("### 🌟 Các tính năng nổi bật:")
st.markdown("- Phân tích tổn thất, báo cáo kỹ thuật")
st.markdown("- Lưu trữ và truy xuất lịch sử GPT")
st.markdown("- Truy cập hệ thống nhanh chóng qua Sidebar")

st.info("✅ Mọi bản cập nhật hoặc chỉnh sửa Google Sheet đều tự động hiển thị!")

# Các nút chính mở ra liên kết
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<a href="https://docs.google.com/spreadsheets/d/1hGMkQxGyjees89cc7xw4fVjcXSot7916" target="_blank"><button style="width:100%">📄 Báo cáo CMIS</button></a>', unsafe_allow_html=True)

with col2:
    st.markdown('<a href="https://chat.openai.com/" target="_blank"><button style="width:100%">💬 ChatGPT công khai</button></a>', unsafe_allow_html=True)

with col3:
    st.markdown('<a href="https://www.youtube.com/@dienlucdinhhoa" target="_blank"><button style="width:100%">🎥 Các video</button></a>', unsafe_allow_html=True)

with col4:
    st.markdown('<a href="https://terabox.com/s/1cegqu7nP7rd0BdL_MIyrtA" target="_blank"><button style="width:100%;color:red;border:1px solid red;">📂 Dữ liệu lớn - Terabox</button></a>', unsafe_allow_html=True)

st.markdown("---")

# Trợ lý AI PHẠM HỒNG LONG – Có mã truy cập
st.markdown("### 🤖 Trợ lý riêng: AI PHẠM HỒNG LONG")
if "wrong_count" not in st.session_state:
    st.session_state.wrong_count = 0

user_code = st.text_input("🔐 Nhập mã truy cập", type="password")

if user_code:
    if user_code == "Abcde@12345":
        st.success("🎉 Chào bạn! Trợ lý Mắt Nâu đã sẵn sàng.")
        st.session_state.wrong_count = 0
        private_query = st.text_area("💬 Bạn muốn hỏi gì Mắt Nâu?")
        if private_query:
            st.info("🧠 Mắt Nâu đang phân tích và phản hồi...")
    else:
        st.session_state.wrong_count += 1
        st.error("❌ Sai mã truy cập.")

if st.session_state.wrong_count >= 3:
    st.markdown("🔑 **Bạn quên mã? Trả lời câu hỏi bảo mật sau:**")
    st.markdown("**❓ Người yêu anh tên là gì?** *(phân biệt hoa/thường)*")
    answer = st.text_input("💬 Trả lời:", type="password")
    if answer == "Mắt Nâu":
        st.success("✔️ Chính xác rồi! Mời nhập lại mã truy cập.")
        st.session_state.wrong_count = 0
