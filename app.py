
import streamlit as st
import pandas as pd
import os
from PIL import Image
from datetime import datetime

st.set_page_config(page_title="Phục vụ họp", layout="wide")

# ====== Nhập liệu ======
st.title("🧾 Phục vụ họp – Ghi báo cáo và xuất file")

ten = st.text_input("🔹 Tên cuộc họp")
ngay = st.date_input("📅 Ngày họp", value=pd.Timestamp.today())
gio = st.time_input("🕐 Giờ họp", value=pd.to_datetime("07:30").time())
nd = st.text_area("📝 Nội dung cuộc họp", height=250)
files = st.file_uploader("📎 Đính kèm tài liệu", accept_multiple_files=True)

# Tạo folder uploads nếu chưa có
upload_dir = "uploads"
os.makedirs(upload_dir, exist_ok=True)

def luu():
    saved_files = []
    if files:
        for file in files:
            file_path = os.path.join(upload_dir, file.name)
            with open(file_path, "wb") as f:
                f.write(file.read())
            saved_files.append(file_path)
    df = pd.DataFrame([{
        "Tên cuộc họp": ten,
        "Ngày": ngay.strftime("%d/%m/%Y"),
        "Giờ": gio.strftime("%H:%M"),
        "Nội dung": nd,
        "Tệp đính kèm": ", ".join(saved_files) if saved_files else ""
    }])
    if os.path.exists("lich_su_cuoc_hop.csv"):
        df.to_csv("lich_su_cuoc_hop.csv", mode="a", index=False, header=False, encoding="utf-8-sig")
    else:
        df.to_csv("lich_su_cuoc_hop.csv", index=False, encoding="utf-8-sig")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📤 Tạo Word"):
        st.success("✅ Đã tạo Word (demo)")
        luu()
with col2:
    if st.button("📽️ Tạo PowerPoint"):
        st.success("✅ Đã tạo PowerPoint (demo)")
        luu()
with col3:
    if st.button("📜 Lưu lịch sử"):
        luu()
        st.success("✅ Lịch sử cuộc họp đã được lưu")

# ====== Hiển thị lịch sử ======
st.markdown("---")
st.subheader("📚 Lịch sử cuộc họp đã được lưu")

if os.path.exists("lich_su_cuoc_hop.csv"):
    lich_su = pd.read_csv("lich_su_cuoc_hop.csv", encoding="utf-8-sig")
    new_rows = []
    for i, row in lich_su.iterrows():
        st.markdown(f"### 📅 {row['Ngày']} {row['Giờ']} – `{row['Tên cuộc họp']}`")
        st.markdown(f"{row['Nội dung']}")

        if pd.notna(row["Tệp đính kèm"]):
            for f in row["Tệp đính kèm"].split(", "):
                try:
                    if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                        st.image(f, width=300)
                    elif f.lower().endswith('.pdf'):
                        st.markdown(f'<iframe src="{f}" width="100%" height="400px"></iframe>', unsafe_allow_html=True)
                    else:
                        st.markdown(f"📎 [{os.path.basename(f)}]({f})")
                except:
                    st.warning(f"Không thể hiển thị file: {f}")

        # Nút xoá riêng từng dòng
        if st.button(f"🗑️ Xoá dòng {i+1}", key=f"xoa_{i}"):
            lich_su = lich_su.drop(i)
            lich_su.to_csv("lich_su_cuoc_hop.csv", index=False, encoding="utf-8-sig")
            st.warning("🗑️ Đã xoá một dòng lịch sử cuộc họp")
            st.experimental_rerun()

    if st.button("🗑️ Xoá toàn bộ lịch sử"):
        os.remove("lich_su_cuoc_hop.csv")
        st.warning("🗑️ Đã xoá toàn bộ lịch sử cuộc họp")
else:
    st.info("Chưa có lịch sử nào.")
