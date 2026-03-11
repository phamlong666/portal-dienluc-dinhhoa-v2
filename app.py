from pathlib import Path
import streamlit as st
import pandas as pd
import os
import io
from datetime import date, time, datetime
from PIL import Image
import math
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import zipfile
import xml.etree.ElementTree as ET
import json
import re
import matplotlib.pyplot as plt # Import for plotting in loss analysis
from google.oauth2 import service_account # Import for Google Drive
from googleapiclient.discovery import build # Import for Google Drive
from googleapiclient.http import MediaIoBaseDownload # Import for Google Drive

# ================== CẤU HÌNH EMAIL GỬI NHẮC VIỆC ==================
# Anh cần đảm bảo thông tin email và mật khẩu ứng dụng là chính xác
# và đã cho phép ứng dụng kém an toàn truy cập (hoặc sử dụng mật khẩu ứng dụng của Google)
# Lưu ý: yagmail cần được cài đặt: pip install yagmail
import yagmail

EMAIL_TAI_KHOAN = "phamlong666@gmail.com"
EMAIL_MAT_KHAU = "zaacuxxvznflqavt"  # Mật khẩu ứng dụng Gmail (KHÔNG PHẢI MẬT KHẨU TÀI KHOẢN CHÍNH)

def gui_email_nhac_viec(viec, ngay, gio, nguoinhan):
    """Gửi email nhắc việc."""
    try:
        # Khởi tạo đối tượng SMTP của yagmail
        yag = yagmail.SMTP(EMAIL_TAI_KHOAN, EMAIL_MAT_KHAU)
        subject = "⏰ Nhắc việc từ Trung tâm điều hành số"
        body = f"""
        Xin chào,

        Đây là nhắc việc tự động từ hệ thống:

        📌 Việc: {viec}
        📅 Ngày: {ngay}
        ⏰ Giờ: {gio}

        Hệ thống điều hành số - Điện lực Định Hóa.
        """
        # Gửi email tới người nhận với tiêu đề và nội dung đã cho
        yag.send(to=nguoinhan, subject=subject, contents=body)
        st.success("📧 Đã gửi email nhắc việc thành công.")
    except Exception as e:
        st.warning(f"⚠️ Không gửi được email: {e}. Vui lòng kiểm tra lại thông tin tài khoản và mật khẩu ứng dụng Gmail.")

# ================== CẤU HÌNH CHUNG CỦA ỨNG DỤNG STREAMLIT ==================
st.set_page_config(
    page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa",
    layout="wide",
    initial_sidebar_state="auto" # Giúp sidebar luôn mở theo mặc định
)

# ================== CUSTOM CSS CHO GIAO DIỆN ==================
st.markdown('''
<style>
    /* Điều chỉnh kích thước font chữ tổng thể */
    html, body, [class*="css"] {
        font-size: 1.1em !important; /* Giảm font nhẹ để phù hợp hơn với nhiều module */
    }
    /* Tiêu đề sidebar */
    section[data-testid="stSidebar"] h3 {
        font-size: 1.4em !important;
        font-weight: bold;
        margin-top: 1em;
    }
    /* Nút trong sidebar */
    .sidebar-button {
        display: block;
        background-color: #42A5F5;
        color: #ffffff !important;
        padding: 10px 15px; /* Điều chỉnh padding */
        border-radius: 8px; /* Điều chỉnh bo góc */
        margin: 6px 0; /* Điều chỉnh margin */
        font-weight: bold;
        font-size: 1.1em; /* Điều chỉnh font size */
        text-shadow: 0px 0px 2px rgba(0,0,0,0.5); /* Điều chỉnh shadow */
        box-shadow: 1px 1px 3px rgba(0,0,0,0.25); /* Điều chỉnh shadow */
        transition: all 0.2s ease-in-out;
        text-decoration: none;
    }
    .sidebar-button:hover {
        background-color: #1E88E5 !important;
        transform: translateY(-1px);
        box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
    }
    /* Tiêu đề chính trong nội dung */
    h2, h3, h4 {
        font-weight: bold !important;
        color: #1a237e;
    }
    /* Padding cho khối nội dung chính */
    .block-container {
        padding: 2rem 2rem 4rem 2rem;
    }
    /* Nút chính */
    .main-button {
        display: inline-block;
        background-color: #FFCC80;
        color: white;
        text-align: center;
        padding: 20px 28px; /* Điều chỉnh padding */
        border-radius: 12px; /* Điều chỉnh bo góc */
        font-weight: bold;
        text-decoration: none;
        margin: 12px;
        transition: 0.3s;
        font-size: 22px; /* Điều chỉnh font size */
        box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
    }
    .main-button:hover {
        transform: scale(1.03); /* Giảm hiệu ứng scale nhẹ hơn */
        box-shadow: 3px 3px 10px rgba(0,0,0,0.25);
    }
    /* Cuộn sidebar nếu nội dung quá dài */
    section[data-testid="stSidebar"] > div:first-child {
        max-height: 95vh;
        overflow-y: auto;
    }
</style>
''', unsafe_allow_html=True)

# ================== HEADER ỨNG DỤNG ==================
col1, col2 = st.columns([1, 10])
with col1:
    try:
        # Đảm bảo file logo.png nằm trong thư mục 'assets' cùng cấp với app.py
        logo = Image.open("assets/logo_hinh_tron_hoan_chinh.png")
        st.image(logo, width=70)
    except FileNotFoundError:
        st.warning("⚠️ Không tìm thấy logo. Vui lòng đặt file 'logo_hinh_tron_hoan_chinh.png' vào thư mục 'assets'.")
    except Exception as e:
        st.warning(f"⚠️ Lỗi khi tải logo: {e}")

with col2:
    st.markdown("""
        <h1 style='color:#003399; font-size:42px; margin-top:18px;'>
        Trung tâm điều hành số - phần mềm Điện lực Định Hóa
        </h1>
        <p style='font-size:13px; color:gray;'>Bản quyền © 2025 by Phạm Hồng Long & Brown Eyes</p>
    """, unsafe_allow_html=True)

# ================== MENU TỪ GOOGLE SHEET (SIDEBAR) ==================
# URL tới Google Sheet chứa danh mục ứng dụng
SHEET_URL_MENU = "https://docs.google.com/spreadsheets/d/18kYr8DmDLnUUYzJJVHxzit5KCY286YozrrrIpOeojXI/gviz/tq?tqx=out:csv"
try:
    df_menu = pd.read_csv(SHEET_URL_MENU)
    df_menu = df_menu[['Tên ứng dụng', 'Liên kết', 'Nhóm chức năng']].dropna()
    grouped_menu = df_menu.groupby('Nhóm chức năng')

    st.sidebar.markdown("<h3 style='color:#003399'>📚 Danh mục hệ thống</h3>", unsafe_allow_html=True)
    for group_name, group_data in grouped_menu:
        with st.sidebar.expander(f"📁 {group_name}", expanded=False):
            for _, row in group_data.iterrows():
                label = row['Tên ứng dụng']
                link = row['Liên kết']
                st.markdown(f"""
                    <a href="{link}" target="_blank" class="sidebar-button">
                        🚀 {label}
                    </a>
                """, unsafe_allow_html=True)
except Exception as e:
    st.sidebar.error(f"🚫 Không thể tải menu từ Google Sheet. Lỗi: {e}. Vui lòng kiểm tra URL hoặc quyền truy cập.")

# ================== GIỚI THIỆU CHUNG ==================
st.info("""
👋 Chào mừng đến với Trung tâm điều hành số - phần mềm Điện lực Định Hóa

📌 **Các tính năng nổi bật:**
- Quản lý nhắc việc và lịch sử họp
- Dự báo điểm sự cố từ dữ liệu dòng điện và lịch sử
- Phân tích và quản lý tổn thất điện năng (TBA, Hạ thế, Trung thế, Toàn đơn vị)
- Kết nối tới Dropbox, Terabox và AI cá nhân
- Truy cập hệ thống nhanh chóng qua Sidebar

✅ Mọi bản cập nhật chỉ cần chỉnh sửa Google Sheet đều tự động hiển thị!
""")

# ================== NÚT CHỨC NĂNG CHÍNH TRÊN TRANG ==================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="display: flex; justify-content: center; flex-wrap: wrap;">
    <a href="https://terabox.com/s/1cegqu7nP7rd0BdL_MIyrtA" target="_blank" class="main-button">📦 Bigdata_Terabox</a>
    <a href="https://chat.openai.com/c/2d132e26-7b53-46b3-bbd3-8a5229e77973" target="_blank" class="main-button">🤖 AI. PHẠM HỒNG LONG</a>
    <a href="https://www.youtube.com" target="_blank" class="main-button">🎬 video tuyên truyền</a>
    <a href="https://www.dropbox.com/scl/fo/yppcs3fy1sxrilyzjbvxa/APan4-c_N5N5wbIDtTzUiuKo?dl=0" target="_blank" class="main-button">  Báo cáo CMIS</a>
</div>
""", unsafe_allow_html=True)

# ================== CẤU HÌNH FILE LƯU TRỮ DỮ LIỆU CỤC BỘ ==================
REMINDERS_FILE = "nhac_viec.csv"
MEETINGS_FILE = "lich_su_cuoc_hop.csv"
UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True) # Đảm bảo thư mục tồn tại

# ================== KHỞI TẠO SESSION STATE (QUAN TRỌNG ĐỂ DUY TRÌ DỮ LIỆU) ==================
# Khởi tạo session state cho module "AI Trợ lý tổn thất"
if 'df_tba_thang' not in st.session_state: st.session_state.df_tba_thang = None
if 'df_tba_luyke' not in st.session_state: st.session_state.df_tba_luyke = None
if 'df_tba_ck' not in st.session_state: st.session_state.df_tba_ck = None
if 'df_ha_thang' not in st.session_state: st.session_state.df_ha_thang = None
if 'df_ha_luyke' not in st.session_state: st.session_state.df_ha_luyke = None
if 'df_ha_ck' not in st.session_state: st.session_state.df_ha_ck = None
if 'df_trung_thang_tt' not in st.session_state: st.session_state.df_trung_thang_tt = None
if 'df_trung_luyke_tt' not in st.session_state: st.session_state.df_trung_ck_tt = None # Lỗi chính tả ở đây, giữ nguyên theo code gốc nếu có thể.
if 'df_trung_thang_dy' not in st.session_state: st.session_state.df_trung_thang_dy = None
if 'df_trung_luyke_dy' not in st.session_state: st.session_state.df_trung_luyke_dy = None
if 'df_trung_ck_dy' not in st.session_state: st.session_state.df_trung_ck_dy = None
if 'df_dv_thang' not in st.session_state: st.session_state.df_dv_thang = None
if 'df_dv_luyke' not in st.session_state: st.session_state.df_dv_luyke = None
if 'df_dv_ck' not in st.session_state: st.session_state.df_dv_ck = None
# Khởi tạo st.session_state.suco_data ở cấp cao nhất để đảm bảo luôn có sẵn
if "suco_data" not in st.session_state:
    st.session_state.suco_data = [] # Luôn khởi tạo là danh sách rỗng
    STORAGE_FILE_SUCO = "storage_bao_cao_su_co.xlsx"
    if os.path.exists(STORAGE_FILE_SUCO):
        try:
            df_loaded_suco = pd.read_excel(STORAGE_FILE_SUCO)
            st.session_state.suco_data = df_loaded_suco.to_dict(orient="records")
        except Exception as e:
            st.warning(f"⚠️ Không thể đọc dữ liệu sự cố từ file đã lưu: {e}. Đang sử dụng dữ liệu trống.")
            st.session_state.suco_data = [] # Đảm bảo reset nếu lỗi

# Cờ để kiểm soát việc tải lại file upload cho module sự cố
if 'file_uploaded_flag_suco' not in st.session_state:
    st.session_state.file_uploaded_flag_suco = False

# ================== BIẾN VÀ HÀM HỖ TRỢ TẢI DỮ LIỆU TỪ GOOGLE DRIVE ==================
# Anh cần tạo file .streamlit/secrets.toml với thông tin tài khoản dịch vụ Google Cloud
# Ví dụ:
# [google]
# type = "service_account"
# project_id = "your-gcp-project-id"
# private_key_id = "..."
# private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
# client_email = "your-service-account-email@your-gcp-project-id.iam.gserviceaccount.com"
# client_id = "..."
# auth_uri = "https://accounts.google.com/o/oauth2/auth"
# token_uri = "https://oauth2.googleapis.com/token"
# auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
# client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account-email%40your-gcp-project-id.iam.gserviceaccount.com"
# universe_domain = "googleapis.com"

@st.cache_resource # Sử dụng st.cache_resource cho dịch vụ để tránh khởi tạo lại không cần thiết
def get_drive_service():
    """Khởi tạo và trả về đối tượng dịch vụ Google Drive."""
    try:
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["google"],
            scopes=["https://www.googleapis.com/auth/drive.readonly"] # Chỉ cần quyền đọc
        )
        return build('drive', 'v3', credentials=credentials)
    except KeyError:
        st.error("Lỗi: Không tìm thấy cấu hình Google Drive trong `secrets.toml`. Vui lòng tham khảo hướng dẫn để tạo file này.")
        return None
    except Exception as e:
        st.error(f"Lỗi khi xác thực Google Drive: {e}. Vui lòng kiểm tra cấu hình `secrets.toml`.")
        return None

@st.cache_data # Sử dụng st.cache_data cho các kết quả tải về để tăng tốc độ
def list_excel_files_from_folder(folder_id):
    """Liệt kê các file Excel trong thư mục Google Drive đã cho."""
    service = get_drive_service()
    if not service:
        return {}
    query = f"'{folder_id}' in parents and mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'"
    try:
        results = service.files().list(q=query, fields="files(id, name)").execute()
        return {f['name']: f['id'] for f in results.get('files', [])}
    except Exception as e:
        st.error(f"Lỗi khi liệt kê file từ Google Drive (thư mục {folder_id}): {e}. Vui lòng kiểm tra ID thư mục và quyền truy cập.")
        return {}

@st.cache_data # Sử dụng st.cache_data cho các kết quả tải về để tăng tốc độ
def download_excel_from_drive(file_id):
    """Tải xuống file Excel từ Google Drive bằng ID file."""
    service = get_drive_service()
    if not service:
        return pd.DataFrame()
    try:
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            # Có thể thêm thanh tiến trình ở đây: st.progress(status.progress())
        fh.seek(0)
        return pd.read_excel(fh, sheet_name=0) # Đọc sheet đầu tiên
    except Exception as e:
        st.warning(f"Không thể tải xuống hoặc đọc file với ID {file_id}. Lỗi: {e}. Có thể file không tồn tại hoặc không đúng định dạng sheet 'dữ liệu'.")
        return pd.DataFrame()

def generate_filenames(year, start_month, end_month, prefix):
    """Tạo danh sách tên file dự kiến dựa trên năm, tháng và tiền tố."""
    return [f"{prefix}_{year}_{str(m).zfill(2)}.xlsx" for m in range(start_month, end_month + 1)]

def load_data_from_drive(file_list, all_files_in_folder, nhan="Thực hiện"):
    """Tải và nối các DataFrame từ danh sách file Google Drive."""
    dfs = []
    for fname in file_list:
        file_id = all_files_in_folder.get(fname)
        if file_id:
            df = download_excel_from_drive(file_id)
            if not df.empty:
                df["Kỳ"] = nhan
                dfs.append(df)
        # else: # Gỡ bỏ thông báo này để tránh làm quá tải giao diện nếu có nhiều file thiếu
            # st.info(f"Không tìm thấy file: {fname}")
    return pd.concat(dfs) if dfs else pd.DataFrame()

def classify_nguong(x):
    """Phân loại tỷ lệ tổn thất vào các ngưỡng."""
    try:
        x = float(str(x).replace(",", "."))
    except (ValueError, TypeError):
        return "Không rõ"

    if x < 2: return "<2%"
    elif 2 <= x < 3: return ">=2 và <3%"
    elif 3 <= x < 4: return ">=3 và <4%"
    elif 4 <= x < 5: return ">=4 và <5%"
    elif 5 <= x < 7: return ">=5 và <7%"
    else: return ">=7%"

# ================== CHỌN MODULE LÀM VIỆC ==================
# Đã thêm các lựa chọn mới cho module "AI Trợ lý tổn thất"
chon_modul = st.selectbox(
    '📌 Chọn chức năng làm việc',
    [
        '⏰ Nhắc việc',
        '📑 Phục vụ họp',
        '📍 Dự báo điểm sự cố',
        '⚡ AI Trợ lý tổn thất' # Module mới được thêm vào
    ],
    key="main_module_selector" # Đảm bảo key duy nhất
)

# ================== LOGIC HIỂN THỊ TỪNG MODULE = ==================

if chon_modul == '⏰ Nhắc việc':
    st.header("⏰ Nhắc việc")

    # Tạo mới danh sách nhắc việc
    if st.button("🆕 Tạo mới danh sách nhắc việc"):
        df_nhac_viec = pd.DataFrame(columns=["Việc", "Ngày", "Giờ", "Email"])
        df_nhac_viec.to_csv(REMINDERS_FILE, index=False)
        st.success("✅ Đã khởi tạo danh sách nhắc việc.")

    # Thêm việc cần nhắc
    with st.expander("➕ Thêm việc cần nhắc"):
        with st.form("form_nhac"):
            viec = st.text_input("🔔 Việc cần nhắc")
            ngay = st.date_input("📅 Ngày", date.today(), format="DD/MM/YYYY")
            gio = st.time_input("⏰ Giờ", time(7, 30))
            email = st.text_input("📧 Gửi tới", value=EMAIL_TAI_KHOAN) # Sử dụng EMAIL_TAI_KHOAN làm mặc định
            submit = st.form_submit_button("📌 Tạo nhắc việc")
        if submit:
            if viec and email:
                new_row = {
                    "Việc": viec,
                    "Ngày": ngay.strftime("%d/%m/%y"),
                    "Giờ": gio.strftime("%H:%M"),
                    "Email": email
                }
                # Kiểm tra nếu file tồn tại, nếu không thì tạo DataFrame rỗng
                df_nhac_viec_current = pd.read_csv(REMINDERS_FILE) if os.path.exists(REMINDERS_FILE) else pd.DataFrame(columns=["Việc", "Ngày", "Giờ", "Email"])
                df_nhac_viec_current = pd.concat([df_nhac_viec_current, pd.DataFrame([new_row])], ignore_index=True)
                df_nhac_viec_current.to_csv(REMINDERS_FILE, index=False)
                st.success("✅ Đã tạo nhắc việc.")
                gui_email_nhac_viec(
                    viec,
                    ngay.strftime("%d/%m/%y"),
                    gio.strftime("%H:%M"),
                    email
                )
                st.rerun() # Refresh để cập nhật danh sách
            else:
                st.warning("⚠️ Vui lòng nhập 'Việc cần nhắc' và 'Email'.")

    # Hiển thị & xóa nhắc việc
    if os.path.exists(REMINDERS_FILE):
        st.subheader("📋 Danh sách nhắc việc")
        try:
            df_nhac_viec_display = pd.read_csv(REMINDERS_FILE, dtype=str)
            if not df_nhac_viec_display.empty:
                for idx, row in df_nhac_viec_display.iterrows():
                    col1, col2 = st.columns([6,1])
                    with col1:
                        st.write(f"📌 **{row['Việc']}** lúc {row['Giờ']} ngày {row['Ngày']} → {row['Email']}")
                    with col2:
                        if st.button("❌", key=f"xoa_nhac_{idx}"):
                            df_nhac_viec_display.drop(index=idx, inplace=True)
                            df_nhac_viec_display.to_csv(REMINDERS_FILE, index=False)
                            st.success("🗑️ Đã xoá nhắc việc.")
                            st.rerun()
            else:
                st.info("Chưa có nhắc việc nào được tạo.")
        except pd.errors.EmptyDataError:
            st.info("File nhắc việc trống. Hãy tạo một nhắc việc mới.")
        except Exception as e:
            st.error(f"❌ Lỗi khi hiển thị nhắc việc: {e}")

    # Xuất / Nhập Excel (Nhắc việc)
    st.markdown("### 📤 Xuất / Nhập Excel (Nhắc việc)")
    col_export_nhac, col_import_nhac = st.columns(2)

    with col_export_nhac:
        if os.path.exists(REMINDERS_FILE):
            df_export_nhac = pd.read_csv(REMINDERS_FILE)
            towrite_nhac = io.BytesIO()
            with pd.ExcelWriter(towrite_nhac, engine='xlsxwriter') as writer:
                df_export_nhac.to_excel(writer, index=False, sheet_name='NhacViec')
            towrite_nhac.seek(0)
            st.download_button("📥 Tải Excel nhắc việc", data=towrite_nhac, file_name="nhac_viec.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    with col_import_nhac:
        file_nhac = st.file_uploader("📁 Nhập từ Excel (Nhắc việc)", type=["xlsx"], key="upload_nhacviec")
        if file_nhac:
            try:
                df_import_nhac = pd.read_excel(file_nhac, dtype=str)
                # Chuẩn hoá ngày giờ nếu có thể
                if "Ngày" in df_import_nhac.columns:
                    df_import_nhac["Ngày"] = pd.to_datetime(df_import_nhac["Ngày"], errors="coerce").dt.strftime("%d/%m/%y").fillna("")
                if "Giờ" in df_import_nhac.columns:
                    # Chuyển đổi sang định dạng HH:MM, xử lý trường hợp giờ là float (Excel chuyển đổi)
                    df_import_nhac["Giờ"] = df_import_nhac["Giờ"].apply(
                        lambda x: pd.to_datetime(str(x), format='%H:%M', errors='coerce').strftime('%H:%M') if ':' in str(x) else \
                                   pd.to_datetime(f"{int(float(x)*24)}:{(float(x)*24 - int(float(x)*24))*60:02.0f}", format='%H:%M', errors='coerce').strftime('%H:%M') if pd.notna(x) else ""
                    ).fillna("00:00")

                df_import_nhac.to_csv(REMINDERS_FILE, index=False)
                st.success("✅ Đã nhập lại danh sách nhắc việc.")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Lỗi khi nhập file Excel nhắc việc: {e}")

elif chon_modul == '📑 Phục vụ họp':
    st.header("📑 Phục vụ họp")

    with st.expander("➕ Thêm cuộc họp mới"):
        with st.form("form_hop"):
            ten_hop = st.text_input("📌 Tên cuộc họp")
            ngay_hop = st.date_input("📅 Ngày họp", format="DD/MM/YYYY")
            gio_hop = st.time_input("⏰ Giờ họp", time(8, 0))
            noidung_hop = st.text_area("📝 Nội dung")
            files_hop = st.file_uploader("📎 Đính kèm", accept_multiple_files=True, key="files_hop_uploader")
            submit_hop = st.form_submit_button("💾 Lưu cuộc họp")
        if submit_hop:
            if ten_hop and noidung_hop:
                try:
                    file_names = []
                    for f in files_hop:
                        file_path = os.path.join(UPLOAD_FOLDER, f.name)
                        with open(file_path, "wb") as out:
                            out.write(f.read())
                        file_names.append(f.name)
                    new_row_hop = {
                        "Ngày": ngay_hop.strftime("%d/%m/%y"),
                        "Giờ": gio_hop.strftime("%H:%M"),
                        "Tên cuộc họp": ten_hop,
                        "Nội dung": noidung_hop,
                        "Tệp": ";".join(file_names)
                    }
                    df_lich_su_hop = pd.read_csv(MEETINGS_FILE) if os.path.exists(MEETINGS_FILE) else pd.DataFrame(columns=["Ngày", "Giờ", "Tên cuộc họp", "Nội dung", "Tệp"])
                    df_lich_su_hop = pd.concat([df_lich_su_hop, pd.DataFrame([new_row_hop])], ignore_index=True)
                    df_lich_su_hop.to_csv(MEETINGS_FILE, index=False)
                    st.success("✅ Đã lưu cuộc họp.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Lỗi khi lưu cuộc họp: {e}")
            else:
                st.warning("⚠️ Vui lòng nhập 'Tên cuộc họp' và 'Nội dung'.")

    # Hiển thị & Xoá họp
    if os.path.exists(MEETINGS_FILE):
        st.subheader("📚 Danh sách cuộc họp")
        try:
            df_lich_su_hop_display = pd.read_csv(MEETINGS_FILE, dtype=str)
            if not df_lich_su_hop_display.empty:
                for idx, row in df_lich_su_hop_display.iterrows():
                    with st.expander(f"📌 {row['Tên cuộc họp']} – {row['Ngày']} {row['Giờ']}"):
                        st.write("📝", row["Nội dung"])
                        file_list_hop = str(row.get("Tệp", "")).split(";")
                        for file_name_hop in file_list_hop:
                            file_path_hop = os.path.join(UPLOAD_FOLDER, file_name_hop)
                            if os.path.exists(file_path_hop) and file_name_hop:
                                st.write(f"📎 {file_name_hop}")
                                with open(file_path_hop, "rb") as f_hop:
                                    st.download_button("⬇️ Tải", f_hop.read(), file_name=file_name_hop, key=f"dl_hop_{idx}_{file_name_hop}")
                        with st.form(f"form_xoa_hop_{idx}"):
                            confirm_hop = st.checkbox("🗑️ Xác nhận xóa cuộc họp này", key=f"xoa_ck_hop_{idx}")
                            do_delete_hop = st.form_submit_button("❗ Xác nhận xoá")
                            if confirm_hop and do_delete_hop:
                                df_lich_su_hop_display.drop(index=idx, inplace=True)
                                df_lich_su_hop_display.to_csv(MEETINGS_FILE, index=False)
                                st.success("🗑️ Đã xoá cuộc họp.")
                                st.rerun()
            else:
                st.info("Chưa có cuộc họp nào được lưu.")
        except pd.errors.EmptyDataError:
            st.info("File lịch sử họp trống. Hãy thêm một cuộc họp mới.")
        except Exception as e:
            st.error(f"❌ Lỗi khi hiển thị cuộc họp: {e}")

    # Xuất / Nhập Excel (Phục vụ họp)
    st.markdown("### 📤 Xuất / Nhập Excel (Phục vụ họp)")
    col_export_hop, col_import_hop = st.columns(2)

    with col_export_hop:
        if os.path.exists(MEETINGS_FILE):
            df_export_hop = pd.read_csv(MEETINGS_FILE)
            towrite_hop = io.BytesIO()
            with pd.ExcelWriter(towrite_hop, engine='xlsxwriter') as writer:
                df_export_hop.to_excel(writer, index=False, sheet_name='CuocHop')
            towrite_hop.seek(0)
            st.download_button("  Tải Excel cuộc họp", data=towrite_hop, file_name="phuc_vu_hop.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    with col_import_hop:
        file_hop = st.file_uploader("📁 Nhập từ Excel (Phục vụ họp)", type=["xlsx"], key="upload_hop")
        if file_hop:
            try:
                df_import_hop = pd.read_excel(file_hop, dtype=str)
                df_import_hop.to_csv(MEETINGS_FILE, index=False)
                st.success("✅ Đã nhập lại danh sách cuộc họp.")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Lỗi khi nhập file Excel cuộc họp: {e}")

elif chon_modul == '📍 Dự báo điểm sự cố':
    st.title("📍 Dự báo điểm sự cố")

    # ===== QUẢN LÝ DỮ LIỆU SỰ CỐ TỪ FILE EXCEL CỤC BỘ =====
    STORAGE_FILE_SUCO = "storage_bao_cao_su_co.xlsx" # Đã định nghĩa ở trên, nhưng giữ lại để rõ ràng

    uploaded_excel_suco = st.file_uploader("📥 Tải dữ liệu lịch sử từ file Excel (.xlsx)", type="xlsx", key="upload_suco_data")

    # Chỉ xử lý file nếu có file mới được tải lên và chưa được xử lý trong lần chạy này
    if uploaded_excel_suco is not None and not st.session_state.file_uploaded_flag_suco:
        try:
            df_uploaded_suco = pd.read_excel(uploaded_excel_suco)
            st.session_state.suco_data = df_uploaded_suco.to_dict(orient="records")
            # Ghi dữ liệu mới vào file lưu trữ để duy trì
            pd.DataFrame(st.session_state.suco_data).to_excel(STORAGE_FILE_SUCO, index=False)
            st.success("✅ Đã ghi và nạp dữ liệu sự cố từ file thành công. Ứng dụng sẽ tải lại để áp dụng.")
            st.session_state.file_uploaded_flag_suco = True # Đặt cờ để ngăn xử lý lại ngay lập tức
            st.rerun() # GỌI st.rerun() TẠI ĐÂY để đảm bảo trạng thái nhất quán sau khi upload
        except Exception as e:
            st.warning(f"⚠️ Không thể xử lý file đã tải lên: {e}. Vui lòng kiểm tra định dạng file.")
            st.session_state.suco_data = [] # Reset về danh sách trống nếu quá trình upload/xử lý lỗi
            st.session_state.file_uploaded_flag_suco = False # Reset cờ để cho phép thử lại
    # Nếu file uploader rỗng (ví dụ: sau khi rerun, hoặc người dùng đã xóa file), đặt lại cờ
    elif uploaded_excel_suco is None:
        st.session_state.file_uploaded_flag_suco = False


    # Đảm bảo file KMZ luôn được xử lý độc lập
    marker_locations = {}
    kmz_file = st.file_uploader("  Tải file KMZ để lấy dữ liệu tọa độ cột", type="kmz")
    if kmz_file is not None:
        try:
            with zipfile.ZipFile(kmz_file, 'r') as z:
                for filename in z.namelist():
                    if filename.endswith('.kml'):
                        with z.open(filename) as f:
                            tree = ET.parse(f)
                            root = tree.getroot()
                            ns = {'kml': 'http://www.opengis.net/kml/2.2'}
                            for pm in root.findall('.//kml:Placemark', ns):
                                name_tag = pm.find('kml:name', ns)
                                point = pm.find('.//kml:Point/kml:coordinates', ns)
                                if name_tag is not None and point is not None:
                                    name = name_tag.text.strip()
                                    coords = point.text.strip().split(',')
                                    lon, lat = float(coords[0]), float(coords[1])
                                    marker_locations[name] = (lat, lon)
            st.success(f"✅ Đã trích xuất {len(marker_locations)} điểm từ file KMZ.")
        except Exception as e:
            st.error(f"❌ Lỗi khi đọc file KMZ: {e}. Đảm bảo file KMZ hợp lệ và chứa KML có Placemark/Point/coordinates.")

    st.subheader("📝 Nhập các vụ sự cố lịch sử")

    # Form nhập sự cố mới
    # Để khắc phục lỗi "Missing Submit Button", bạn cần đảm bảo st.form_submit_button được đặt bên trong st.form

    with st.form(key="my_form"):
        ten_mc = st.text_input("Tên máy cắt")
        ngay = st.date_input("Ngày xảy ra sự cố")
        dong_suco = st.text_input("Dòng sự cố")
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
        vi_tri = st.text_input("Vị trí sự cố")
        nguyen_nhan = st.text_input("Nguyên nhân")
        thoi_tiet = st.text_input("Thời tiết")

        submitted = st.form_submit_button("Lưu vụ sự cố")

    if submitted:
        if ten_mc and dong_suco and vi_tri:
            st.success("✔️ Đã lưu vụ sự cố!")
        else:
            st.warning("⚠️ Vui lòng điền đầy đủ các trường bắt buộc.")

        # Luôn tạo DataFrame cho data_editor, ngay cả khi st.session_state.suco_data trống
    df_for_editor = pd.DataFrame(st.session_state.suco_data)

    with st.expander("📋 Danh sách sự cố đã nhập", expanded=True):
        # BEGIN FIX FOR INDENTATION ERROR
        if not df_for_editor.empty:
            edited_df_suco = st.data_editor(
                df_for_editor,
                num_rows="dynamic",
                use_container_width=True,
                key="suco_data_editor"
            )

            if st.button("Cập nhật dữ liệu đã sửa", key="update_edited_suco"):
                st.session_state.suco_data = edited_df_suco.to_dict(orient="records")
                st.success("✔️ Đã cập nhật danh sách sau khi chỉnh sửa!")
                pd.DataFrame(st.session_state.suco_data).to_excel(STORAGE_FILE_SUCO, index=False)

            def convert_df_to_excel(df):
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, sheet_name='SuCo', index=False)
                return output.getvalue()

            st.download_button(
                label="📤 Xuất báo cáo Excel",
                data=convert_df_to_excel(edited_df_suco),
                file_name="bao_cao_su_co.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_suco_excel"
            )
        else:
            st.info("Chưa có sự cố nào được nhập. Vui lòng nhập dữ liệu sự cố ở trên để hiển thị tại đây.")
        # END FIX FOR INDENTATION ERROR


    # ============================
    # TÍNH TOÁN KHOẢNG CÁCH SỰ CỐ
    # ============================
    def extract_current(dong_suco_str, loai_suco):
        """Trích xuất dòng sự cố từ chuỗi nhập vào."""
        try:
            # Tìm tất cả các số trong chuỗi
            values = re.findall(r'\d+', dong_suco_str)
            values = [int(v) for v in values]
            if not values:
                return None
            if "Io" in loai_suco:
                # Nếu loại sự cố có Io, giả định Io là giá trị cuối cùng được nhập
                return values[-1]
            else:
                # Ngược lại, tính tổng các dòng pha
                return sum(values)
        except:
            return None

    def tinh_khoang_cach(I_suco, U0_V, z_ohm_per_km):
        """Tính khoảng cách dự kiến đến điểm sự cố."""
        try:
            if I_suco == 0 or z_ohm_per_km == 0: return None
            return round((U0_V / (I_suco * z_ohm_per_km)), 2)
        except:
            return None

    st.subheader("🔍 Dự báo điểm sự cố từ dòng điện")
    ten_mc_input = st.text_input("Tên máy cắt muốn dự báo", key="ten_mc_du_bao")
    dong_input = st.text_input("Dòng sự cố (ví dụ: Ia=500, Ib=600, Ic=50, Io=400)", key="dong_suco_du_bao")
    cap_dien_ap = st.selectbox("Cấp điện áp đường dây", ["22kV", "35kV", "110kV"], key="cap_dien_ap_du_bao")
    z_default = 4.0  # suất trở hỗn hợp đã cập nhật theo yêu cầu
    loai_suco_input = st.selectbox("Loại sự cố (để tính toán)", [
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
    ], key="loai_suco_input_du_bao")

    if st.button("Phân tích dòng sự cố", key="phan_tich_dong_suco"):
        U0_map = {"22kV": 22000 / math.sqrt(3), "35kV": 35000 / math.sqrt(3), "110kV": 110000 / math.sqrt(3)}
        I = extract_current(dong_input, loai_suco_input)
        if I is not None:
            d = tinh_khoang_cach(I, U0_map[cap_dien_ap], z_default)
            if d is not None:
                st.success(f"✅ Khoảng cách dự kiến đến điểm sự cố: {d} km")
            else:
                st.warning("⚠️ Không tính được khoảng cách. Dòng sự cố hoặc suất trở có thể bằng 0.")
        else:
            st.warning("⚠️ Không nhận diện được dòng sự cố hợp lệ từ 'Dòng sự cố' đã nhập.")

    # BỔ SUNG: Dự báo từ dữ liệu lịch sử (Sử dụng dữ liệu từ session_state.suco_data)
    st.subheader("📚 Dự báo điểm sự cố từ dữ liệu lịch sử")
    ten_mc_ls = st.text_input("🔎 Nhập tên máy cắt để lọc dữ liệu (Lịch sử)", key="ten_mc_ls_filter")
    dong_moi = st.text_input("Nhập dòng sự cố mới (Ia, Ib, Ic, Io) để tìm lịch sử", key="dong_moi_ls")
    if dong_moi:
        try:
            # Chuyển đổi chuỗi dòng sự cố mới thành danh sách số
            input_values = [int(x.strip()) for x in re.findall(r'\d+', dong_moi)]

            def euclidean(a, b):
                # Đảm bảo hai danh sách có cùng độ dài trước khi tính toán
                if len(a) != len(b):
                    return float('inf') # Trả về vô cực nếu độ dài không khớp để không chọn
                return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

            min_dist = float('inf')
            nearest_case = None

            if st.session_state.suco_data: # Chỉ lặp nếu có dữ liệu lịch sử
                for case in st.session_state.suco_data:
                    try:
                        # Lọc theo tên máy cắt nếu được nhập
                        if ten_mc_ls and ten_mc_ls.lower() not in case.get("Tên máy cắt", "").lower():
                            continue
                        # Trích xuất dòng sự cố từ trường 'Dòng sự cố' trong lịch sử
                        case_values = [int(x.strip()) for x in re.findall(r'\d+', case.get("Dòng sự cố", ""))]
                        if case_values: # Chỉ tính toán nếu có giá trị
                            dist = euclidean(input_values, case_values)
                            if dist < min_dist:
                                min_dist = dist
                                nearest_case = case
                    except Exception as e:
                        # st.warning(f"Lỗi xử lý dữ liệu lịch sử: {e} trong vụ sự cố {case}") # Gỡ bỏ để tránh nhiều lỗi nhỏ
                        continue # Bỏ qua vụ sự cố bị lỗi định dạng

            if nearest_case:
                st.success(f"✅ Dự báo gần nhất theo lịch sử: {nearest_case['Vị trí']} – Nguyên nhân: {nearest_case['Nguyên nhân']} – Dòng sự cố lịch sử: {nearest_case['Dòng sự cố']}")
            else:
                st.warning("⚠️ Không tìm thấy dòng sự cố tương đồng trong dữ liệu lịch sử hoặc dữ liệu lịch sử trống. Hãy thử nhập nhiều dữ liệu hơn.")
        except Exception as e:
            st.warning(f"⚠️ Định dạng dòng sự cố mới không hợp lệ. Vui lòng nhập theo dạng: 500, 600, 50, 400. Lỗi: {e}")

    # ============================
    # TIỆN ÍCH: DỰ BÁO THEO ĐIỀU KIỆN CHỌN (CÓ GHI NHỚ FILE SAU F5)
    # ============================
    st.markdown("---")
    st.subheader("📈 Dự báo điểm sự cố theo điều kiện chọn")

    DATA_FILE_PATH_TRA_CUU = "du_bao_su_co_day_du_voi_3uo.xlsx"
    TEMP_UPLOAD_PATH_TRA_CUU = "uploaded_tra_cuu.xlsx"

    df_tra_cuu = None
    uploaded_file_tra_cuu = st.file_uploader("📁 Tải file Excel dự báo (có thể thay đổi z')", type=["xlsx"], key="tra_cuu_file_uploader")

    if uploaded_file_tra_cuu:
        with open(TEMP_UPLOAD_PATH_TRA_CUU, "wb") as f:
            f.write(uploaded_file_tra_cuu.read())
        df_tra_cuu = pd.read_excel(TEMP_UPLOAD_PATH_TRA_CUU)
        st.success("✅ Đã ghi và nạp dữ liệu tra cứu từ file thành công.")
        st.dataframe(df_tra_cuu, use_container_width=True)
    elif os.path.exists(TEMP_UPLOAD_PATH_TRA_CUU):
        df_tra_cuu = pd.read_excel(TEMP_UPLOAD_PATH_TRA_CUU)
        st.dataframe(df_tra_cuu, use_container_width=True)
    else:
        try:
            df_tra_cuu = pd.read_excel(DATA_FILE_PATH_TRA_CUU)
            st.dataframe(df_tra_cuu, use_container_width=True)
        except FileNotFoundError:
            st.warning(f"❌ Không tìm thấy file mẫu '{DATA_FILE_PATH_TRA_CUU}'.")

    if df_tra_cuu is not None and not df_tra_cuu.empty:
        with st.expander("🔍 Tra cứu theo điều kiện chọn"):
            col1, col2 = st.columns(2)

            with col1:
                selected_line = st.selectbox("🔌 Chọn đường dây", sorted(df_tra_cuu["Đường dây"].unique()))
                selected_fault = st.selectbox("⚡ Chọn loại sự cố", sorted(df_tra_cuu["Loại sự cố"].unique()))

            with col2:
                Ia = st.number_input("Ia (A)", min_value=0)
                Ib = st.number_input("Ib (A)", min_value=0)
                Ic = st.number_input("Ic (A)", min_value=0)
                Io = st.number_input("Io (A)", min_value=0)
                Uo3 = st.number_input("3Uo (A)", min_value=0)

            if st.button("🔍 Tra cứu"):
                input_sum = sum([v for v in [Ia, Ib, Ic, Io, Uo3] if v > 0])

                if input_sum == 0:
                    st.warning("⚠️ Vui lòng nhập ít nhất một dòng sự cố để tra cứu.")
                else:
                    df_tra_cuu["Dòng tổng (A)"] = pd.to_numeric(df_tra_cuu["Dòng tổng (A)"], errors='coerce')
                    df_temp = df_tra_cuu.dropna(subset=["Dòng tổng (A)"])

                    if not df_temp.empty:
                        closest_idx = df_temp["Dòng tổng (A)"].sub(input_sum).abs().idxmin()
                        dong_co_so_found = df_temp.loc[closest_idx, "Dòng cơ sở (A)"]

                        ket_qua = df_tra_cuu[
                            (df_tra_cuu["Đường dây"] == selected_line) &
                            (df_tra_cuu["Loại sự cố"] == selected_fault) &
                            (df_tra_cuu["Dòng cơ sở (A)"] == dong_co_so_found)
                        ]

                        if not ket_qua.empty:
                            st.success(f"✅ Dòng gần nhất: {int(input_sum)} A → Dòng cơ sở: {int(dong_co_so_found)} A")
                            st.dataframe(ket_qua.reset_index(drop=True), use_container_width=True)
                        else:
                            st.warning("⚠️ Không tìm thấy kết quả phù hợp với các điều kiện đã chọn.")
                    else:
                        st.warning("⚠️ Không có dữ liệu hợp lệ để tra cứu.")

# ================== MODULE AI TRỢ LÝ TỔN THẤT ==================
elif chon_modul == '⚡ AI Trợ lý tổn thất':
    st.title("📥 AI Trợ lý tổn thất")

    # Các nút điều hướng chính cho module tổn thất
    st.markdown("### Chọn loại tổn thất để phân tích:")
    with st.expander("🔌 Tổn thất các TBA công cộng", expanded=True):
        st.header("Phân tích dữ liệu TBA công cộng")
        # ID thư mục Google Drive chứa file Excel TBA
        FOLDER_ID_TBA = '165Txi8IyqG50uFSFHzWidSZSG9qpsbaq' # Cập nhật ID thư mục nếu cần

        col_tba_1, col_tba_2, col_tba_3 = st.columns(3)
        with col_tba_1:
            mode_tba = st.radio("Chế độ phân tích", ["Theo tháng", "Lũy kế", "So sánh cùng kỳ", "Lũy kế cùng kỳ"], key="tba_mode")
        with col_tba_2:
            thang_from_tba = st.selectbox("Từ tháng", list(range(1, 13)), index=0, key="tba_thang_from")
            thang_to_options_tba = list(range(thang_from_tba, 13))
            default_index_thang_to_tba = 0
            if "Lũy kế" in mode_tba:
                if 5 in thang_to_options_tba:
                    default_index_thang_to_tba = thang_to_options_tba.index(5)
                elif len(thang_to_options_tba) > 4:
                     default_index_thang_to_tba = 4
                else:
                     default_index_thang_to_tba = len(thang_to_options_tba) - 1 if thang_to_options_tba else 0 # Ensure default_index is not None
                thang_to_tba = st.selectbox("Đến tháng", thang_to_options_tba, index=default_index_thang_to_tba, key="tba_thang_to")
            else:
                thang_to_tba = thang_from_tba

        with col_tba_3:
            nam_tba = st.selectbox("Chọn năm", list(range(2020, datetime.now().year + 1))[::-1], index=0, key="tba_nam")
            nam_cungkỳ_tba = nam_tba - 1 if "cùng kỳ" in mode_tba.lower() else None

        nguong_display_tba = st.selectbox("Ngưỡng tổn thất", ["(All)", "<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%", ">=5 và <7%", ">=7%"], key="tba_nguong_display")

        all_files_tba = list_excel_files_from_folder(FOLDER_ID_TBA)

        # Load current year data
        files_tba = generate_filenames(nam_tba, thang_from_tba, thang_to_tba, "TBA")
        df_tba_raw = load_data_from_drive(files_tba, all_files_tba, "Thực hiện")

        df_tba = pd.DataFrame() # Initialize df_tba as an empty DataFrame for final processed data
        
        # Process current year data (Thực hiện)
        if not df_tba_raw.empty:
            required_cols_raw = ["Tên TBA", "Điện nhận", "Điện tổn thất"]
            if all(col in df_tba_raw.columns for col in required_cols_raw):
                df_tba_raw["Điện nhận"] = pd.to_numeric(df_tba_raw["Điện nhận"].astype(str).str.replace(',', '.'), errors='coerce')
                df_tba_raw["Điện tổn thất"] = pd.to_numeric(df_tba_raw["Điện tổn thất"].astype(str).str.replace(',', '.'), errors='coerce')
                df_tba_raw.dropna(subset=["Điện nhận", "Điện tổn thất"], inplace=True)

                if "Lũy kế" in mode_tba:
                    df_tba_agg = df_tba_raw.groupby(["Tên TBA", "Kỳ"]).agg(
                        Tong_Dien_Nhan=('Điện nhận', 'sum'),
                        Tong_Dien_Ton_That=('Điện tổn thất', 'sum')
                    ).reset_index()
                    df_tba_agg["Tỷ lệ tổn thất"] = (df_tba_agg["Tong_Dien_Ton_That"] / df_tba_agg["Tong_Dien_Nhan"] * 100).round(2)
                    df_tba = df_tba_agg.rename(columns={'Tong_Dien_Nhan': 'Điện nhận', 'Tong_Dien_Ton_That': 'Điện tổn thất'})
                else:
                    if "Tỷ lệ tổn thất" in df_tba_raw.columns:
                        df_tba_raw["Tỷ lệ tổn thất"] = pd.to_numeric(df_tba_raw["Tỷ lệ tổn thất"].astype(str).str.replace(',', '.'), errors='coerce')
                    else:
                        df_tba_raw["Tỷ lệ tổn thất"] = (df_tba_raw["Điện tổn thất"] / df_tba_raw["Điện nhận"] * 100).round(2)
                    df_tba = df_tba_raw
            else:
                missing_cols = [col for col in required_cols_raw if col not in df_tba_raw.columns]
                st.error(f"Lỗi: Dữ liệu TBA 'Thực hiện' thiếu các cột cần thiết ({', '.join(missing_cols)}). Vui lòng kiểm tra cấu trúc file Excel.")
                df_tba = pd.DataFrame(columns=["Tên TBA", "Kỳ", "Tỷ lệ tổn thất", "Ngưỡng tổn thất"])

        # Load and process previous year data (Cùng kỳ)
        df_ck_tba = pd.DataFrame() # Initialize df_ck_tba as an empty DataFrame for processed data
        if "cùng kỳ" in mode_tba.lower() and nam_cungkỳ_tba:
            files_ck_tba = generate_filenames(nam_cungkỳ_tba, thang_from_tba, thang_to_tba, "TBA")
            df_ck_tba_raw = load_data_from_drive(files_ck_tba, all_files_tba, "Cùng kỳ")
            if not df_ck_tba_raw.empty:
                required_cols_ck = ["Tên TBA", "Điện nhận", "Điện tổn thất"]
                if all(col in df_ck_tba_raw.columns for col in required_cols_ck):
                    df_ck_tba_raw["Điện nhận"] = pd.to_numeric(df_ck_tba_raw["Điện nhận"].astype(str).str.replace(',', '.'), errors='coerce')
                    df_ck_tba_raw["Điện tổn thất"] = pd.to_numeric(df_ck_tba_raw["Điện tổn thất"].astype(str).str.replace(',', '.'), errors='coerce')
                    df_ck_tba_raw.dropna(subset=["Điện nhận", "Điện tổn thất"], inplace=True)

                    if "Lũy kế" in mode_tba: # This condition now correctly applies to "Lũy kế cùng kỳ"
                        df_ck_tba_agg = df_ck_tba_raw.groupby(["Tên TBA", "Kỳ"]).agg(
                            Tong_Dien_Nhan=('Điện nhận', 'sum'),
                            Tong_Dien_Ton_That=('Điện tổn thất', 'sum')
                        ).reset_index()
                        df_ck_tba_agg["Tỷ lệ tổn thất"] = (df_ck_tba_agg["Tong_Dien_Ton_That"] / df_ck_tba_agg["Tong_Dien_Nhan"] * 100).round(2)
                        df_ck_tba = df_ck_tba_agg.rename(columns={'Tong_Dien_Nhan': 'Điện nhận', 'Tong_Dien_Ton_That': 'Điện tổn thất'})
                    else: # For "So sánh cùng kỳ" (monthly)
                        if "Tỷ lệ tổn thất" in df_ck_tba_raw.columns:
                            df_ck_tba_raw["Tỷ lệ tổn thất"] = pd.to_numeric(df_ck_tba_raw["Tỷ lệ tổn thất"].astype(str).str.replace(',', '.'), errors='coerce')
                        else:
                            df_ck_tba_raw["Tỷ lệ tổn thất"] = (df_ck_tba_raw["Điện tổn thất"] / df_ck_tba_raw["Điện nhận"] * 100).round(2)
                        df_ck_tba = df_ck_tba_raw
                else:
                    missing_cols = [col for col in required_cols_ck if col not in df_ck_tba_raw.columns]
                    st.error(f"Lỗi: Dữ liệu TBA 'Cùng kỳ' thiếu các cột cần thiết ({', '.join(missing_cols)}). Vui lòng kiểm tra cấu trúc file Excel.")
                    df_ck_tba = pd.DataFrame(columns=["Tên TBA", "Kỳ", "Tỷ lệ tổn thất", "Ngưỡng tổn thất"])
            
        # Concatenate df_tba and df_ck_tba if df_ck_tba has data
        if not df_ck_tba.empty and not df_tba.empty: # Only concatenate if both have data
            df_tba = pd.concat([df_tba, df_ck_tba])
        elif df_ck_tba.empty and df_tba.empty: # If both are empty, keep df_tba empty
            df_tba = pd.DataFrame()
        elif not df_ck_tba.empty and df_tba.empty: # If only df_ck_tba has data, use it
            df_tba = df_ck_tba


        # Ensure 'Tỷ lệ tổn thất' is numeric and handle missing values
        if not df_tba.empty and "Tỷ lệ tổn thất" in df_tba.columns:
            df_tba["Tỷ lệ tổn thất"] = pd.to_numeric(df_tba["Tỷ lệ tổn thất"].astype(str).str.replace(',', '.'), errors='coerce')
            
            # Define all possible categories for 'Ngưỡng tổn thất'
            loss_categories = ["<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%", ">=5 và <7%", ">=7%"]
            # Convert 'Ngưỡng tổn thất' to a Categorical type with all defined categories
            df_tba["Ngưỡng tổn thất"] = df_tba["Tỷ lệ tổn thất"].apply(classify_nguong)
            df_tba["Ngưỡng tổn thất"] = pd.Categorical(df_tba["Ngưỡng tổn thất"], categories=loss_categories, ordered=True)

            # Ensure "Tên TBA" and "Kỳ" exist before dropping duplicates
            required_tba_columns_for_unique = ["Tên TBA", "Kỳ"]
            if all(col in df_tba.columns for col in required_tba_columns_for_unique):
                df_unique_tba = df_tba.drop_duplicates(subset=["Tên TBA", "Kỳ"])
            else:
                st.error(f"Lỗi: Dữ liệu TBA thiếu các cột cần thiết để xác định TBA duy nhất ({', '.join(required_tba_columns_for_unique)}).")
                df_unique_tba = pd.DataFrame(columns=["Tên TBA", "Kỳ", "Tỷ lệ tổn thất", "Ngưỡng tổn thất"]) # Provide a fallback empty DataFrame

            if not df_unique_tba.empty:
                # Group by and pivot. The categorical type will ensure all categories are present.
                count_df_tba = df_unique_tba.groupby(["Ngưỡng tổn thất", "Kỳ"], observed=False).size().reset_index(name="Số lượng")
                pivot_df_tba = count_df_tba.pivot(index="Ngưỡng tổn thất", columns="Kỳ", values="Số lượng").fillna(0).astype(int)
                # The reindex is no longer strictly necessary here if the categorical type is handled correctly,
                # but keeping it ensures the order.
                pivot_df_tba = pivot_df_tba.reindex(loss_categories) # Reindex to ensure all categories are present, even if 0

                # Tăng DPI và điều chỉnh fontsize
                fig_tba, (ax_bar_tba, ax_pie_tba) = plt.subplots(1, 2, figsize=(12, 5), dpi=1200) # Tăng figsize và DPI

                x_tba = range(len(pivot_df_tba))
                width_tba = 0.35
                colors_tba = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
                for i, col in enumerate(pivot_df_tba.columns):
                    offset_tba = (i - (len(pivot_df_tba.columns)-1)/2) * width_tba
                    bars_tba = ax_bar_tba.bar([xi + offset_tba for xi in x_tba], pivot_df_tba[col], width_tba, label=col, color=colors_tba[i % len(colors_tba)])
                    for bar in bars_tba:
                        height = bar.get_height()
                        if height > 0:
                            ax_bar_tba.text(bar.get_x() + bar.get_width()/2, height + 0.5, f'{int(height)}', ha='center', va='bottom', fontsize=8, fontweight='bold', color='black') # Tăng fontsize

                ax_bar_tba.set_ylabel("Số lượng", fontsize=9) # Tăng fontsize
                ax_bar_tba.set_title("Số lượng TBA theo ngưỡng tổn thất", fontsize=11, weight='bold') # Tăng fontsize
                ax_bar_tba.set_xticks(list(x_tba))
                ax_bar_tba.set_xticklabels(pivot_df_tba.index, fontsize=8) # Tăng fontsize
                ax_bar_tba.tick_params(axis='y', labelsize=8) # Tăng labelsize
                ax_bar_tba.legend(title="Kỳ", fontsize=8) # Tăng fontsize
                ax_bar_tba.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.6)

                pie_data_tba = pd.Series(0, index=pivot_df_tba.index)
                if 'Thực hiện' in df_unique_tba['Kỳ'].unique():
                    df_latest_tba = df_unique_tba[df_unique_tba['Kỳ'] == 'Thực hiện']
                    pie_data_tba = df_latest_tba["Ngưỡng tổn thất"].value_counts().reindex(pivot_df_tba.index, fill_value=0)
                elif not df_unique_tba.empty and not pivot_df_tba.empty:
                    first_col_data_tba = pivot_df_tba.iloc[:, 0]
                    if first_col_data_tba.sum() > 0:
                        pie_data_tba = first_col_data_tba

                if pie_data_tba.sum() > 0:
                    wedges, texts, autotexts = ax_pie_tba.pie(
                        pie_data_tba,
                        labels=pivot_df_tba.index,
                        autopct='%1.1f%%',
                        startangle=90,
                        colors=colors_tba,
                        pctdistance=0.75,
                        wedgeprops={'width': 0.3, 'edgecolor': 'w'}
                    )
                    for text in texts: text.set_fontsize(7); text.set_fontweight('bold') # Tăng fontsize
                    for autotext in autotexts: autotext.set_color('black'); autotext.set_fontsize(7); autotext.set_fontweight('bold') # Tăng fontsize
                    ax_pie_tba.text(0, 0, f"Tổng số TBA\\n{pie_data_tba.sum()}", ha='center', va='center', fontsize=8, fontweight='bold', color='black') # Tăng fontsize
                    ax_pie_tba.set_title("Tỷ trọng TBA theo ngưỡng tổn thất", fontsize=11, weight='bold') # Tăng fontsize
                else:
                    ax_pie_tba.text(0.5, 0.5, "Không có dữ liệu tỷ trọng phù hợp", horizontalalignment='center', verticalalignment='center', transform=ax_pie_tba.transAxes, fontsize=9) # Tăng fontsize
                    ax_pie_tba.set_title("Tỷ trọng TBA theo ngưỡng tổn thất", fontsize=11, weight='bold') # Tăng fontsize

                st.pyplot(fig_tba)

                nguong_filter_tba = st.selectbox("Chọn ngưỡng để lọc danh sách TBA", ["(All)", "<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%", ">=5 và <7%", ">=7%"], key="tba_detail_filter")
                if nguong_filter_tba != "(All)":
                    df_filtered_tba = df_tba[df_tba["Ngưỡng tổn thất"] == nguong_filter_tba]
                else:
                    df_filtered_tba = df_tba

                st.markdown("### 📋 Danh sách chi tiết TBA")
                st.dataframe(df_filtered_tba.reset_index(drop=True), use_container_width=True)
            else:
                st.warning("Không có dữ liệu TBA duy nhất để hiển thị biểu đồ. Vui lòng kiểm tra dữ liệu đầu vào.")
        else:
            if df_tba.empty:
                st.warning("Không có dữ liệu TBA được tải về. Vui lòng kiểm tra các file Excel trên Google Drive và ID thư mục.")
            else:
                # This error message should be more general as df_tba might be empty due to issues in df_tba_raw or df_ck_tba_raw
                # The specific missing column checks are already handled above in the raw data processing.
                st.error("Lỗi: Không thể phân tích dữ liệu TBA. Vui lòng kiểm tra cấu trúc file Excel và đảm bảo có đủ dữ liệu.")

    with st.expander("⚡ Tổn thất hạ thế"):
        st.header("Phân tích dữ liệu tổn thất hạ thế")
        FOLDER_ID_HA = '1_rAY5T-unRyw20YwMgKuG1C0y7oq6GkK' # Cập nhật ID thư mục nếu cần

        all_files_ha = list_excel_files_from_folder(FOLDER_ID_HA)
        nam_ha = st.selectbox("Chọn năm", list(range(2020, datetime.now().year + 1))[::-1], index=0, key="ha_nam")
        loai_bc_ha = st.radio("Loại báo cáo", ["Tháng", "Lũy kế"], horizontal=True, key="ha_loai_bc")
        thang_ha = st.selectbox("Chọn tháng", list(range(1, 13)), index=0, key="ha_thang")

        months_ha = list(range(1, 13))
        df_th_ha = pd.DataFrame({"Tháng": months_ha, "Tỷ lệ": [None]*12})
        df_ck_ha = pd.DataFrame({"Tháng": months_ha, "Tỷ lệ": [None]*12})

        tong_ton_that_ha = 0
        tong_thuong_pham_ha = 0

        for i in range(1, 13):
            fname_ha = f"HA_{nam_ha}_{i:02}.xlsx"
            file_id_ha = all_files_ha.get(fname_ha)

            if file_id_ha and i <= thang_ha:
                df_curr_ha = download_excel_from_drive(file_id_ha)
                if not df_curr_ha.empty and df_curr_ha.shape[0] >= 1:
                    try:
                        ty_le_th_ha = float(str(df_curr_ha.iloc[0, 4]).replace(",", "."))
                        ton_that_ha = float(str(df_curr_ha.iloc[0, 3]).replace(",", "."))
                        thuong_pham_ha = float(str(df_curr_ha.iloc[0, 1]).replace(",", "."))

                        if loai_bc_ha == "Lũy kế":
                            tong_ton_that_ha += ton_that_ha
                            tong_thuong_pham_ha += thuong_pham_ha
                            ty_le_lk_ha = (tong_ton_that_ha / tong_thuong_pham_ha) * 100 if tong_thuong_pham_ha > 0 else 0
                            df_th_ha.loc[df_th_ha["Tháng"] == i, "Tỷ lệ"] = ty_le_lk_ha
                        else:
                            df_th_ha.loc[df_th_ha["Tháng"] == i, "Tỷ lệ"] = ty_le_th_ha
                    except Exception as e:
                        st.warning(f"Lỗi đọc dữ liệu từ file hạ thế: {fname_ha}. Lỗi: {e}")

            fname_ck_ha = f"HA_{nam_ha - 1}_{i:02}.xlsx"
            file_id_ck_ha = all_files_ha.get(fname_ck_ha)
            if file_id_ck_ha:
                df_ck_file_ha = download_excel_from_drive(file_id_ck_ha)
                if not df_ck_file_ha.empty and df_ck_file_ha.shape[0] >= 1:
                    try:
                        ty_le_ck_ha = float(str(df_ck_file_ha.iloc[0, 4]).replace(",", "."))
                        df_ck_ha.loc[df_ck_ha["Tháng"] == i, "Tỷ lệ"] = ty_le_ck_ha
                    except Exception as e:
                        # st.warning(f"Lỗi đọc dữ liệu cùng kỳ file hạ thế: {fname_ck_ha}. Lỗi: {e}") # Bỏ bớt thông báo lỗi nhỏ
                        pass

        if df_th_ha["Tỷ lệ"].notna().any():
            fig_ha, ax_ha = plt.subplots(figsize=(6, 3), dpi=600)

            ax_ha.plot(df_th_ha["Tháng"], df_th_ha["Tỷ lệ"], color='#1f77b4', label='Thực hiện', linewidth=1, markersize=3, marker='o')
            if df_ck_ha["Tỷ lệ"].notna().any():
                ax_ha.plot(df_ck_ha["Tháng"], df_ck_ha["Tỷ lệ"], color='#ff7f0e', label='Cùng kỳ', linewidth=1, markersize=3, marker='o')

            for i, v in df_th_ha.dropna(subset=["Tỷ lệ"]).iterrows():
                ax_ha.text(v["Tháng"], v["Tỷ lệ"] + 0.05, f"{v['Tỷ lệ']:.2f}", ha='center', fontsize=6, color='black')

            if df_ck_ha["Tỷ lệ"].notna().any():
                for i, v in df_ck_ha.dropna(subset=["Tỷ lệ"]).iterrows():
                    ax_ha.text(v["Tháng"], v["Tỷ lệ"] + 0.05, f"{v['Tỷ lệ']:.2f}", ha='center', fontsize=6, color='black')

            ax_ha.set_ylabel("Tỷ lệ (%)", fontsize=7, color='black')
            ax_ha.set_xlabel("Tháng", fontsize=7, color='black')
            ax_ha.set_xticks(months_ha)
            ax_ha.tick_params(axis='both', colors='black', labelsize=6)
            ax_ha.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
            ax_ha.set_title("Biểu đồ tỷ lệ tổn thất hạ thế", fontsize=9, color='black')
            ax_ha.legend(fontsize=7, frameon=False)

            st.pyplot(fig_ha)
            st.dataframe(df_th_ha.dropna(subset=["Tỷ lệ"]).reset_index(drop=True)) # Chỉ hiển thị dữ liệu có tỷ lệ

        else:
            st.warning("Không có dữ liệu phù hợp để hiển thị. Vui lòng kiểm tra các file Excel trên Google Drive (thư mục Hạ thế) và định dạng của chúng.")

    with st.expander("⚡ Tổn thất trung thế"):
        st.header("Phân tích dữ liệu TBA Trung thế")
        FOLDER_ID_TRUNG = '1-Ph2auxlinL5Y3bxE7AeeAeYE2KDALJT' # Cập nhật ID thư mục nếu cần

        all_files_trung = list_excel_files_from_folder(FOLDER_ID_TRUNG)
        nam_trung = st.selectbox("Chọn năm", list(range(2020, datetime.now().year + 1))[::-1], index=0, key="trung_nam")
        loai_bc_trung = st.radio("Loai báo cáo", ["Tháng", "Lũy kế"], horizontal=True, key="trung_loai_bc")
        thang_trung = st.selectbox("Chọn tháng", list(range(1, 13)), index=0, key="trung_thang")

        months_trung = list(range(1, 13))
        df_th_trung = pd.DataFrame({"Tháng": months_trung, "Tỷ lệ": [None]*12})
        df_ck_trung = pd.DataFrame({"Tháng": months_trung, "Tỷ lệ": [None]*12})

        tong_ton_that_trung = 0
        tong_thuong_pham_trung = 0

        # Khởi tạo tổng lũy kế cho dữ liệu "Cùng kỳ" (năm trước)
        tong_ton_that_ck_trung = 0
        tong_thuong_pham_ck_trung = 0

        for i in range(1, 13):
            # --- Xử lý dữ liệu năm hiện tại (Thực hiện) ---
            fname_trung = f"TA_{nam_trung}_{i:02}.xlsx"
            file_id_trung = all_files_trung.get(fname_trung)

            if file_id_trung and i <= thang_trung:
                df_curr_trung = download_excel_from_drive(file_id_trung)
                if not df_curr_trung.empty and df_curr_trung.shape[0] >= 1:
                    try:
                        ty_le_th_trung = float(str(df_curr_trung.iloc[0, 4]).replace(",", "."))
                        ton_that_trung = float(str(df_curr_trung.iloc[0, 3]).replace(",", "."))
                        thuong_pham_trung = float(str(df_curr_trung.iloc[0, 1]).replace(",", "."))

                        if loai_bc_trung == "Lũy kế":
                            tong_ton_that_trung += ton_that_trung
                            tong_thuong_pham_trung += thuong_pham_trung
                            ty_le_lk_trung = (tong_ton_that_trung / tong_thuong_pham_trung) * 100 if tong_thuong_pham_trung > 0 else 0
                            df_th_trung.loc[df_th_trung["Tháng"] == i, "Tỷ lệ"] = ty_le_lk_trung
                        else:
                            df_th_trung.loc[df_th_trung["Tháng"] == i, "Tỷ lệ"] = ty_le_th_trung
                    except Exception as e:
                        st.warning(f"Lỗi đọc dữ liệu từ file trung thế: {fname_trung}. Lỗi: {e}")

            # --- Xử lý dữ liệu "Cùng kỳ" (năm trước) ---
            fname_ck_trung = f"TA_{nam_trung - 1}_{i:02}.xlsx"
            file_id_ck_trung = all_files_trung.get(fname_ck_trung)
            # **Đã bỏ điều kiện `and i <= thang_trung` ở đây để vẽ cả năm cùng kỳ**
            if file_id_ck_trung:
                df_ck_file_trung = download_excel_from_drive(file_id_ck_trung)
                if not df_ck_file_trung.empty and df_ck_file_trung.shape[0] >= 1:
                    try:
                        # Đọc các giá trị tổn thất và thương phẩm của năm trước
                        ty_le_ck_trung_thang = float(str(df_ck_file_trung.iloc[0, 4]).replace(",", ".")) # Tỷ lệ tháng năm trước
                        ton_that_ck_trung = float(str(df_ck_file_trung.iloc[0, 3]).replace(",", ".")) # Tổn thất tháng năm trước
                        thuong_pham_ck_trung = float(str(df_ck_file_trung.iloc[0, 1]).replace(",", ".")) # Thương phẩm tháng năm trước

                        if loai_bc_trung == "Lũy kế":
                            # Tính lũy kế cho dữ liệu năm trước
                            tong_ton_that_ck_trung += ton_that_ck_trung
                            tong_thuong_pham_ck_trung += thuong_pham_ck_trung
                            ty_le_lk_ck_trung = (tong_ton_that_ck_trung / tong_thuong_pham_ck_trung) * 100 if tong_thuong_pham_ck_trung > 0 else 0
                            df_ck_trung.loc[df_ck_trung["Tháng"] == i, "Tỷ lệ"] = ty_le_lk_ck_trung
                        else:
                            # Nếu không phải lũy kế, dùng tỷ lệ tháng của năm trước
                            df_ck_trung.loc[df_ck_trung["Tháng"] == i, "Tỷ lệ"] = ty_le_ck_trung_thang
                    except Exception as e:
                        # st.warning(f"Lỗi đọc dữ liệu cùng kỳ file trung thế: {fname_ck_trung}. Lỗi: {e}")
                        pass # Suppress minor warnings for cleaner output

        if df_th_trung["Tỷ lệ"].notna().any():
            fig_trung, ax_trung = plt.subplots(figsize=(6, 3), dpi=600)

            ax_trung.plot(df_th_trung["Tháng"], df_th_trung["Tỷ lệ"], color='#1f77b4', label='Thực hiện', linewidth=1, markersize=3, marker='o')
            if df_ck_trung["Tỷ lệ"].notna().any():
                ax_trung.plot(df_ck_trung["Tháng"], df_ck_trung["Tỷ lệ"], color='#ff7f0e', label='Cùng kỳ', linewidth=1, markersize=3, marker='o')

            for i, v in df_th_trung.dropna(subset=["Tỷ lệ"]).iterrows():
                ax_trung.text(v["Tháng"], v["Tỷ lệ"] + 0.05, f"{v['Tỷ lệ']:.2f}", ha='center', fontsize=6, color='black')

            if df_ck_trung["Tỷ lệ"].notna().any():
                for i, v in df_ck_trung.dropna(subset=["Tỷ lệ"]).iterrows():
                    ax_trung.text(v["Tháng"], v["Tỷ lệ"] + 0.05, f"{v['Tỷ lệ']:.2f}", ha='center', fontsize=6, color='black')

            ax_trung.set_ylabel("Tỷ lệ (%)", fontsize=7, color='black')
            ax_trung.set_xlabel("Tháng", fontsize=7, color='black')
            ax_trung.set_xticks(months_trung)
            ax_trung.tick_params(axis='both', colors='black', labelsize=6)
            ax_trung.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
            ax_trung.set_title("Biểu đồ tỷ lệ tổn thất trung thế", fontsize=9, color='black')
            ax_trung.legend(fontsize=7, frameon=False)

            st.pyplot(fig_trung)
            st.dataframe(df_th_trung.dropna(subset=["Tỷ lệ"]).reset_index(drop=True))

        else:
            st.warning("Không có dữ liệu phù hợp để hiển thị. Vui lòng kiểm tra các file Excel trên Google Drive (thư mục Trung thế) và định dạng của chúng.")

    with st.expander("⚡ Tổn thất các đường dây trung thế"):
        st.header("Phân tích dữ liệu tổn thất đường dây trung thế")
        FOLDER_ID_DY = '1ESynjLXJrw8TaF3zwlQm-BR3mFf4LIi9' # Cập nhật ID thư mục nếu cần

        all_files_dy = list_excel_files_from_folder(FOLDER_ID_DY)

        all_years_dy = sorted({int(fname.split("_")[1]) for fname in all_files_dy.keys() if "_" in fname and len(fname.split("_")) == 3}) # Ensure filename format like DD_YYYY_MM.xlsx

        selected_year_dy = st.selectbox("Chọn năm", all_years_dy, key="dy_nam") if all_years_dy else None
        if not selected_year_dy:
            st.warning("Không có dữ liệu năm cho tổn thất đường dây trung thế.")
        else:
            include_cungkỳ_dy = st.checkbox("So sánh cùng kỳ năm trước", value=True, key="dy_cung_ky")
            mode_dy = st.radio("Chọn chế độ báo cáo", ["Tháng", "Lũy kế"], horizontal=True, key="dy_loai_bc")
            chart_type_dy = st.radio("Chọn kiểu biểu đồ", ["Cột", "Đường line"], horizontal=True, key="dy_chart_type")

            data_list_dy = []

            for fname, file_id in all_files_dy.items():
                try:
                    parts = fname.split("_")
                    if len(parts) == 3: # Expecting format like PREFIX_YYYY_MM.xlsx
                        year = int(parts[1])
                        month = int(parts[2].split(".")[0])
                    else:
                        continue # Skip files with unexpected naming conventions
                except ValueError:
                    continue

                if year == selected_year_dy or (include_cungkỳ_dy and year == selected_year_dy - 1):
                    df_curr_dy = download_excel_from_drive(file_id)

                    for idx, row in df_curr_dy.iterrows():
                        if len(row) > 5: # Ensure row has enough columns
                            ten_dd = str(row.iloc[1]).strip()
                            dien_ton_that = pd.to_numeric(str(row.iloc[5]).replace(",", "."), errors='coerce')
                            thuong_pham = pd.to_numeric(str(row.iloc[2]).replace(",", "."), errors='coerce')
                            ky = "Cùng kỳ" if year == selected_year_dy - 1 else "Thực hiện"

                            data_list_dy.append({
                                "Năm": year,
                                "Tháng": month,
                                "Đường dây": ten_dd,
                                "Điện tổn thất": dien_ton_that,
                                "Thương phẩm": thuong_pham,
                                "Kỳ": ky
                            })

            df_all_dy = pd.DataFrame(data_list_dy)
            df_all_dy.dropna(subset=["Điện tổn thất", "Thương phẩm"], inplace=True) # Remove rows with invalid numbers

            if not df_all_dy.empty:
                duong_day_list_dy = df_all_dy["Đường dây"].unique()

                for dd in duong_day_list_dy:
                    df_dd_filtered = df_all_dy[df_all_dy["Đường dây"] == dd].copy() # Use .copy() to avoid SettingWithCopyWarning

                    df_dd_filtered.sort_values("Tháng", inplace=True)

                    if mode_dy == "Lũy kế":
                        df_dd_filtered["Tổng Điện tổn thất"] = df_dd_filtered.groupby(["Kỳ"])["Điện tổn thất"].cumsum()
                        df_dd_filtered["Tổng Thương phẩm"] = df_dd_filtered.groupby(["Kỳ"])["Thương phẩm"].cumsum()
                        df_dd_filtered["Tổn thất (%)"] = (df_dd_filtered["Tổng Điện tổn thất"] / df_dd_filtered["Tổng Thương phẩm"] * 100).round(2)
                    else:
                        df_dd_filtered["Tổn thất (%)"] = (df_dd_filtered["Điện tổn thất"] / df_dd_filtered["Thương phẩm"] * 100).round(2)

                    # Removed .fillna(0) here to prevent plotting spurious zeros
                    pivot_df_dy = df_dd_filtered.pivot(index="Tháng", columns="Kỳ", values="Tổn thất (%)").reindex(range(1, 13))

                    st.write(f"### Biểu đồ tỷ lệ tổn thất - Đường dây {dd}")

                    fig_dy, ax_dy = plt.subplots(figsize=(10, 4), dpi=150)

                    if chart_type_dy == "Cột":
                        pivot_df_dy.plot(kind="bar", ax=ax_dy)
                        ax_dy.set_xticklabels(pivot_df_dy.index, rotation=0, ha='center')
                        ax_dy.tick_params(axis='y', labelrotation=0)
                        for container in ax_dy.containers:
                            for bar in container:
                                height = bar.get_height()
                                if height > 0:
                                    ax_dy.text(bar.get_x() + bar.get_width()/2, height + 0.2, f"{height:.2f}", ha='center', fontsize=7)
                    else:
                        for col in pivot_df_dy.columns:
                            # Only plot non-NaN values, keeping legitimate zeros
                            valid_data_dy = pivot_df_dy[col].dropna() # Changed from pivot_dy to pivot_df_dy
                            if not valid_data_dy.empty: # Check if there's any valid data to plot
                                ax_dy.plot(valid_data_dy.index, valid_data_dy.values, marker='o', label=col)
                                for x, y in zip(valid_data_dy.index, valid_data_dy.values):
                                    ax_dy.text(x, y + 0.2, f"{y:.2f}", ha='center', fontsize=7)
                        ax_dy.set_xticks(range(1, 13))
                        ax_dy.set_xticklabels(range(1, 13), rotation=0, ha='center')
                        ax_dy.tick_params(axis='y', labelrotation=0)

                    ax_dy.set_xlabel("Tháng")
                    ax_dy.set_ylabel("Tổn thất (%)")
                    ax_dy.set_title(f"Đường dây {dd} - Năm {selected_year_dy}")
                    ax_dy.legend()
                    ax_dy.grid(axis='y', linestyle='--', alpha=0.7)

                    st.pyplot(fig_dy, use_container_width=True)

            else:
                st.warning("Không có dữ liệu để hiển thị cho năm đã chọn hoặc đường dây đã lọc. Vui lòng kiểm tra lại dữ liệu trên Google Drive.")

    with st.expander("⚡ Tổn thất toàn đơn vị"):
        st.header("Phân tích dữ liệu toàn đơn vị")
        FOLDER_ID_TOAN_DON_VI = '1bPmINKlAHJMWUcxonMSnuLGz9ErlPEUi' # Cập nhật ID thư mục nếu cần

        all_files_dv = list_excel_files_from_folder(FOLDER_ID_TOAN_DON_VI)
        nam_dv = st.selectbox("Chọn năm", list(range(2020, datetime.now().year + 1))[::-1], index=0, key="dv_nam")
        loai_bc_dv = st.radio("Loại báo cáo", ["Tháng", "Lũy kế"], horizontal=True, key="dv_loai_bc")
        thang_dv = st.selectbox("Chọn tháng", list(range(1, 13)), index=0, key="dv_thang")

        months_dv = list(range(1, 13))
        df_th_dv = pd.DataFrame({"Tháng": months_dv, "Tỷ lệ": [None]*12})
        df_ck_dv = pd.DataFrame({"Tháng": months_dv, "Tỷ lệ": [None]*12})

        tong_ton_that_dv = 0
        tong_thuong_pham_dv = 0

        for i in range(1, 13):
            fname_dv = f"DV_{nam_dv}_{i:02}.xlsx"
            file_id_dv = all_files_dv.get(fname_dv)

            if file_id_dv and i <= thang_dv:
                df_curr_dv = download_excel_from_drive(file_id_dv)
                if not df_curr_dv.empty and df_curr_dv.shape[0] >= 1:
                    try:
                        ty_le_th_dv = float(str(df_curr_dv.iloc[0, 4]).replace(",", "."))
                        ton_that_dv = float(str(df_curr_dv.iloc[0, 3]).replace(",", "."))
                        thuong_pham_dv = float(str(df_curr_dv.iloc[0, 1]).replace(",", "."))

                        if loai_bc_dv == "Lũy kế":
                            tong_ton_that_dv += ton_that_dv
                            tong_thuong_pham_dv += thuong_pham_dv
                            ty_le_lk_dv = (tong_ton_that_dv / tong_thuong_pham_dv) * 100 if tong_thuong_pham_dv > 0 else 0
                            df_th_dv.loc[df_th_dv["Tháng"] == i, "Tỷ lệ"] = ty_le_lk_dv
                        else:
                            df_th_dv.loc[df_th_dv["Tháng"] == i, "Tỷ lệ"] = ty_le_th_dv
                    except Exception as e:
                        st.warning(f"Lỗi đọc dữ liệu từ file toàn đơn vị: {fname_dv}. Lỗi: {e}")

            fname_ck_dv = f"DV_{nam_dv - 1}_{i:02}.xlsx"
            file_id_ck_dv = all_files_dv.get(fname_ck_dv)
            if file_id_ck_dv:
                df_ck_file_dv = download_excel_from_drive(file_id_ck_dv)
                if not df_ck_file_dv.empty and df_ck_file_dv.shape[0] >= 1:
                    try:
                        ty_le_ck_dv = float(str(df_ck_file_dv.iloc[0, 4]).replace(",", "."))
                        df_ck_dv.loc[df_ck_dv["Tháng"] == i, "Tỷ lệ"] = ty_le_ck_dv
                    except Exception as e:
                        # st.warning(f"Lỗi đọc dữ liệu cùng kỳ file toàn đơn vị: {fname_ck_dv}. Lỗi: {e}") # Bỏ bớt thông báo lỗi nhỏ
                        pass

        if df_th_dv["Tỷ lệ"].notna().any():
            fig_dv, ax_dv = plt.subplots(figsize=(6, 3), dpi=600)

            ax_dv.plot(df_th_dv["Tháng"], df_th_dv["Tỷ lệ"], color='#1f77b4', label='Thực hiện', linewidth=1, markersize=3, marker='o')
            if df_ck_dv["Tỷ lệ"].notna().any():
                ax_dv.plot(df_ck_dv["Tháng"], df_ck_dv["Tỷ lệ"], color='#ff7f0e', label='Cùng kỳ', linewidth=1, markersize=3, marker='o')

            for i, v in df_th_dv.dropna(subset=["Tỷ lệ"]).iterrows():
                ax_dv.text(v["Tháng"], v["Tỷ lệ"] + 0.05, f"{v['Tỷ lệ']:.2f}", ha='center', fontsize=6, color='black')

            if df_ck_dv["Tỷ lệ"].notna().any():
                for i, v in df_ck_dv.dropna(subset=["Tỷ lệ"]).iterrows():
                    ax_dv.text(v["Tháng"], v["Tỷ lệ"] + 0.05, f"{v['Tỷ lệ']:.2f}", ha='center', fontsize=6, color='black')

            ax_dv.set_ylabel("Tỷ lệ (%)", fontsize=7, color='black')
            ax_dv.set_xlabel("Tháng", fontsize=7, color='black')
            ax_dv.set_xticks(months_dv)
            ax_dv.tick_params(axis='both', colors='black', labelsize=6)
            ax_dv.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
            ax_dv.set_title("Biểu đồ tỷ lệ tổn thất toàn đơn vị", fontsize=9, color='black')
            ax_dv.legend(fontsize=7, frameon=False)

            st.pyplot(fig_dv)
            st.dataframe(df_th_dv.dropna(subset=["Tỷ lệ"]).reset_index(drop=True))

        else:
            st.warning("Không có dữ liệu phù hợp để hiển thị. Vui lòng kiểm tra các file Excel trên Google Drive (thư mục Toàn đơn vị) và định dạng của chúng.")
 