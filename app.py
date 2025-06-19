from pathlib import Path
import streamlit as st
import streamlit as st
import pandas as pd
from PIL import Image
import datetime
import streamlit as st
import pandas as pd
import os
import io
from datetime import date, time, datetime
from PIL import Image
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
import zipfile
import math
import re

st.set_page_config(page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa", layout="wide")
st.markdown('''
<style>
    html, body {
        font-size: 20px !important;
    }
    h1, h2, h3, h4 {
        font-size: 2em !important;
    }
    button, label, select, input, textarea {
        font-size: 1.6em !important;
    }
    a.sidebar-button {
    font-size: 0.9em !important;
}

.sidebar-button {
        font-size: 1.5em !important;
    }
    section[data-testid="stSidebar"] {
        font-size: 1.4em !important;
    }
</style>
''', unsafe_allow_html=True)


# ================== CUSTOM CSS ==================
st.markdown("""
    <style>
        section[data-testid="stSidebar"] > div:first-child {
            max-height: 95vh;
            overflow-y: auto;
        }
        a.sidebar-button {
    font-size: 0.9em !important;
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
        <p style='font-size:13px; color:gray;'>Bản quyền &copy; 2025 by Phạm Hồng Long & Brown Eyes</p>

# ================== MENU TỪ GOOGLE SHEET ==================
sheet_url = "https://docs.google.com/spreadsheets/d/18kYr8DmDLnUUYzJJVHxzit5KCY286YozrrrIpOeojXI/gviz/tq?tqx=out:csv"

}
try:
    df = pd.read_csv(sheet_url)
    df = df[['Tên ứng dụng', 'Liên kết', 'Nhóm chức năng']].dropna()
    grouped = df.groupby('Nhóm chức năng')

}


    st.sidebar.markdown("<h3 style='color:#003399'>📚 Danh mục hệ thống</h3>", unsafe_allow_html=True)
    

    for group_name, group_data in grouped:
        with st.sidebar.expander(f"{icon} {group_name}", expanded=False):
        
            for _, row in group_data.iterrows():
                label = row['Tên ứng dụng']
                link = row['Liên kết']
                st.markdown(f"""
                    <a href="{link}" target="_blank" class="sidebar-button">
                        🚀 {label}
                    </a>
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

# ================== NÚT CHỨC NĂNG CHÍNH ==================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="display: flex; justify-content: center; flex-wrap: wrap;">
    <a href="https://terabox.com/s/1cegqu7nP7rd0BdL_MIyrtA" target="_blank" class="main-button">📦 Bigdata_Terabox</a>
    <a href="https://chat.openai.com/c/2d132e26-7b53-46b3-bbd3-8a5229e77973" target="_blank" class="main-button">🤖 AI. PHẠM HỒNG LONG</a>
    <a href="https://www.youtube.com" target="_blank" class="main-button">🎬 video tuyên truyền</a>
    <a href="https://www.dropbox.com/scl/fo/yppcs3fy1sxrilyzjbvxa/APan4-c_N5NwbIDtTzUiuKo?dl=0" target="_blank" class="main-button">📄 Báo cáo CMIS</a>
</div>




st.set_page_config(page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa", layout="wide")

# ===== FILE LƯU DỮ LIỆU =====
REMINDERS_FILE = "nhac_viec.csv"
MEETINGS_FILE = "lich_su_cuoc_hop.csv"
UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

EMAIL_MAC_DINH = "phamlong666@gmail.com"

# ===== NÚT NHẮC VIỆC =====

# =============== GÓI CÁC MODULE VÀO MENU CHỌN ===============
chon_modul = st.selectbox('📌 Chọn chức năng làm việc', ['⏰ Nhắc việc', '📑 Phục vụ họp', '📍 Dự báo điểm sự cố'])

if chon_modul == '⏰ Nhắc việc':
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

elif chon_modul == '📑 Phục vụ họp':
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
    
    st.set_page_config(layout="wide")
    st.markdown("<style>html, body, [class*='css']  {font-size: 2em !important;}</style>", unsafe_allow_html=True)

elif chon_modul == '📍 Dự báo điểm sự cố':
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

icon_map = {
"An toàn": "🧯",
"An toàn, điều độ": "🛡️",
"Báo cáo": "📊",
"Công nghệ thông tin": "🧠",
"Kinh doanh": "💼",
"Kỹ thuật": "🔧",
"Quản trị nội bộ": "👥",
"Thiên tai - cứu nạn": "🆘",
"Điều độ": "🧭"
}

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
            ])
        with col2:
            vi_tri = st.text_input("Vị trí sự cố")
            nguyen_nhan = st.text_input("Nguyên nhân")
            thoi_tiet = st.text_input("Thời tiết")
    
        submitted = st.form_submit_button("Lưu vụ sự cố")
        if submitted:
            st.session_state.suco_data.append({
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
    
    # ============================
    # TÍNH TOÁN KHOẢNG CÁCH SỰ CỐ
    # ============================
    def extract_current(dong_suco_str, loai_suco):
        try:
            values = re.findall(r'\d+', dong_suco_str)
            values = [int(v) for v in values]
            if not values:
                return None
            if "Io" in loai_suco:
                return values[-1]  # mặc định Io là cuối
            else:
                return sum(values)
        except:
            return None
    
    def tinh_khoang_cach(I_suco, U0_V, z_ohm_per_km):
        try:
            return round((U0_V / (I_suco * z_ohm_per_km)), 2)
        except:
            return None
    
    st.subheader("🔍 Dự báo điểm sự cố từ dòng điện")
    ten_mc_input = st.text_input("Tên máy cắt muốn dự báo")
    dong_input = st.text_input("Dòng sự cố (ví dụ: Ia=500, Ib=600, Ic=50, Io=400)")
    cap_dien_ap = st.selectbox("Cấp điện áp đường dây", ["22kV", "35kV", "110kV"])
    z_default = 4.0  # suất trở hỗn hợp đã cập nhật theo yêu cầu
    loai_suco_input = st.selectbox("Loại sự cố", [
    ])
    
    if st.button("Phân tích"):
        U0_map = {"22kV": 22000 / math.sqrt(3), "35kV": 35000 / math.sqrt(3), "110kV": 110000 / math.sqrt(3)}
        I = extract_current(dong_input, loai_suco_input)
        if I:
            d = tinh_khoang_cach(I, U0_map[cap_dien_ap], z_default)
            if d:
                st.success(f"✅ Khoảng cách dự kiến đến điểm sự cố: {d} km")
            else:
                st.warning("⚠️ Không tính được khoảng cách.")
        else:
            st.warning("⚠️ Không nhận diện được dòng sự cố hợp lệ.")
    
    # BỔ SUNG: Dự báo từ dữ liệu lịch sử
    st.subheader("📚 Dự báo điểm sự cố từ dữ liệu lịch sử")
    ten_mc_ls = st.text_input("🔎 Nhập tên máy cắt để lọc dữ liệu")
    dong_moi = st.text_input("Nhập dòng sự cố mới (Ia, Ib, Ic, Io)")
    if dong_moi:
        try:
            input_values = [int(x.strip()) for x in re.findall(r'\d+', dong_moi)]
            def euclidean(a, b):
                return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
    
            min_dist = float('inf')
            nearest_case = None
            for case in st.session_state.suco_data:
                try:
                    if ten_mc_ls and ten_mc_ls not in case.get("Tên máy cắt", ""):
                        continue
                    case_values = [int(x.strip()) for x in re.findall(r'\d+', case["Dòng sự cố"])]
                    if len(case_values) == len(input_values):
                        dist = euclidean(input_values, case_values)
                        if dist < min_dist:
                            min_dist = dist
                            nearest_case = case
                except:
                    continue
    
            if nearest_case:
                st.success(f"✅ Dự báo gần nhất theo lịch sử: {nearest_case['Vị trí']} – Nguyên nhân: {nearest_case['Nguyên nhân']}")
            else:
                st.warning("⚠️ Không tìm thấy dòng sự cố tương đồng trong dữ liệu lịch sử.")
        except:
            st.warning("⚠️ Định dạng dòng sự cố không hợp lệ. Vui lòng nhập theo dạng: 500, 600, 50, 400")
    
    
}
