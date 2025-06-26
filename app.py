# app_tba_congcong.py
import streamlit as st
import pandas as pd
import os
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

# ==== HÀM TẠO TÊN FILE ====
def generate_filenames(year, start_month, end_month):
    return [f"TBA_{year}_{str(m).zfill(2)}.xlsx" for m in range(start_month, end_month + 1)]

# ==== ĐỌC FILE GIẢ LẬP (TỪ LOCAL TRƯỚC) ====
def load_data(file_list):
    data_frames = []
    for file in file_list:
        file_path = f"/mnt/data/{file}"
        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
            data_frames.append(df)
    return pd.concat(data_frames) if data_frames else pd.DataFrame()

# ==== XỬ LÝ DỮ LIỆU ====
if mode == "Theo tháng":
    files = generate_filenames(nam, thang_from, thang_from)
    df = load_data(files)

elif mode == "Lũy kế":
    files = generate_filenames(nam, thang_from, thang_to)
    df = load_data(files)
    if not df.empty and "Tên TBA" in df.columns:
        df = df.groupby("Tên TBA", as_index=False).sum()

elif mode == "So sánh cùng kỳ":
    files_now = generate_filenames(nam, thang_from, thang_from)
    files_last = generate_filenames(nam - 1, thang_from, thang_from)
    df_now = load_data(files_now)
    df_last = load_data(files_last)
    if not df_now.empty and not df_last.empty:
        df = df_now.merge(df_last, on="Tên TBA", suffixes=(f"_{nam}", f"_{nam-1}"))
        df["Chênh lệch tổn thất"] = df[f"Điện tổn thất_{nam}"] - df[f"Điện tổn thất_{nam-1}"]
    else:
        df = pd.DataFrame()

elif mode == "Lũy kế cùng kỳ":
    files_now = generate_filenames(nam, thang_from, thang_to)
    files_last = generate_filenames(nam - 1, thang_from, thang_to)
    df_now = load_data(files_now)
    df_last = load_data(files_last)
    if not df_now.empty and not df_last.empty:
        df_now_group = df_now.groupby("Tên TBA", as_index=False).sum()
        df_last_group = df_last.groupby("Tên TBA", as_index=False).sum()
        df = df_now_group.merge(df_last_group, on="Tên TBA", suffixes=(f"_{nam}", f"_{nam-1}"))
        df["Chênh lệch tổn thất"] = df[f"Điện tổn thất_{nam}"] - df[f"Điện tổn thất_{nam-1}"]
    else:
        df = pd.DataFrame()

# ==== HIỂN THỊ DỮ LIỆU ====
st.markdown("---")
if not df.empty:
    st.dataframe(df, use_container_width=True)

    # Vẽ biểu đồ mẫu nếu có cột "Tỷ lệ tổn thất"
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
    st.warning("Không có dữ liệu phù hợp hoặc thiếu file Excel trong thư mục test.")
