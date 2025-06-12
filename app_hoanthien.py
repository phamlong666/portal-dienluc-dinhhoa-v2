
import streamlit as st
import datetime

# Sidebar menu lựa chọn
menu_options = ["Trang chính", "Phục vụ họp"]
selected = st.sidebar.selectbox("Chọn chức năng", menu_options)

if selected == "Trang chính":
    st.title("🌐 Trung tâm điều hành số – Điện lực Định Hóa")
    st.markdown("Chào mừng bạn đến với hệ thống điều hành số.")


elif selected == "Phục vụ họp":
    st.markdown("## 🧾 Phục vụ họp – Ghi báo cáo, xuất file, và nhắc việc")

    if "lich_su" not in st.session_state:
        st.session_state["lich_su"] = []

    col1, col2 = st.columns([3, 1])
    with col1:
        ten = st.text_input("🔹 Tên cuộc họp")
        ngay = st.date_input("📅 Ngày họp", value=datetime.date.today())
        gio = st.time_input("🕐 Giờ bắt đầu", value=datetime.time(7, 30))
        nd = st.text_area("📝 Nội dung cuộc họp", height=250)

        uploaded_files = st.file_uploader("📎 Đính kèm tài liệu (nhiều định dạng)", accept_multiple_files=True)

        def save_lich_su():
            st.session_state["lich_su"].append({
                "ten": ten,
                "ngay": ngay.strftime("%d/%m/%Y"),
                "gio": gio.strftime("%H:%M"),
                "nd": nd,
                "files": [f.name for f in uploaded_files]
            })

        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("📤 Tạo Word"):
                save_lich_su()
                st.success("✅ Word đã tạo (tạm thời chưa xuất file)")
        with b2:
            if st.button("📽️ Tạo PowerPoint"):
                save_lich_su()
                st.success("✅ PowerPoint đã tạo (placeholder)")
        with b3:
            if st.button("📜 Lưu lịch sử"):
                save_lich_su()
                st.success("✅ Đã lưu vào lịch sử")

        st.markdown("---")
        st.subheader("📚 Lịch sử cuộc họp đã lưu")
        for cuoc_hop in st.session_state["lich_su"]:
            st.markdown(f"📅 **{cuoc_hop['ngay']} {cuoc_hop['gio']}** – `{cuoc_hop['ten']}`  
{cuoc_hop['nd']}")
            if cuoc_hop["files"]:
                for f in cuoc_hop["files"]:
                    st.markdown(f"📎 {f}")

    with col2:
        st.info("⏰ Tính năng 'Nhắc việc' sẽ sớm cập nhật qua email: phamlong666@gmail.com")
