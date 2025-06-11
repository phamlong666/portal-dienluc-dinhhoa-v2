
import streamlit as st
import datetime

# ====== Điều hướng giữa các giao diện ======
tab = st.session_state.get("tab", "Trang chính")

if tab == "Trang chính":
    st.set_page_config(page_title="Trung tâm điều hành số - Điện lực Định Hóa", layout="wide")
    st.title("🌐 Trung tâm điều hành số – Điện lực Định Hóa")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🧾 Phục vụ họp", use_container_width=True):
            st.session_state["tab"] = "Phục vụ họp"
            st.rerun()
    with col2:
        st.link_button("📦 Dữ liệu lớn_Terabox", "https://terabox.com")
    with col3:
        st.link_button("💬 ChatGPT công khai", "https://chat.openai.com")
    with col4:
        st.link_button("📄 Báo cáo CMIS", "https://dropbox.com")

elif tab == "Phục vụ họp":
    st.header("🧾 Phục vụ họp – Ghi báo cáo và xuất file")
    if st.button("🔙 Quay về trang chính"):
        st.session_state["tab"] = "Trang chính"
        st.rerun()

    # --- Giao diện nhập cuộc họp ---
    ten = st.text_input("Tên cuộc họp")
    ngay = st.date_input("Ngày họp", value=datetime.date.today())
    nd = st.text_area("Nội dung cuộc họp", height=300)

    col1, col2, col3 = st.columns(3)

    if "lich_su" not in st.session_state:
        st.session_state["lich_su"] = []

    def save_lich_su():
        st.session_state["lich_su"].append(
            {"ten": ten, "ngay": ngay.strftime("%d/%m/%Y"), "nd": nd}
        )

    with col1:
        if st.button("📤 Tạo Word"):
            st.success("Tạo Word – placeholder")
            save_lich_su()
    with col2:
        if st.button("📽️ Tạo PowerPoint"):
            st.success("Tạo PPT – placeholder")
            save_lich_su()
    with col3:
        if st.button("📜 Lưu lịch sử"):
            save_lich_su()
            st.success("✅ Đã lưu")

    st.markdown("---")
    st.subheader("📚 Lịch sử cuộc họp đã lưu")
    for cuoc_hop in st.session_state["lich_su"]:
        st.markdown(f"📅 **{cuoc_hop['ngay']}** – `{cuoc_hop['ten']}`  
{cuoc_hop['nd']}")
