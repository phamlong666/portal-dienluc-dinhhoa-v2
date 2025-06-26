# Tập trung sửa lỗi không đọc được dữ liệu từ Google Drive

import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
import re

st.set_page_config(layout="wide", page_title="Phân tích tổn thất TBA công cộng")
st.title("📊 Phân tích tổn thất các TBA công cộng")

# ==== CẤU HÌNH ====
col1, col2, col3 = st.columns(3)
with col1:
    mode = st.radio("Chế độ phân tích", ["Theo tháng", "Lũy kế", "So sánh cùng kỳ", "Lũy kế cùng kỳ"])
with col2:
    thang_from = st.selectbox("Từ tháng", list(range(1, 13)), index=0)
    thang_to = st.selectbox("Đến tháng", list(range(thang_from, 13)), index=4) if "Lũy kế" in mode else thang_from
with col3:
    nam = st.selectbox("Chọn năm", list(range(2020, datetime.now().year + 1))[::-1], index=0)

# ==== URL Google Drive thư mục chứa dữ liệu ====
FOLDER_URL = "https://drive.google.com/drive/folders/1o1O5jMhvJ6V2bqr6VdNoWTfXYiFYnl98"

# ==== Sửa hàm lấy danh sách file sử dụng BeautifulSoup để tránh lỗi khi Google đổi cấu trúc ====
def get_file_links_from_drive(folder_url):
    from bs4 import BeautifulSoup
    folder_id = folder_url.split("folders/")[-1].split("?")[0]
    url = f"https://drive.google.com/drive/folders/{folder_id}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    scripts = soup.find_all("script")
    files = {}
    for script in scripts:
        if "drive.view" in script.text:
            matches = re.findall(r'\\x22(.*?)\\x22', script.text)
            for i in range(len(matches)):
                if matches[i].endswith(".xlsx"):
                    name = matches[i]
                    try:
                        file_id = matches[i + 2]
                        if len(file_id) > 20:
                            files[name] = file_id
                    except:
                        continue
    return files

def download_excel_from_drive(file_id):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    res = requests.get(url)
    if res.status_code == 200:
        return pd.read_excel(BytesIO(res.content), sheet_name="dữ liệu")
    return pd.DataFrame()

def generate_filenames(year, start_month, end_month):
    return [f"TBA_{year}_{str(m).zfill(2)}.xlsx" for m in range(start_month, end_month + 1)]

def load_data_from_drive(file_list, drive_files):
    dfs = []
    for file in file_list:
        file_id = drive_files.get(file)
        if file_id:
            df = download_excel_from_drive(file_id)
            if not df.empty:
                dfs.append(df)
    return pd.concat(dfs) if dfs else pd.DataFrame()

# ==== TẢI DANH SÁCH FILE ====
drive_files = get_file_links_from_drive(FOLDER_URL)

if mode == "Theo tháng":
    files = generate_filenames(nam, thang_from, thang_from)
    df = load_data_from_drive(files, drive_files)
elif mode == "Lũy kế":
    files = generate_filenames(nam, thang_from, thang_to)
    df = load_data_from_drive(files, drive_files)
    if not df.empty and "Tên TBA" in df.columns:
        df = df.groupby("Tên TBA", as_index=False).sum()
elif mode == "So sánh cùng kỳ":
    files_now = generate_filenames(nam, thang_from, thang_from)
    files_last = generate_filenames(nam - 1, thang_from, thang_from)
    df_now = load_data_from_drive(files_now, drive_files)
    df_last = load_data_from_drive(files_last, drive_files)
    if not df_now.empty and not df_last.empty:
        df = df_now.merge(df_last, on="Tên TBA", suffixes=(f"_{nam}", f"_{nam-1}"))
        df["Chênh lệch tổn thất"] = df[f"Điện tổn thất_{nam}"] - df[f"Điện tổn thất_{nam-1}"]
    else:
        df = pd.DataFrame()
elif mode == "Lũy kế cùng kỳ":
    files_now = generate_filenames(nam, thang_from, thang_to)
    files_last = generate_filenames(nam - 1, thang_from, thang_to)
    df_now = load_data_from_drive(files_now, drive_files)
    df_last = load_data_from_drive(files_last, drive_files)
    if not df_now.empty and not df_last.empty:
        df_now_group = df_now.groupby("Tên TBA", as_index=False).sum()
        df_last_group = df_last.groupby("Tên TBA", as_index=False).sum()
        df = df_now_group.merge(df_last_group, on="Tên TBA", suffixes=(f"_{nam}", f"_{nam-1}"))
        df["Chênh lệch tổn thất"] = df[f"Điện tổn thất_{nam}"] - df[f"Điện tổn thất_{nam-1}"]
    else:
        df = pd.DataFrame()

# ==== HIỂN THỊ ==== 
st.markdown("---")
if not df.empty:
    st.dataframe(df, use_container_width=True)
    if "Tỷ lệ tổn thất" in df.columns:
        fig, ax = plt.subplots()
        df.plot(kind="bar", x="Tên TBA", y="Tỷ lệ tổn thất", ax=ax)
        ax.set_title("Biểu đồ tỷ lệ tổn thất các TBA", fontsize=14, fontweight='bold', color='black')
        ax.set_ylabel("Tỷ lệ tổn thất (%)", fontsize=12, fontweight='bold', color='black')
        ax.set_xlabel("Tên TBA", fontsize=12, fontweight='bold', color='black')
        ax.tick_params(axis='x', labelrotation=90, labelcolor='black', labelsize=10)
        ax.tick_params(axis='y', labelcolor='black', labelsize=10)
        st.pyplot(fig)
else:
    st.warning("Không có dữ liệu phù hợp hoặc thiếu tệp Excel trong thư mục Google Drive.")
