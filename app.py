import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from datetime import datetime
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

st.set_page_config(layout="wide", page_title="Phân tích tổn thất TBA công cộng")
st.title("📊 Phân tích tổn thất các TBA công cộng")

# ============ CẤU HÌNH ============
col1, col2, col3 = st.columns(3)
with col1:
    mode = st.radio("Chế độ phân tích", ["Theo tháng", "Lũy kế", "So sánh cùng kỳ", "Lũy kế cùng kỳ"])
with col2:
    thang_from = st.selectbox("Từ tháng", list(range(1, 13)), index=0)
    thang_to = st.selectbox("Đến tháng", list(range(thang_from, 13)), index=4) if "Lũy kế" in mode else thang_from
with col3:
    nam = st.selectbox("Chọn năm", list(range(2020, datetime.now().year + 1))[::-1], index=0)
    nam_cungkỳ = nam - 1 if "cùng kỳ" in mode.lower() else None

nguong = st.selectbox("Ngưỡng tổn thất", ["(All)", "<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%", ">=5 và <7%", ">=7%"])

# ============ KẾT NỐI GOOGLE DRIVE ============
FOLDER_ID = '165Txi8IyqG50uFSFHzWidSZSG9qpsbaq'

@st.cache_data
def get_drive_service():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["google"],
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build('drive', 'v3', credentials=credentials)

@st.cache_data
def list_excel_files():
    service = get_drive_service()
    query = f"'{FOLDER_ID}' in parents and mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return {f['name']: f['id'] for f in results.get('files', [])}

def download_excel(file_id):
    service = get_drive_service()
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    fh.seek(0)
    try:
        return pd.read_excel(fh, sheet_name="dữ liệu")
    except:
        return pd.DataFrame()

def generate_filenames(year, start_month, end_month):
    return [f"TBA_{year}_{str(m).zfill(2)}.xlsx" for m in range(start_month, end_month + 1)]

def load_data(file_list, all_files, nhan="Thực hiện"):
    dfs = []
    for fname in file_list:
        file_id = all_files.get(fname)
        if file_id:
            df = download_excel(file_id)
            if not df.empty:
                df["Kỳ"] = nhan
                dfs.append(df)
    return pd.concat(dfs) if dfs else pd.DataFrame()

# ============ PHÂN TÍCH ============
all_files = list_excel_files()

def apply_filters_and_metrics(df):
    if df.empty:
        return df
    df = df.copy()
    df["Tỷ lệ tổn thất"] = round((df["Tổn thất (KWh)"] / df["ĐN nhận đầu nguồn"]) * 100, 2)
    df["ĐN nhận đầu nguồn"] = df["ĐN nhận đầu nguồn"].apply(lambda x: f"{x:,.0f}".replace(",", "."))
    df["Điện thương phẩm"] = df["Điện thương phẩm"].apply(lambda x: f"{x:,.0f}".replace(",", "."))
    df["Tổn thất (KWh)"] = df["Tổn thất (KWh)"].apply(lambda x: f"{x:,.0f}".replace(",", "."))
    if nguong != "(All)":
        df = df[df["Ngưỡng tổn thất"] == nguong]
    return df

files = generate_filenames(nam, thang_from, thang_to if "Lũy kế" in mode else thang_from)
df = load_data(files, all_files, "Thực hiện")
if "cùng kỳ" in mode.lower() and nam_cungkỳ:
    files_ck = generate_filenames(nam_cungkỳ, thang_from, thang_to if "Lũy kế" in mode else thang_from)
    df_ck = load_data(files_ck, all_files, "Cùng kỳ")
    df = pd.concat([df, df_ck])

df = apply_filters_and_metrics(df)

# ============ HIỂN THỊ ============
st.markdown("---")
if not df.empty:
    st.dataframe(df, use_container_width=True)

    # Biểu đồ cột theo kỳ và ngưỡng tổn thất
    if "Ngưỡng tổn thất" in df.columns and "Kỳ" in df.columns:
        count_df = df.groupby(["Ngưỡng tổn thất", "Kỳ"]).size().unstack(fill_value=0).reset_index()
        fig, ax = plt.subplots()
        width = 0.35
        x = range(len(count_df))
        bar1 = ax.bar([i - width/2 for i in x], count_df["Thực hiện"], width, label="Thực hiện", color="teal")
        bar2 = ax.bar([i + width/2 for i in x], count_df["Cùng kỳ"], width, label="Cùng kỳ", color="lightgray")
        ax.set_xticks(x)
        ax.set_xticklabels(count_df["Ngưỡng tổn thất"])
        ax.set_title("Số lượng TBA theo ngưỡng tổn thất", fontsize=14, fontweight="bold")
        ax.set_ylabel("Số lượng")
        for bars in [bar1, bar2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height + 0.5, f'{int(height)}', ha='center', fontsize=9, fontweight='bold', color='black')
        ax.legend()
        st.pyplot(fig)

    # Biểu đồ tròn tỷ trọng
    if "Ngưỡng tổn thất" in df.columns:
        pie_df = df["Ngưỡng tổn thất"].value_counts().sort_index()
        labels = pie_df.index
        sizes = pie_df.values
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.2f%%', startangle=90)
        ax1.axis('equal')
        ax1.set_title("Tỷ trọng TBA theo ngưỡng tổn thất")
        st.pyplot(fig1)
else:
    st.warning("Không có dữ liệu phù hợp hoặc thiếu file Excel trong thư mục Drive.")
