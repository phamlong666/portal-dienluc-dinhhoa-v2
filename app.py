
import streamlit as st

st.set_page_config(page_title="Trung tâm điều hành số - EVNNPC Định Hóa", layout="wide")
st.markdown("## Trung tâm điều hành số – EVNNPC Điện lực Định Hóa")

# Tạo bộ đếm sai
if "wrong_count" not in st.session_state:
    st.session_state.wrong_count = 0

# Nhập mã truy cập
user_code = st.text_input("🔐 Nhập mã truy cập trợ lý PHẠM HỒNG LONG", type="password")

# Kiểm tra mã
if user_code:
    if user_code == "Abcde@12345":
        st.success("✅ Xin chào anh Long! Trợ lý Mắt Nâu đã sẵn sàng.")
        st.session_state.wrong_count = 0
        query = st.text_area("🧠 Anh muốn hỏi gì Mắt Nâu?")
        if query:
            st.info("💬 Mắt Nâu sẽ phân tích và trả lời tại đây...")
            # Gọi GPT, sinh báo cáo...
    else:
        st.session_state.wrong_count += 1
        st.error("❌ Sai mã. Vui lòng thử lại.")

# Gợi ý khi sai >= 3 lần
if st.session_state.wrong_count >= 3:
    st.markdown("🔑 **Bạn quên mã truy cập?**")
    st.markdown("**❓ Người yêu anh tên là gì?** *(phân biệt chữ hoa/thường)*")
    answer = st.text_input("💬 Trả lời câu hỏi bảo mật:", type="password")
    if answer == "Mắt Nâu":
        st.success("🎉 Chính xác rồi anh Long! Em vẫn luôn ở đây...")
        st.session_state.wrong_count = 0
