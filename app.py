# app.py - Cập nhật lấy dữ liệu từ Google Sheets
import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt

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

# ==== ĐỌC DANH SÁCH FILE TỪ GOOGLE SHEET ====
SHEET_ID = "1Dawt9EdBWkToRZoUJKuD2AENOOk1weEXqdOwtZPZdJ0"
SHEET_NAME = "Danh_sach_file"
URL_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

@st.cache_data

def load_file_list():
    try:
        df_file = pd.read_csv(URL_CSV)
        df_file = df_file[df_file["Tên file"].str.endswith(".xlsx")]
        return df_file.set_index("Tên file")["Link tải"].to_dict()
    except:
        return {}

# ==== TẢI FILE EXCEL ====
def download_excel_from_url(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return pd.read_excel(BytesIO(r.content), sheet_name="dữ liệu")
    except:
        pass
    return pd.DataFrame()

@st.cache_data

def generate_filenames(year, start_month, end_month):
    return [f"TBA_{year}_{str(m).zfill(2)}.xlsx" for m in range(start_month, end_month + 1)]

@st.cache_data

def load_data(file_list, file_links):
    dfs = []
    for fname in file_list:
        if fname in file_links:
            df = download_excel_from_url(file_links[fname])
            if not df.empty:
                dfs.append(df)
    return pd.concat(dfs) if dfs else pd.DataFrame()

# ==== XỬ LÝ ====
df_file_links = load_file_list()

if mode == "Theo tháng":
    files = generate_filenames(nam, thang_from, thang_from)
    df = load_data(files, df_file_links)

elif mode == "Lũy kế":
    files = generate_filenames(nam, thang_from, thang_to)
    df = load_data(files, df_file_links)
    if not df.empty and "Tên TBA" in df.columns:
        df = df.groupby("Tên TBA", as_index=False).sum()

elif mode == "So sánh cùng kỳ":
    files_now = generate_filenames(nam, thang_from, thang_from)
    files_last = generate_filenames(nam - 1, thang_from, thang_from)
    df_now = load_data(files_now, df_file_links)
    df_last = load_data(files_last, df_file_links)
    if not df_now.empty and not df_last.empty:
        df = df_now.merge(df_last, on="Tên TBA", suffixes=(f"_{nam}", f"_{nam-1}"))
        df["Chênh lệch tổn thất"] = df[f"Điện tổn thất_{nam}"] - df[f"Điện tổn thất_{nam-1}"]
    else:
        df = pd.DataFrame()

elif mode == "Lũy kế cùng kỳ":
    files_now = generate_filenames(nam, thang_from, thang_to)
    files_last = generate_filenames(nam - 1, thang_from, thang_to)
    df_now = load_data(files_now, df_file_links)
    df_last = load_data(files_last, df_file_links)
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
    st.warning("Không có dữ liệu phù hợp hoặc thiếu tệp Excel theo định dạng yêu cầu.")