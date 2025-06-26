# app_tba_congcong.py
import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
import os
import re

# Import các thư viện Google API
from googleapiclient.discovery import build
# Bạn có thể không cần các thư viện google.oauth2 và google.auth nếu chỉ dùng API Key cho folder công khai
# from google.oauth2.credentials import Credentials
# from google.auth.transport.requests import Request
# from google.auth.exceptions import RefreshError

st.set_page_config(layout="wide", page_title="Phân tích tổn thất TBA công cộng")
st.title("📊 Phân tích tổn thất các TBA công cộng")

# ==== CẤU HÌNH CHẾ ĐỘ PHÂN TÍCH ====
col1, col2, col3 = st.columns(3)

with col1:
    mode = st.radio("Chế độ phân tích", ["Theo tháng", "Lũy kế", "So sánh cùng kỳ", "Lũy kế cùng kỳ"])

with col2:
    thang_from = st.selectbox("Từ tháng", list(range(1, 13)), index=0)
    if "Lũy kế" in mode:
        thang_to = st.selectbox("Đến tháng", list(range(thang_from, 13)), index=4)
    else:
        thang_to = thang_from

with col3:
    nam = st.selectbox("Chọn năm", list(range(2020, datetime.now().year + 1))[::-1], index=0)

# ==== CẤU HÌNH GOOGLE DRIVE API ====
# Khóa API của bạn đã được thay thế vào đây
API_KEY = "AIzaSyB2sDczQAzYdi8ffFut3Ie0DluchLta4Ls" 

# ID của thư mục Google Drive công khai của bạn
# Chỉ lấy phần ID sau "folders/"
FOLDER_ID = "1o1O5jMhvJ6V2bqr6VdNoWTfXYiFYnl98"

# Hàm khởi tạo dịch vụ Google Drive API
@st.cache_resource # Sử dụng cache để tránh khởi tạo lại service mỗi lần chạy lại script
def get_drive_service(api_key):
    try:
        service = build('drive', 'v3', developerKey=api_key)
        st.success("Đã khởi tạo dịch vụ Google Drive API thành công.")
        return service
    except Exception as e:
        st.error(f"Lỗi khi khởi tạo dịch vụ Google Drive API: {e}. Vui lòng kiểm tra API Key của bạn.")
        return None

# ==== HÀM QUÉT DANH SÁCH FILE TRÊN GOOGLE DRIVE SỬ DỤNG API ====
def get_file_links_from_drive_api(service, folder_id):
    files = {}
    if not service:
        return files
    
    st.write(f"Đang tìm kiếm tệp trong thư mục Google Drive ID: {folder_id} bằng API.")
    try:
        # Tìm các tệp trong thư mục cụ thể, chỉ lấy tên và ID
        # q: Tìm kiếm các tệp có 'folder_id' trong parents và có mimeType là Excel
        # fields: chỉ định các trường cần lấy (file id và tên)
        results = service.files().list(
            q=f"'{folder_id}' in parents and (mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or mimeType='application/vnd.ms-excel')",
            fields="files(id, name)"
        ).execute()
        
        items = results.get('files', [])

        if not items:
            st.warning("Không tìm thấy tệp Excel nào trong thư mục Google Drive được chỉ định.")
        else:
            for item in items:
                file_name = item['name']
                file_id = item['id']
                files[file_name] = file_id
                st.write(f"  - Tìm thấy tệp: {file_name} (ID: {file_id})")
        st.write(f"Tổng số tệp Excel được xác định từ Drive (qua API): {len(files)}")
        return files
    except Exception as e:
        st.error(f"Lỗi khi lấy danh sách tệp từ Google Drive API: {e}. Vui lòng kiểm tra ID thư mục và quyền truy cập API.")
        return {}

# Hàm tải xuống Excel từ Google Drive API
def download_excel_from_drive_api(service, file_id):
    if not service:
        return pd.DataFrame()

    try:
        # Sử dụng API để tải nội dung tệp
        # Tệp lớn hơn 10MB cần dùng requests.get(download_url) thay vì service.files().get_media()
        # Đối với file Excel nhỏ, get_media là đủ.
        request = service.files().get_media(fileId=file_id)
        file_content = BytesIO(request.execute())
        
        df = pd.read_excel(file_content, sheet_name="dữ liệu")
        st.write(f"  - Đã tải dữ liệu thành công từ tệp ID {file_id}. Kích thước DataFrame: {df.shape}")
        return df
    except Exception as e:
        st.error(f"Lỗi khi tải hoặc đọc tệp Excel từ ID {file_id} qua API: {e}. Có thể tên sheet 'dữ liệu' không tồn tại hoặc tệp bị hỏng.")
        return pd.DataFrame()

# ==== HÀM PHÂN TÍCH (giữ nguyên, chỉ gọi các hàm API mới) ====
def generate_filenames(year, start_month, end_month):
    return [f"TBA_{year}_{str(m).zfill(2)}.xlsx" for m in range(start_month, end_month + 1)]

def load_data_from_drive(file_list, drive_files_map, drive_service): # Thêm drive_service
    dfs = []
    st.write(f"Đang tải dữ liệu cho các tệp: {file_list}")
    for file in file_list:
        file_id = drive_files_map.get(file)
        if file_id:
            st.write(f"Đang tải tệp: {file} (ID: {file_id})")
            df = download_excel_from_drive_api(drive_service, file_id) # Gọi hàm API mới
            if not df.empty:
                dfs.append(df)
            else:
                st.warning(f"Tệp '{file}' (ID: {file_id}) được tải về nhưng trống hoặc có lỗi khi đọc.")
        else:
            st.warning(f"Không tìm thấy ID cho tệp '{file}' trong danh sách tệp từ Google Drive. Tệp này có thể không tồn tại hoặc tên không khớp.")
    
    if dfs:
        combined_df = pd.concat(dfs)
        st.write(f"Đã kết hợp {len(dfs)} DataFrame. Kích thước DataFrame cuối cùng: {combined_df.shape}")
        return combined_df
    else:
        st.warning("Không có DataFrame nào được tải thành công từ các tệp đã chọn.")
        return pd.DataFrame()

# ==== XỬ LÝ CHÍNH ====
st.markdown("---")
st.write("Bắt đầu quá trình xử lý dữ liệu...")

# Khởi tạo dịch vụ Drive API
drive_service = get_drive_service(API_KEY)

# Lấy danh sách tệp từ Drive bằng API
drive_files_map = {}
if drive_service:
    drive_files_map = get_file_links_from_drive_api(drive_service, FOLDER_ID)
else:
    st.error("Không thể khởi tạo dịch vụ Google Drive API. Vui lòng kiểm tra API Key.")

if not drive_files_map:
    st.error("Không thể lấy danh sách tệp từ Google Drive. Vui lòng kiểm tra FOLDER_ID, API Key và quyền truy cập thư mục. Đảm bảo các tệp là Excel (.xlsx hoặc .xls).")
    df = pd.DataFrame() # Đảm bảo df trống nếu không lấy được file
else:
    st.write(f"Chế độ phân tích được chọn: {mode}")
    st.write(f"Năm: {nam}, Từ tháng: {thang_from}, Đến tháng: {thang_to}")

    df = pd.DataFrame() # Khởi tạo df rỗng để tránh lỗi nếu không vào được các điều kiện

    if mode == "Theo tháng":
        files = generate_filenames(nam, thang_from, thang_from)
        st.write(f"Tệp cần tìm cho chế độ 'Theo tháng': {files}")
        df = load_data_from_drive(files, drive_files_map, drive_service)

    elif mode == "Lũy kế":
        files = generate_filenames(nam, thang_from, thang_to)
        st.write(f"Các tệp cần tìm cho chế độ 'Lũy kế': {files}")
        df = load_data_from_drive(files, drive_files_map, drive_service)
        if not df.empty and "Tên TBA" in df.columns:
            st.write("Đang nhóm dữ liệu theo 'Tên TBA' cho chế độ 'Lũy kế'.")
            df = df.groupby("Tên TBA", as_index=False).sum(numeric_only=True)
        elif not df.empty and "Tên TBA" not in df.columns:
            st.warning("Cột 'Tên TBA' không tìm thấy trong dữ liệu cho chế độ 'Lũy kế'. Không thể nhóm dữ liệu.")

    elif mode == "So sánh cùng kỳ":
        files_now = generate_filenames(nam, thang_from, thang_from)
        files_last = generate_filenames(nam - 1, thang_from, thang_from)
        st.write(f"Tệp hiện tại ({nam}) cho chế độ 'So sánh cùng kỳ': {files_now}")
        st.write(f"Tệp năm trước ({nam-1}) cho chế độ 'So sánh cùng kỳ': {files_last}")
        df_now = load_data_from_drive(files_now, drive_files_map, drive_service)
        df_last = load_data_from_drive(files_last, drive_files_map, drive_service)
        if not df_now.empty and not df_last.empty:
            if "Tên TBA" in df_now.columns and "Tên TBA" in df_last.columns:
                st.write("Đang hợp nhất dữ liệu cho chế độ 'So sánh cùng kỳ'.")
                cols_to_sum = [col for col in df_now.columns if pd.api.types.is_numeric_dtype(df_now[col]) or col == "Tên TBA"]
                df_now_filtered = df_now[cols_to_sum]
                df_last_filtered = df_last[cols_to_sum]
                
                df = df_now_filtered.merge(df_last_filtered, on="Tên TBA", suffixes=(f"_{nam}", f"_{nam-1}"))
                
                col_dien_ton_that_nam = f"Điện tổn thất_{nam}"
                col_dien_ton_that_nam_truoc = f"Điện tổn thất_{nam-1}"
                
                if col_dien_ton_that_nam in df.columns and col_dien_ton_that_nam_truoc in df.columns:
                    df["Chênh lệch tổn thất"] = df[col_dien_ton_that_nam] - df[col_dien_ton_that_nam_truoc]
                else:
                    st.warning(f"Không tìm thấy cột '{col_dien_ton_that_nam}' hoặc '{col_dien_ton_that_nam_truoc}' để tính toán 'Chênh lệch tổn thất'.")
            else:
                st.warning("Cột 'Tên TBA' không tìm thấy trong một trong các DataFrame cho chế độ 'So sánh cùng kỳ'.")
        else:
            st.warning("Một trong các DataFrame (hiện tại hoặc năm trước) trống cho chế độ 'So sánh cùng kỳ'.")
            df = pd.DataFrame()

    elif mode == "Lũy kế cùng kỳ":
        files_now = generate_filenames(nam, thang_from, thang_to)
        files_last = generate_filenames(nam - 1, thang_from, thang_to)
        st.write(f"Các tệp hiện tại ({nam}) cho chế độ 'Lũy kế cùng kỳ': {files_now}")
        st.write(f"Các tệp năm trước ({nam-1}) cho chế độ 'Lũy kế cùng kỳ': {files_last}")
        df_now = load_data_from_drive(files_now, drive_files_map, drive_service)
        df_last = load_data_from_drive(files_last, drive_files_map, drive_service)
        if not df_now.empty and not df_last.empty:
            if "Tên TBA" in df_now.columns and "Tên TBA" in df_last.columns:
                st.write("Đang nhóm và hợp nhất dữ liệu cho chế độ 'Lũy kế cùng kỳ'.")
                df_now_group = df_now.groupby("Tên TBA", as_index=False).sum(numeric_only=True)
                df_last_group = df_last.groupby("Tên TBA", as_index=False).sum(numeric_only=True)
                
                df = df_now_group.merge(df_last_group, on="Tên TBA", suffixes=(f"_{nam}", f"_{nam-1}"))
                
                col_dien_ton_that_nam = f"Điện tổn thất_{nam}"
                col_dien_ton_that_nam_truoc = f"Điện tổn thất_{nam-1}"
                
                if col_dien_ton_that_nam in df.columns and col_dien_ton_that_nam_truoc in df.columns:
                    df["Chênh lệch tổn thất"] = df[col_dien_ton_that_nam] - df[col_dien_ton_that_nam_truoc]
                else:
                    st.warning(f"Không tìm thấy cột '{col_dien_ton_that_nam}' hoặc '{col_dien_ton_that_nam_truoc}' để tính toán 'Chênh lệch tổn thất' trong chế độ 'Lũy kế cùng kỳ'.")
            else:
                st.warning("Cột 'Tên TBA' không tìm thấy trong một trong các DataFrame đã nhóm cho chế độ 'Lũy kế cùng kỳ'.")
        else:
            st.warning("Một trong các DataFrame (hiện tại hoặc năm trước) trống cho chế độ 'Lũy kế cùng kỳ'.")
            df = pd.DataFrame()

# ==== HIỂN THỊ ====
st.markdown("---")
if not df.empty:
    st.dataframe(df, use_container_width=True)
    if "Tỷ lệ tổn thất" in df.columns:
        st.write("Cột 'Tỷ lệ tổn thất' được tìm thấy. Đang tạo biểu đồ.")
        fig, ax = plt.subplots(figsize=(10, 6))
        df.plot(kind="bar", x="Tên TBA", y="Tỷ lệ tổn thất", ax=ax)
        ax.set_title("Biểu đồ tỷ lệ tổn thất các TBA", fontsize=14, fontweight='bold', color='black')
        ax.set_ylabel("Tỷ lệ tổn thất (%)", fontsize=12, fontweight='bold', color='black')
        ax.set_xlabel("Tên TBA", fontsize=12, fontweight='bold', color='black')
        ax.tick_params(axis='x', labelrotation=90, labelcolor='black', labelsize=10)
        ax.tick_params(axis='y', labelcolor='black', labelsize=10)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("Không tìm thấy cột 'Tỷ lệ tổn thất' trong DataFrame. Không thể tạo biểu đồ.")
else:
    st.warning("Không có dữ liệu phù hợp hoặc thiếu tệp Excel trong thư mục Google Drive.")
    st.write("DataFrame trống. Vui lòng kiểm tra các đường dẫn tệp, tên tệp và nội dung trong Google Drive.")