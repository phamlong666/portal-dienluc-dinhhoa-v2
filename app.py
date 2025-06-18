
import streamlit as st
import pandas as pd
import os
import io
from datetime import date, time, datetime
from PIL import Image

st.set_page_config(page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa", layout="wide")

# ===== FILE LƯU DỮ LIỆU =====
REMINDERS_FILE = "nhac_viec.csv"
MEETINGS_FILE = "lich_su_cuoc_hop.csv"
UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

EMAIL_MAC_DINH = "phamlong666@gmail.com"

# ===== NÚT NHẮC VIỆC =====
st.header("⏰ Nhắc việc")

# Tạo mới danh sách
if st.button("🆕 Tạo mới danh sách nhắc việc"):
    df = pd.DataFrame(columns=["Việc", "Ngày", "Giờ", "Email"])
    df.to_csv(REMINDERS_FILE, index=False)
    st.success("✅ Đã khởi tạo danh sách.")

# Thêm việc
with st.expander("➕ Thêm việc cần nhắc"):
    with st.form("form_nhac"):
        viec = st.text_input("🔔 Việc cần nhắc")
        ngay = st.date_input("📅 Ngày", date.today())
        gio = st.time_input("⏰ Giờ", time(7, 30))
        email = st.text_input("📧 Gửi tới", value=EMAIL_MAC_DINH)
        submit = st.form_submit_button("📌 Tạo nhắc việc")
    if submit:
        new_row = {
            "Việc": viec,
            "Ngày": ngay.strftime("%d/%m/%y"),
            "Giờ": gio.strftime("%H:%M"),
            "Email": email
        }
        df = pd.read_csv(REMINDERS_FILE) if os.path.exists(REMINDERS_FILE) else pd.DataFrame()
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(REMINDERS_FILE, index=False)
        st.success("✅ Đã tạo nhắc việc.")

# Hiển thị & xóa
if os.path.exists(REMINDERS_FILE):
    st.subheader("📋 Danh sách nhắc việc")
    try:
        df = pd.read_csv(REMINDERS_FILE, dtype=str)
        for idx, row in df.iterrows():
            col1, col2 = st.columns([6,1])
            with col1:
                st.write(f"📌 **{row['Việc']}** lúc {row['Giờ']} ngày {row['Ngày']} → {row['Email']}")
            with col2:
                if st.button("❌", key=f"xoa_{idx}"):
                    df.drop(index=idx, inplace=True)
                    df.to_csv(REMINDERS_FILE, index=False)
                    st.rerun()
    except Exception as e:
        st.error(f"❌ Lỗi khi hiển thị nhắc việc: {e}")

# Xuất / Nhập Excel
st.markdown("### 📤 Xuất / Nhập Excel (Nhắc việc)")
col1, col2 = st.columns(2)

with col1:
    if os.path.exists(REMINDERS_FILE):
        df_export = pd.read_csv(REMINDERS_FILE)
        towrite = io.BytesIO()
        with pd.ExcelWriter(towrite, engine='xlsxwriter') as writer:
            df_export.to_excel(writer, index=False, sheet_name='NhacViec')
        st.download_button("📥 Tải Excel", data=towrite.getvalue(), file_name="nhac_viec.xlsx")

with col2:
    file = st.file_uploader("📂 Nhập từ Excel", type=["xlsx"], key="upload_nhacviec")
    if file:
        try:
            df = pd.read_excel(file, dtype=str)
            # Chuẩn hoá ngày giờ nếu có thể
            df["Ngày"] = pd.to_datetime(df["Ngày"], errors="coerce").dt.strftime("%d/%m/%y")
            df["Giờ"] = df["Giờ"].fillna("00:00")
            df.to_csv(REMINDERS_FILE, index=False)
            st.success("✅ Đã nhập lại danh sách.")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Lỗi khi nhập file Excel: {e}")

# ===== NÚT PHỤC VỤ HỌP =====
st.header("📑 Phục vụ họp")

with st.expander("➕ Thêm cuộc họp mới"):
    with st.form("form_hop"):
        ten = st.text_input("📌 Tên cuộc họp")
        ngay = st.date_input("📅 Ngày họp")
        gio = st.time_input("⏰ Giờ họp", time(8, 0))
        noidung = st.text_area("📝 Nội dung")
        files = st.file_uploader("📎 Đính kèm", accept_multiple_files=True)
        submit = st.form_submit_button("💾 Lưu cuộc họp")
    if submit:
        try:
            file_names = []
            for f in files:
                file_path = os.path.join(UPLOAD_FOLDER, f.name)
                with open(file_path, "wb") as out:
                    out.write(f.read())
                file_names.append(f.name)
            new_row = {
                "Ngày": ngay.strftime("%d/%m/%y"),
                "Giờ": gio.strftime("%H:%M"),
                "Tên cuộc họp": ten,
                "Nội dung": noidung,
                "Tệp": ";".join(file_names)
            }
            df = pd.read_csv(MEETINGS_FILE) if os.path.exists(MEETINGS_FILE) else pd.DataFrame()
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(MEETINGS_FILE, index=False)
            st.success("✅ Đã lưu cuộc họp.")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Lỗi khi lưu cuộc họp: {e}")

# Hiển thị & Xoá họp
if os.path.exists(MEETINGS_FILE):
    st.subheader("📚 Danh sách cuộc họp")
    try:
        df = pd.read_csv(MEETINGS_FILE)
        for idx, row in df.iterrows():
            with st.expander(f"📌 {row['Tên cuộc họp']} – {row['Ngày']} {row['Giờ']}"):
                st.write("📝", row["Nội dung"])
                file_list = str(row.get("Tệp", "")).split(";")
                for file in file_list:
                    file_path = os.path.join(UPLOAD_FOLDER, file)
                    if os.path.exists(file_path):
                        st.write(f"📎 {file}")
                        with open(file_path, "rb") as f:
                            st.download_button("⬇️ Tải", f.read(), file_name=file, key=f"{file}_{idx}")
                with st.form(f"form_xoa_{idx}"):
                    confirm = st.checkbox("🗑️ Xóa", key=f"xoa_ck_{idx}")
                    do_delete = st.form_submit_button("❗ Xác nhận")
                    if confirm and do_delete:
                        df.drop(index=idx, inplace=True)
                        df.to_csv(MEETINGS_FILE, index=False)
                        st.success("🗑️ Đã xoá.")
                        st.rerun()
    except Exception as e:
        st.error(f"❌ Lỗi khi hiển thị cuộc họp: {e}")

# Xuất / Nhập Excel
st.markdown("### 📤 Xuất / Nhập Excel (Phục vụ họp)")
col3, col4 = st.columns(2)

with col3:
    if os.path.exists(MEETINGS_FILE):
        df_export = pd.read_csv(MEETINGS_FILE)
        towrite2 = io.BytesIO()
        with pd.ExcelWriter(towrite2, engine='xlsxwriter') as writer:
            df_export.to_excel(writer, index=False, sheet_name='CuocHop')
        st.download_button("📥 Tải Excel", data=towrite2.getvalue(), file_name="phuc_vu_hop.xlsx")

with col4:
    file = st.file_uploader("📂 Nhập từ Excel", type=["xlsx"], key="upload_hop")
    if file:
        try:
            df = pd.read_excel(file, dtype=str)
            df.to_csv(MEETINGS_FILE, index=False)
            st.success("✅ Đã nhập lại danh sách.")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Lỗi khi nhập file Excel: {e}")
