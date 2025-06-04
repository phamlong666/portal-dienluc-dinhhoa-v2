
import streamlit as st

# Cấu hình trang
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>Trung tâm điều hành số - phần mềm Điện lực Định Hóa</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 12px;'>Bản quyền © 2025 by Phạm Hồng Long & Brown Eyes</p>", unsafe_allow_html=True)

# Giao diện chính nếu chưa chọn gì
if "page" not in st.session_state:
    st.session_state["page"] = "main"

if st.session_state["page"] == "main":
    st.subheader("🌟 Chức năng chính")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.button("📦 Bigdata_Terabox", use_container_width=True)
    with col2:
        st.button("🤖 AI. PHẠM HỒNG LONG", use_container_width=True)
    with col3:
        st.button("🎞️ video tuyên truyền", use_container_width=True)
    with col4:
        st.button("📄 Báo cáo CMIS", use_container_width=True)
    with col5:
        if st.button("📊 TỔN THẤT", use_container_width=True):
            st.session_state["page"] = "ton_that"

# Giao diện tổn thất riêng
elif st.session_state["page"] == "ton_that":
    st.markdown("### 📊 PHÂN TÍCH TỔN THẤT TOÀN ĐƠN VỊ")
    if st.button("⬅️ Về trang chính"):
        st.session_state["page"] = "main"

    option = st.radio("Chọn phân tích", ["Toàn đơn vị", "Trung áp", "Hạ áp"], horizontal=True)

    if option == "Toàn đơn vị":
        st.success("🔍 Phân tích từ sheet: Đơn vị_Cấp điện áp")
        st.info("Chức năng đang được phát triển...")

    elif option == "Trung áp":
        st.success("🔍 Phân tích từ sheet: Tổn thất trung-hạ áp (Trung thế)")
        st.info("Chức năng đang được phát triển...")

    elif option == "Hạ áp":
        st.success("🔍 Phân tích từ sheet: Tổn thất trung-hạ áp (Hạ thế)")
        st.info("Chức năng đang được phát triển...")
