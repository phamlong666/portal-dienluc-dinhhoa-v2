
import streamlit as st

st.set_page_config(page_title="Trung tâm điều hành số - phần mềm Điện lực Định Hóa", layout="wide")

# Giao diện chào mừng
st.markdown("## Trung tâm điều hành số – phần mềm Điện lực Định Hóa")
st.success("Chào mừng anh Long đến với Trung tâm điều hành số - Điện lực Định Hóa")

st.markdown("### 🌟 Các tính năng nổi bật:")
st.markdown("- Phân tích thất bại, báo cáo kỹ thuật")
st.markdown("- Lưu trữ và truy xuất lịch sử GPT")
st.markdown("- Truy cập hệ thống nhanh chóng qua Sidebar")

st.info("✅ Mọi bản cập nhật hoặc chỉnh sửa Google Sheet đều tự động hiển thị!")

# Các nút lựa chọn chính
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.button("📄 Báo cáo CMIS")

with col2:
    if st.button("💬 ChatGPT công khai"):
        query = st.text_area("Hỏi gì đó ChatGPT (công khai)?")
        if query:
            st.info("🤖 GPT công khai trả lời tại đây...")

with col3:
    st.button("🎥 Các video")

with col4:
    st.button("🗂️ Dữ liệu lớn - Terabox")

# Divider
st.markdown("---")

# Trợ lý AI PHẠM HỒNG LONG (ẩn sau mã truy cập)
st.markdown("### 🤖 Trợ lý riêng: AI PHẠM HỒNG LONG")
if "wrong_count" not in st.session_state:
    st.session_state.wrong_count = 0

user_code = st.text_input("🔐 Nhập mã truy cập", type="password")

if user_code:
    if user_code == "Abcde@12345":
        st.success("🎉 Chào anh Long! Trợ lý Mắt Nâu sẵn sàng.")
        st.session_state.wrong_count = 0
        private_query = st.text_area("💬 Anh muốn hỏi gì Mắt Nâu?")
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
