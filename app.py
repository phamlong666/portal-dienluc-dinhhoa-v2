
import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Trung tâm điều hành số", layout="wide")
if "page" not in st.session_state:
    st.session_state["page"] = "main"

def show_main():
    st.title("🌐 Trung tâm điều hành số – Điện lực Định Hóa")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🧾 Phục vụ họp", use_container_width=True):
            st.session_state["page"] = "phuc_vu_hop"
    with col2:
        st.link_button("📦 Bigdata_Terabox", "https://terabox.com")
    with col3:
        st.link_button("💬 ChatGPT công khai", "https://chat.openai.com")
    with col4:
        st.link_button("📄 Báo cáo CMIS", "https://dropbox.com")

def show_phuc_vu_hop():
    st.title("🧾 Phục vụ họp – Ghi báo cáo và xuất file")
    if st.button("🔙 Quay về trang chính"):
        st.session_state["page"] = "main"
        st.rerun()

    ten = st.text_input("🔹 Tên cuộc họp")
    ngay = st.date_input("📅 Ngày họp", value=datetime.date.today())
    gio = st.time_input("🕐 Giờ họp", value=datetime.time(7, 30))
    nd = st.text_area("📝 Nội dung cuộc họp", height=250)
    uploaded_files = st.file_uploader("📎 Đính kèm tài liệu", accept_multiple_files=True)

    def luu_lich_su():
        df = pd.DataFrame([{
            "Tên cuộc họp": ten,
            "Ngày": ngay.strftime("%d/%m/%Y"),
            "Giờ": gio.strftime("%H:%M"),
            "Nội dung": nd,
            "Tệp đính kèm": ", ".join([f.name for f in uploaded_files]) if uploaded_files else ""
        }])
        if os.path.exists("lich_su_cuoc_hop.csv"):
            df.to_csv("lich_su_cuoc_hop.csv", mode="a", index=False, header=False, encoding="utf-8-sig")
        else:
            df.to_csv("lich_su_cuoc_hop.csv", index=False, encoding="utf-8-sig")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📤 Tạo Word"):
            st.success("✅ Đã tạo Word (demo)")
            luu_lich_su()
    with col2:
        if st.button("📽️ Tạo PowerPoint"):
            st.success("✅ Đã tạo PowerPoint (demo)")
            luu_lich_su()
    with col3:
        if st.button("📜 Lưu lịch sử"):
            luu_lich_su()
            st.success("✅ Đã lưu vào file CSV")

    st.markdown("---")
    st.subheader("📚 Lịch sử cuộc họp đã lưu")
    if os.path.exists("lich_su_cuoc_hop.csv"):
        df_old = pd.read_csv("lich_su_cuoc_hop.csv", encoding="utf-8-sig")
        for _, row in df_old.iterrows():
            st.markdown(f"📅 **{row['Ngày']} {row['Giờ']}** – `{row['Tên cuộc họp']}`  <br>{row['Nội dung']}", unsafe_allow_html=True)
            if pd.notna(row["Tệp đính kèm"]):
                for f in row["Tệp đính kèm"].split(", "):
                    st.markdown(f"📎 {f}")
    else:
        st.info("Chưa có lịch sử nào được lưu.")

# Điều hướng giữa các trang
if st.session_state["page"] == "main":
    show_main()
elif st.session_state["page"] == "phuc_vu_hop":
    show_phuc_vu_hop()
