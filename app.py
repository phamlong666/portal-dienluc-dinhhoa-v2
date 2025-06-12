import streamlit as st
import pandas as pd
import os

UPLOAD_FOLDER = "uploads"
CSV_FILE = "lich_su_cuoc_hop.csv"

# Đảm bảo thư mục upload tồn tại
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load dữ liệu lịch sử cuộc họp
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Ngày", "Giờ", "Tên cuộc họp", "Nội dung", "File đính kèm"])

df = load_data()

# 📚 Hiển thị lịch sử cuộc họp
st.subheader("📚 Lịch sử cuộc họp")
if not df.empty:
    for idx, row in df.iterrows():
        if all(k in row for k in ["Ngày", "Giờ", "Tên cuộc họp"]):
            with st.expander(f"📅 {row['Ngày']} {row['Giờ']} – {row['Tên cuộc họp']}"):
                st.markdown(row["Nội dung"])

                # Xem file đính kèm nếu có
                files = str(row.get("File đính kèm", "")).split(";")
                for file in files:
                    file = file.strip()
                    if file:
                        file_path = os.path.join(UPLOAD_FOLDER, file)
                        if os.path.exists(file_path):
                            with open(file_path, "rb") as f:
                                st.download_button(
                                    label=f"📥 Tải {file}",
                                    data=f.read(),
                                    file_name=file
                                )

                # Nút Xóa
                if st.button(f"🗑️ Xóa dòng {idx}", key=f"xoa_{idx}"):
                    df.drop(index=idx, inplace=True)
                    df.to_csv(CSV_FILE, index=False)
                    st.experimental_rerun()