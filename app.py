
import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Trung tâm điều hành số", layout="wide")
menu_options = ["Trang chính", "Phục vụ họp"]
selected = st.sidebar.selectbox("Chọn chức năng", menu_options)

if selected == "Trang chính":
    st.title("🌐 Trung tâm điều hành số – Điện lực Định Hóa")
    st.markdown("Chào mừng bạn đến với hệ thống điều hành số.")

elif selected == "Phục vụ họp":
    st.title("🧾 Phục vụ họp – Ghi báo cáo và xuất file")

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
            st.markdown(f"📅 **{row['Ngày']} {row['Giờ']}** – `{row['Tên cuộc họp']}`  
{row['Nội dung']}")
            if pd.notna(row["Tệp đính kèm"]):
                for f in row["Tệp đính kèm"].split(", "):
                    st.markdown(f"📎 {f}")
    else:
        st.info("Chưa có lịch sử nào được lưu.")
