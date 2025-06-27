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

files = generate_filenames(nam, thang_from, thang_to if "Lũy kế" in mode else thang_from)
df = load_data(files, all_files, "Thực hiện")
if "cùng kỳ" in mode.lower() and nam_cungkỳ:
    files_ck = generate_filenames(nam_cungkỳ, thang_from, thang_to if "Lũy kế" in mode else thang_from)
    df_ck = load_data(files_ck, all_files, "Cùng kỳ")
    df = pd.concat([df, df_ck])

# ============ TIỀN XỬ LÝ ==========
if not df.empty and all(col in df.columns for col in ["Tổn thất (KWh)", "ĐN nhận đầu nguồn"]):
    df = df.copy()
    # Tỷ lệ tổn thất lấy trực tiếp từ file Excel, không tính lại
    # Định dạng số liệu cột điện nhận, điện thương phẩm, tổn thất
    for col in ["ĐN nhận đầu nguồn", "Điện thương phẩm", "Tổn thất (KWh)"]:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"{x:,.0f}".replace(",", "."))

    for col in ["Tỷ lệ tổn thất", "So sánh"]:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: round(x, 2))

    if "Ngưỡng tổn thất" in df.columns and nguong != "(All)":
        df = df[df["Ngưỡng tổn thất"] == nguong]

    for col in ["ĐN nhận đầu nguồn", "Điện thương phẩm", "Tổn thất (KWh)"]:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"{x:,.0f}".replace(",", "."))

# ============ HIỂN THỊ ==========
st.markdown("---")
if not df.empty:
    st.dataframe(df, use_container_width=True)

    # Phân loại ngưỡng tổn thất
    def classify_nguong(x):
        if x < 2: return "<2%"
        elif 2 <= x < 3: return ">=2 và <3%"
        elif 3 <= x < 4: return ">=3 và <4%"
        elif 4 <= x < 5: return ">=4 và <5%"
        elif 5 <= x < 7: return ">=5 và <7%"
        else: return ">=7%"

    if "Tỷ lệ tổn thất" in df.columns:
        df["Ngưỡng tổn thất"] = df["Tỷ lệ tổn thất"].apply(classify_nguong)

    import matplotlib.pyplot as plt
    import numpy as np

    labels = ["<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%", ">=5 và <7%", ">=7%"]
    colors_bar = ["#2f69bf", "#f28e2b", "#bab0ac", "#59a14f", "#e6b000", "#d62728"]

    if "Kỳ" in df.columns:
        group_df = df.groupby(["Ngưỡng tổn thất", "Kỳ"]).size().unstack(fill_value=0).reindex(labels, fill_value=0)
        counts_thuchien = group_df.get("Thực hiện", pd.Series([0]*6, index=labels))
        counts_cungkỳ = group_df.get("Cùng kỳ", pd.Series([0]*6, index=labels))
    else:
        counts_thuchien = df["Ngưỡng tổn thất"].value_counts().reindex(labels, fill_value=0)
        counts_cungkỳ = pd.Series([0]*6, index=labels)

    fig, (ax_bar, ax_pie) = plt.subplots(1, 2, figsize=(12, 5), width_ratios=[2, 1])

    x = np.arange(len(labels))
    width = 0.35
    bars1 = ax_bar.bar(x - width/2, counts_thuchien, width=width, color=colors_bar, label="Thực hiện")
    bars2 = ax_bar.bar(x + width/2, counts_cungkỳ, width=width, color="#d3d3d3", label="Cùng kỳ")

    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax_bar.text(bar.get_x() + bar.get_width()/2, height + 1, str(int(height)),
                        ha='center', va='bottom', fontsize=9, fontweight='bold', color='black')

    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(labels, fontsize=10, fontweight='bold')
    ax_bar.set_ylabel("Số lượng", fontsize=11)
    ax_bar.set_title("Số lượng TBA theo ngưỡng tổn thất", fontsize=12, fontweight='bold')
    ax_bar.legend(fontsize=9)

    # Donut chart
    total = sum(counts_thuchien)
    wedges, texts, autotexts = ax_pie.pie(
        counts_thuchien,
        labels=None,
        autopct=lambda p: f'{p:.2f}%' if p > 0 else '',
        startangle=90,
        colors=colors_bar,
        wedgeprops={'width': 0.3}
    )
    for autotext in autotexts:
        autotext.set_fontweight('bold')
        autotext.set_color('black')
        autotext.set_fontsize(9)
    ax_pie.text(0, 0, f"Tổng số TBA\n{total}", ha='center', va='center', fontsize=11, fontweight='bold')
    ax_pie.set_title("Tỷ trọng TBA theo ngưỡng tổn thất", fontsize=11, fontweight='bold')

    plt.tight_layout()
    st.pyplot(fig)


    # Biểu đồ cột theo kỳ và ngưỡng tổn thất
    if "Ngưỡng tổn thất" in df.columns and "Kỳ" in df.columns:
        count_df = df.groupby(["Ngưỡng tổn thất", "Kỳ"]).size().unstack(fill_value=0).reset_index()
        fig, ax = plt.subplots(figsize=(10, 5))
        width = 0.35
        x = range(len(count_df))
        cols = list(count_df.columns)
        cols.remove("Ngưỡng tổn thất")
        for i, col in enumerate(cols):
            offset = (i - (len(cols) - 1)/2) * width
            bars = ax.bar([xi + offset for xi in x], count_df[col], width, label=col, color=("teal" if "Thực" in col else "lightgray"))
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height + 0.5, f'{int(height)}', ha='center', fontsize=9, fontweight='bold', color='black')
        ax.set_xticks(x)
        ax.set_xticklabels(count_df["Ngưỡng tổn thất"], fontsize=10, fontweight='bold')
        ax.set_title("Số lượng TBA theo ngưỡng tổn thất", fontsize=14, fontweight="bold")
        ax.set_ylabel("Số lượng")
        ax.legend()
        st.pyplot(fig)

        # Biểu đồ donut tỷ trọng TBA theo ngưỡng
        count_pie = df["Ngưỡng tổn thất"].value_counts().reindex([
            "<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%", ">=5 và <7%", ">=7%"
        ], fill_value=0)
        fig2, ax2 = plt.subplots(figsize=(5, 5))
        colors_pie = ["#2f69bf", "#f28e2b", "#bab0ac", "#59a14f", "#e6b000", "#d62728"]
        wedges, texts, autotexts = ax2.pie(
            count_pie,
            labels=None,
            autopct=lambda p: f'{p:.2f}%' if p > 0 else '',
            startangle=90,
            colors=colors_pie,
            wedgeprops={'width': 0.3}
        )
        for autotext in autotexts:
            autotext.set_fontweight('bold')
            autotext.set_color('black')
            autotext.set_fontsize(10)
        ax2.text(0, 0, f"Tổng số TBA\n{count_pie.sum()}", ha='center', va='center', fontsize=12, fontweight='bold')
        st.pyplot(fig2)


else:
    st.warning("Không có dữ liệu phù hợp hoặc thiếu file Excel trong thư mục Drive.")
