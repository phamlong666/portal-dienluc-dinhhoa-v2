from pathlib import Path
import streamlit as st
st.set_page_config(page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa", layout="wide")

import streamlit as st
import pandas as pd
from PIL import Image
import datetime

# ================== CUSTOM CSS ==================
st.markdown("""
    <style>
        section[data-testid="stSidebar"] > div:first-child {
            max-height: 95vh;
            overflow-y: auto;
        }
        .sidebar-button {
            display: block;
            background-color: #42A5F5;
            color: white;
            padding: 10px;
            border-radius: 8px;
            margin: 5px 0;
            font-weight: bold;
            box-shadow: 1px 1px 3px rgba(0,0,0,0.3);
            transition: all 0.2s ease-in-out;
            text-decoration: none;
        }
        .sidebar-button:hover {
            background-color: #1E88E5 !important;
            transform: translateY(-2px);
            box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
        }
        .main-button {
            display: inline-block;
            background-color: #FFCC80;
            color: white;
            text-align: center;
            padding: 22px 30px;
            border-radius: 14px;
            font-weight: bold;
            text-decoration: none;
            margin: 14px;
            transition: 0.3s;
            font-size: 24px;
        }
        .main-button:hover {
            transform: scale(1.05);
            box-shadow: 3px 3px 12px rgba(0,0,0,0.3);
        }
    </style>
""", unsafe_allow_html=True)

# ================== HEADER ==================
col1, col2 = st.columns([1, 10])
with col1:
    try:
        logo = Image.open("assets/logo_hinh_tron_hoan_chinh.png")
        st.image(logo, width=70)
    except:
        st.warning("⚠️ Không tìm thấy logo.")

with col2:
    st.markdown("""
        <h1 style='color:#003399; font-size:42px; margin-top:18px;'>
        Trung tâm điều hành số - phần mềm Điện lực Định Hóa
        </h1>
        <p style='font-size:13px; color:gray;'>Bản quyền © 2025 by Phạm Hồng Long & Brown Eyes</p>
    """, unsafe_allow_html=True)

# ================== MENU TỪ GOOGLE SHEET ==================
sheet_url = "https://docs.google.com/spreadsheets/d/18kYr8DmDLnUUYzJJVHxzit5KCY286YozrrrIpOeojXI/gviz/tq?tqx=out:csv"
try:
    df = pd.read_csv(sheet_url)
    df = df[['Tên ứng dụng', 'Liên kết', 'Nhóm chức năng']].dropna()
    grouped = df.groupby('Nhóm chức năng')

    st.sidebar.markdown("<h3 style='color:#003399'>📚 Danh mục hệ thống</h3>", unsafe_allow_html=True)
    for group_name, group_data in grouped:
        with st.sidebar.expander(f"📂 {group_name}", expanded=False):
            for _, row in group_data.iterrows():
                label = row['Tên ứng dụng']
                link = row['Liên kết']
                st.markdown(f"""
                    <a href="{link}" target="_blank" class="sidebar-button">
                        🚀 {label}
                    </a>
                """, unsafe_allow_html=True)
except Exception as e:
    st.sidebar.error(f"🚫 Không thể tải menu từ Google Sheet. Lỗi: {e}")

# ================== GIỚI THIỆU ==================
st.info("""
👋 Chào mừng anh Long đến với Trung tâm điều hành số - phần mềm Điện lực Định Hóa

📌 **Các tính năng nổi bật:**
- Phân tích thất bại, báo cáo kỹ thuật
- Lưu trữ và truy xuất lịch sử GPT
- Truy cập hệ thống nhanh chóng qua Sidebar

✅ Mọi bản cập nhật chỉ cần chỉnh sửa Google Sheet đều tự động hiển thị!
""")

# ================== NÚT CHỨC NĂNG CHÍNH ==================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="display: flex; justify-content: center; flex-wrap: wrap;">
    <a href="https://terabox.com/s/1cegqu7nP7rd0BdL_MIyrtA" target="_blank" class="main-button">📦 Bigdata_Terabox</a>
    <a href="https://chat.openai.com/c/2d132e26-7b53-46b3-bbd3-8a5229e77973" target="_blank" class="main-button">🤖 AI. PHẠM HỒNG LONG</a>
    <a href="https://www.youtube.com" target="_blank" class="main-button">🎬 video tuyên truyền</a>
    <a href="https://www.dropbox.com/scl/fo/yppcs3fy1sxrilyzjbvxa/APan4-c_N5NwbIDtTzUiuKo?dl=0" target="_blank" class="main-button">📄 Báo cáo CMIS</a>
</div>
""", unsafe_allow_html=True)



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


# ====== MODULE ĐÃ GHÉP TỪ PHIÊN BẢN ỔN ĐỊNH ======


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
