# app_tba_congcong.py
import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
import os
import re

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

# ==== HÀM QUÉT DANH SÁCH FILE TRÊN GOOGLE DRIVE (FOLDER CÔNG KHAI) ====
FOLDER_URL = "https://drive.google.com/drive/folders/1o1O5jMhvJ6V2bqr6VdNoWTfXYiFYnl98"

def get_file_links_from_drive(folder_url):
    folder_id = folder_url.split("folders/")[-1].split("?")[0]
    st.write(f"Đang cố gắng truy cập thư mục Google Drive ID: {folder_id}")
    url = f"https://drive.google.com/drive/folders/{folder_id}"
    try:
        res = requests.get(url)
        res.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        st.write(f"Trạng thái phản hồi URL thư mục Google Drive: {res.status_code}")
        
        # Kiểm tra nội dung phản hồi
        # st.text(res.text) # Bỏ comment dòng này để xem toàn bộ phản hồi HTML để gỡ lỗi regex

        pattern = re.compile(r'"(https://drive.google.com/file/d/[^/]+)"')
        matches = pattern.findall(res.text)
        st.write(f"Tìm thấy {len(matches)} liên kết tệp tiềm năng trong HTML.")
        files = {}
        for match in matches:
            file_id = match.split("/d/")[-1]
            file_name = get_filename_from_id(file_id)
            if file_name:
                files[file_name] = file_id
                st.write(f"  - Tìm thấy tệp: {file_name} với ID: {file_id}")
        st.write(f"Tổng số tệp được xác định từ Drive: {len(files)}")
        return files
    except requests.exceptions.RequestException as e:
        st.error(f"Lỗi khi truy cập Google Drive folder URL: {e}. Vui lòng kiểm tra URL và quyền truy cập thư mục.")
        return {}
    except Exception as e:
        st.error(f"Đã xảy ra lỗi không mong muốn khi lấy liên kết tệp từ Drive: {e}")
        return {}

def get_filename_from_id(file_id):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    try:
        res = requests.get(url, stream=True)
        res.raise_for_status()
        if "Content-Disposition" in res.headers:
            cd = res.headers["Content-Disposition"]
            filename_match = re.findall('filename="?([^";]+)"?', cd)
            if filename_match:
                st.write(f"  - Tên tệp được trích xuất từ header: {filename_match[0]}")
                return filename_match[0]
        st.write(f"  - Không thể trích xuất tên tệp cho ID: {file_id}. Header Content-Disposition không tìm thấy hoặc không chứa tên tệp.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Lỗi khi tải xuống tên tệp từ ID {file_id}: {e}. Có thể tệp không tồn tại hoặc không có quyền truy cập.")
        return None
    except Exception as e:
        st.error(f"Đã xảy ra lỗi không mong muốn khi lấy tên tệp từ ID {file_id}: {e}")
        return None

def download_excel_from_drive(file_id):
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    try:
        response = requests.get(download_url)
        response.raise_for_status()
        st.write(f"  - Trạng thái phản hồi URL tải xuống cho tệp ID {file_id}: {response.status_code}")
        
        # Kiểm tra nếu nội dung tải về là HTML (lỗi) thay vì file excel
        if "text/html" in response.headers.get("Content-Type", ""):
            st.error(f"Nội dung tải về từ ID {file_id} là HTML, không phải file Excel. Có thể là lỗi quyền truy cập hoặc tệp không phải Excel.")
            return pd.DataFrame()

        df = pd.read_excel(BytesIO(response.content), sheet_name="dữ liệu")
        st.write(f"  - Đã tải dữ liệu thành công từ tệp ID {file_id}. Kích thước DataFrame: {df.shape}")
        return df
    except requests.exceptions.RequestException as e:
        st.error(f"Lỗi khi tải xuống tệp Excel từ ID {file_id}: {e}. Tệp có thể không tồn tại hoặc không thể tải xuống.")
        return pd.DataFrame()
    except ValueError as e:
        st.error(f"Lỗi khi đọc tệp Excel từ ID {file_id}: {e}. Có thể tên sheet 'dữ liệu' không tồn tại hoặc tệp bị hỏng.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Đã xảy ra lỗi không mong muốn khi tải hoặc đọc tệp Excel từ ID {file_id}: {e}")
        return pd.DataFrame()

# ==== HÀM PHÂN TÍCH ====
def generate_filenames(year, start_month, end_month):
    return [f"TBA_{year}_{str(m).zfill(2)}.xlsx" for m in range(start_month, end_month + 1)]

def load_data_from_drive(file_list, drive_files):
    dfs = []
    st.write(f"Đang tải dữ liệu cho các tệp: {file_list}")
    for file in file_list:
        file_id = drive_files.get(file)
        if file_id:
            st.write(f"Đang tải tệp: {file} (ID: {file_id})")
            df = download_excel_from_drive(file_id)
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

# ==== XỬ LÝ ====
st.markdown("---")
st.write("Bắt đầu quá trình xử lý dữ liệu...")
drive_files = get_file_links_from_drive(FOLDER_URL)
if not drive_files:
    st.error("Không thể lấy danh sách tệp từ Google Drive. Vui lòng kiểm tra FOLDER_URL và quyền truy cập.")
    df = pd.DataFrame() # Đảm bảo df trống nếu không lấy được file

st.write(f"Chế độ phân tích được chọn: {mode}")
st.write(f"Năm: {nam}, Từ tháng: {thang_from}, Đến tháng: {thang_to}")

df = pd.DataFrame() # Khởi tạo df rỗng để tránh lỗi nếu không vào được các điều kiện

if mode == "Theo tháng":
    files = generate_filenames(nam, thang_from, thang_from)
    st.write(f"Tệp cần tìm cho chế độ 'Theo tháng': {files}")
    df = load_data_from_drive(files, drive_files)

elif mode == "Lũy kế":
    files = generate_filenames(nam, thang_from, thang_to)
    st.write(f"Các tệp cần tìm cho chế độ 'Lũy kế': {files}")
    df = load_data_from_drive(files, drive_files)
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
    df_now = load_data_from_drive(files_now, drive_files)
    df_last = load_data_from_drive(files_last, drive_files)
    if not df_now.empty and not df_last.empty:
        if "Tên TBA" in df_now.columns and "Tên TBA" in df_last.columns:
            st.write("Đang hợp nhất dữ liệu cho chế độ 'So sánh cùng kỳ'.")
            # Chọn các cột số có thể tồn tại để tránh lỗi sum() nếu chúng không có
            cols_to_sum = [col for col in df_now.columns if pd.api.types.is_numeric_dtype(df_now[col]) or col == "Tên TBA"]
            df_now_filtered = df_now[cols_to_sum]
            df_last_filtered = df_last[cols_to_sum] # Áp dụng tương tự cho df_last
            
            df = df_now_filtered.merge(df_last_filtered, on="Tên TBA", suffixes=(f"_{nam}", f"_{nam-1}"))
            
            # Đảm bảo các cột cần tính toán tồn tại trước khi thực hiện phép tính
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
        df = pd.DataFrame() # Đảm bảo df trống nếu không có dữ liệu

elif mode == "Lũy kế cùng kỳ":
    files_now = generate_filenames(nam, thang_from, thang_to)
    files_last = generate_filenames(nam - 1, thang_from, thang_to)
    st.write(f"Các tệp hiện tại ({nam}) cho chế độ 'Lũy kế cùng kỳ': {files_now}")
    st.write(f"Các tệp năm trước ({nam-1}) cho chế độ 'Lũy kế cùng kỳ': {files_last}")
    df_now = load_data_from_drive(files_now, drive_files)
    df_last = load_data_from_drive(files_last, drive_files)
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
        df = pd.DataFrame() # Đảm bảo df trống nếu không có dữ liệu

# ==== HIỂN THỊ ====
st.markdown("---")
if not df.empty:
    st.write("DataFrame đã được xử lý và không trống. Đang hiển thị dữ liệu.")
    st.dataframe(df, use_container_width=True)
    if "Tỷ lệ tổn thất" in df.columns:
        st.write("Cột 'Tỷ lệ tổn thất' được tìm thấy. Đang tạo biểu đồ.")
        fig, ax = plt.subplots(figsize=(10, 6)) # Tăng kích thước biểu đồ cho dễ nhìn
        df.plot(kind="bar", x="Tên TBA", y="Tỷ lệ tổn thất", ax=ax)
        ax.set_title("Biểu đồ tỷ lệ tổn thất các TBA", fontsize=14, fontweight='bold', color='black')
        ax.set_ylabel("Tỷ lệ tổn thất (%)", fontsize=12, fontweight='bold', color='black')
        ax.set_xlabel("Tên TBA", fontsize=12, fontweight='bold', color='black')
        ax.tick_params(axis='x', labelrotation=90, labelcolor='black', labelsize=10)
        ax.tick_params(axis='y', labelcolor='black', labelsize=10)
        plt.tight_layout() # Điều chỉnh layout để tránh nhãn bị cắt
        st.pyplot(fig)
    else:
        st.warning("Không tìm thấy cột 'Tỷ lệ tổn thất' trong DataFrame. Không thể tạo biểu đồ.")
else:
    st.warning("Không có dữ liệu phù hợp hoặc thiếu tệp Excel trong thư mục Google Drive.")
    st.write("DataFrame trống. Vui lòng kiểm tra các đường dẫn tệp, tên tệp và nội dung trong Google Drive.")