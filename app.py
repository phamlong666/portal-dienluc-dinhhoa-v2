
import streamlit as st

st.set_page_config(page_title="Trung tâm điều hành số - EVNNPC Định Hóa", layout="wide")

st.markdown("## Trung tâm điều hành số – EVNNPC Điện lực Định Hóa")

# --- PHẦN 1: GIAO DIỆN CHÍNH (luôn hiển thị cho tất cả người dùng) ---
st.markdown("### 📊 Tra cứu và báo cáo dữ liệu điện lực")
st.markdown("- Tổn thất điện năng")
st.markdown("- Tiến độ SCL")
st.markdown("- Phân tích kỹ thuật, biểu đồ báo cáo...")
st.info("📝 Đây là phần hiển thị công khai – ai cũng có thể xem và thao tác.")

# --- PHẦN 2: Trợ lý AI PHẠM HỒNG LONG (ẩn nếu sai mã) ---
st.markdown("---")
st.markdown("### 🤖 Trợ lý AI PHẠM HỒNG LONG")

# Tạo bộ đếm sai
if "wrong_count" not in st.session_state:
    st.session_state.wrong_count = 0

# Nhập mã
user_code = st.text_input("🔐 Nhập mã truy cập để sử dụng trợ lý Mắt Nâu", type="password")

if user_code:
    if user_code == "Abcde@12345":
        st.success("✅ Xin chào anh Long! Trợ lý Mắt Nâu đã sẵn sàng.")
        st.session_state.wrong_count = 0
        query = st.text_area("💬 Anh muốn hỏi gì Mắt Nâu?")
        if query:
            st.info("📡 Mắt Nâu đang xử lý và phản hồi tại đây...")
    else:
        st.session_state.wrong_count += 1
        st.error("❌ Sai mã truy cập.")

# Câu hỏi bí mật nếu nhập sai 3 lần
if st.session_state.wrong_count >= 3:
    st.markdown("🔑 **Bạn quên mã? Hãy trả lời câu hỏi bảo mật**")
    st.markdown("**❓ Người yêu anh tên là gì?** *(phân biệt chữ hoa/thường)*")
    answer = st.text_input("💬 Trả lời:", type="password")
    if answer == "Mắt Nâu":
        st.success("🎉 Chính xác rồi anh Long! Mời nhập lại mã truy cập.")
        st.session_state.wrong_count = 0
