from pathlib import Path
import streamlit as st
st.set_page_config(page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa", layout="wide")

import streamlit as st
import pandas as pd
from PIL import Image
import datetime

# ================== CUSTOM CSS ==================
st.markdown("""
""", unsafe_allow_html=True)

# ================== HEADER ==================
col1, col2 = st.columns([1, 10])
with col1:

with col2:

# ================== MENU TỪ GOOGLE SHEET ==================
sheet_url = "https://docs.google.com/spreadsheets/d/18kYr8DmDLnUUYzJJVHxzit5KCY286YozrrrIpOeojXI/gviz/tq?tqx=out:csv"
try:

except Exception as e:

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


# ========== MODULE CHỌN CHỨC NĂNG ==========

st.markdown("## 📂 Chọn chức năng làm việc")
mod_option = st.selectbox("📌 Vui lòng chọn module", ["Trang chủ", "Nhắc việc", "Phục vụ họp", "Dự báo điểm sự cố"])

if mod_option == "Trang chủ":

if mod_option == "Nhắc việc":
    
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
    
elif mod_option == "Phục vụ họp":
    
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
    import streamlit as st
    import pandas as pd
    import math
    import folium
    from folium.plugins import MarkerCluster
    from streamlit_folium import st_folium
    from datetime import datetime
    import zipfile
    import xml.etree.ElementTree as ET
    import json
    import os
    import io
    import re
    
    st.set_page_config(layout="wide")
    st.markdown("<style>html, body, [class*='css']  {font-size: 1.3em !important;}</style>", unsafe_allow_html=True)
    st.title("📍 Dự báo điểm sự cố")
    
    marker_locations = {}
    kmz_file = st.file_uploader("📂 Tải file KMZ để lấy dữ liệu tọa độ cột", type="kmz")
    if kmz_file is not None:
        with zipfile.ZipFile(kmz_file, 'r') as z:
            for filename in z.namelist():
                if filename.endswith('.kml'):
                    with z.open(filename) as f:
                        tree = ET.parse(f)
                        root = tree.getroot()
                        ns = {'kml': 'http://www.opengis.net/kml/2.2'}
                        for pm in root.findall('.//kml:Placemark', ns):
                            name_tag = pm.find('kml:name', ns)
                            point = pm.find('.//kml:coordinates', ns)
                            if name_tag is not None and point is not None:
                                name = name_tag.text.strip()
                                coords = point.text.strip().split(',')
                                lon, lat = float(coords[0]), float(coords[1])
                                marker_locations[name] = (lat, lon)
        st.success(f"✅ Đã trích xuất {len(marker_locations)} điểm từ file KMZ.")
    
    st.subheader("📝 Nhập các vụ sự cố lịch sử")
    uploaded_excel = st.file_uploader("📥 Tải dữ liệu lịch sử từ file Excel (.xlsx)", type="xlsx")
    if uploaded_excel is not None:
        try:
            df_uploaded = pd.read_excel(uploaded_excel)
            st.session_state.suco_data = df_uploaded.to_dict(orient="records")
            st.success("✅ Đã nạp dữ liệu lịch sử từ file thành công.")
        except Exception as e:
            st.warning(f"⚠️ Không thể đọc file: {e}")
    
    if "suco_data" not in st.session_state:
        st.session_state.suco_data = []
    
    with st.form("suco_form"):
        col1, col2 = st.columns(2)
        with col1:
            ten_mc = st.text_input("Tên máy cắt")
            ngay = st.date_input("Ngày xảy ra sự cố", format="DD/MM/YYYY")
            dong_suco = st.text_input("Dòng sự cố (Ia, Ib, Ic, Io, 3Uo...)")
            loai_suco = st.selectbox("Loại sự cố", [
                "1 pha chạm đất (Io)",
                "2 pha chạm đất (Ia+Ib)",
                "3 pha chạm đất (Ia+Ib+Ic)",
                "Ngắn mạch 2 pha (Ia+Ib)",
                "Ngắn mạch 3 pha (Ia+Ib+Ic)",
                "Ngắn mạch 2 pha có Io (Ia+Ib+Io)",
                "Ngắn mạch 3 pha có Io (Ia+Ib+Ic+Io)",
                "Ngắn mạch 1 pha có Io (Ia+Io)",
                "Ngắn mạch 2 pha có Io (Ib+Ic+Io)",
                "Ngắn mạch 3 pha có Io (Ia+Ib+Ic+Io)"
            ])
        with col2:
            vi_tri = st.text_input("Vị trí sự cố")
            nguyen_nhan = st.text_input("Nguyên nhân")
            thoi_tiet = st.text_input("Thời tiết")
    
        submitted = st.form_submit_button("Lưu vụ sự cố")
        if submitted:
            st.session_state.suco_data.append({
                "Tên máy cắt": ten_mc,
                "Ngày": ngay.strftime("%d/%m/%Y"),
                "Dòng sự cố": dong_suco,
                "Loại sự cố": loai_suco,
                "Vị trí": vi_tri,
                "Nguyên nhân": nguyen_nhan,
                "Thời tiết": thoi_tiet
            })
            st.success("✔️ Đã lưu vụ sự cố!")
    
    if st.session_state.suco_data:
        st.write("### 📋 Danh sách sự cố đã nhập")
        df_suco = pd.DataFrame(st.session_state.suco_data)
        edited_df = st.data_editor(df_suco, num_rows="dynamic", use_container_width=True)
    
        if st.button("Cập nhật dữ liệu đã sửa"):
            st.session_state.suco_data = edited_df.to_dict(orient="records")
            st.success("✔️ Đã cập nhật danh sách sau khi chỉnh sửa!")
    
        def convert_df(df):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='SuCo', index=False)
            writer.close()
            return output.getvalue()
    
        st.download_button(
            label="📤 Xuất báo cáo Excel",
            data=convert_df(df_suco),
            file_name="bao_cao_su_co.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
        df_suco.to_excel("du_lieu_su_co.xlsx", index=False)
    
elif mod_option == "Dự báo điểm sự cố":
    
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
    import streamlit as st
    import pandas as pd
    import math
    import folium
    from folium.plugins import MarkerCluster
    from streamlit_folium import st_folium
    from datetime import datetime
    import zipfile
    import xml.etree.ElementTree as ET
    import json
    import os
    import io
    import re
    
    st.set_page_config(layout="wide")
    st.markdown("<style>html, body, [class*='css']  {font-size: 1.3em !important;}</style>", unsafe_allow_html=True)
    st.title("📍 Dự báo điểm sự cố")
    
    marker_locations = {}
    kmz_file = st.file_uploader("📂 Tải file KMZ để lấy dữ liệu tọa độ cột", type="kmz")
    if kmz_file is not None:
        with zipfile.ZipFile(kmz_file, 'r') as z:
            for filename in z.namelist():
                if filename.endswith('.kml'):
                    with z.open(filename) as f:
                        tree = ET.parse(f)
                        root = tree.getroot()
                        ns = {'kml': 'http://www.opengis.net/kml/2.2'}
                        for pm in root.findall('.//kml:Placemark', ns):
                            name_tag = pm.find('kml:name', ns)
                            point = pm.find('.//kml:coordinates', ns)
                            if name_tag is not None and point is not None:
                                name = name_tag.text.strip()
                                coords = point.text.strip().split(',')
                                lon, lat = float(coords[0]), float(coords[1])
                                marker_locations[name] = (lat, lon)
        st.success(f"✅ Đã trích xuất {len(marker_locations)} điểm từ file KMZ.")
    
    st.subheader("📝 Nhập các vụ sự cố lịch sử")
    uploaded_excel = st.file_uploader("📥 Tải dữ liệu lịch sử từ file Excel (.xlsx)", type="xlsx")
    if uploaded_excel is not None:
        try:
            df_uploaded = pd.read_excel(uploaded_excel)
            st.session_state.suco_data = df_uploaded.to_dict(orient="records")
            st.success("✅ Đã nạp dữ liệu lịch sử từ file thành công.")
        except Exception as e:
            st.warning(f"⚠️ Không thể đọc file: {e}")
    
    if "suco_data" not in st.session_state:
        st.session_state.suco_data = []
    
    with st.form("suco_form"):
        col1, col2 = st.columns(2)
        with col1:
            ten_mc = st.text_input("Tên máy cắt")
            ngay = st.date_input("Ngày xảy ra sự cố", format="DD/MM/YYYY")
            dong_suco = st.text_input("Dòng sự cố (Ia, Ib, Ic, Io, 3Uo...)")
            loai_suco = st.selectbox("Loại sự cố", [
                "1 pha chạm đất (Io)",
                "2 pha chạm đất (Ia+Ib)",
                "3 pha chạm đất (Ia+Ib+Ic)",
                "Ngắn mạch 2 pha (Ia+Ib)",
                "Ngắn mạch 3 pha (Ia+Ib+Ic)",
                "Ngắn mạch 2 pha có Io (Ia+Ib+Io)",
                "Ngắn mạch 3 pha có Io (Ia+Ib+Ic+Io)",
                "Ngắn mạch 1 pha có Io (Ia+Io)",
                "Ngắn mạch 2 pha có Io (Ib+Ic+Io)",
                "Ngắn mạch 3 pha có Io (Ia+Ib+Ic+Io)"
            ])
        with col2:
            vi_tri = st.text_input("Vị trí sự cố")
            nguyen_nhan = st.text_input("Nguyên nhân")
            thoi_tiet = st.text_input("Thời tiết")
    
        submitted = st.form_submit_button("Lưu vụ sự cố")
        if submitted:
            st.session_state.suco_data.append({
                "Tên máy cắt": ten_mc,
                "Ngày": ngay.strftime("%d/%m/%Y"),
                "Dòng sự cố": dong_suco,
                "Loại sự cố": loai_suco,
                "Vị trí": vi_tri,
                "Nguyên nhân": nguyen_nhan,
                "Thời tiết": thoi_tiet
            })
            st.success("✔️ Đã lưu vụ sự cố!")
    
    if st.session_state.suco_data:
        st.write("### 📋 Danh sách sự cố đã nhập")
        df_suco = pd.DataFrame(st.session_state.suco_data)
        edited_df = st.data_editor(df_suco, num_rows="dynamic", use_container_width=True)
    
        if st.button("Cập nhật dữ liệu đã sửa"):
            st.session_state.suco_data = edited_df.to_dict(orient="records")
            st.success("✔️ Đã cập nhật danh sách sau khi chỉnh sửa!")
    
        def convert_df(df):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='SuCo', index=False)
            writer.close()
            return output.getvalue()
    
        st.download_button(
            label="📤 Xuất báo cáo Excel",
            data=convert_df(df_suco),
            file_name="bao_cao_su_co.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
        df_suco.to_excel("du_lieu_su_co.xlsx", index=False)
    