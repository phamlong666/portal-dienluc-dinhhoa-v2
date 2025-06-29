import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

st.set_page_config(layout="wide", page_title="Báo cáo tổn thất TBA")
st.title("📥 AI_Trợ lý tổn thất")

# --- Khởi tạo Session State cho dữ liệu (Giữ nguyên cho các phần khác) ---
if 'df_tba_thang' not in st.session_state:
    st.session_state.df_tba_thang = None
if 'df_tba_luyke' not in st.session_state:
    st.session_state.df_tba_luyke = None # Corrected: Changed session_session to session_state
if 'df_tba_ck' not in st.session_state:
    st.session_state.df_tba_ck = None
if 'df_ha_thang' not in st.session_state:
    st.session_state.df_ha_thang = None
if 'df_ha_luyke' not in st.session_state:
    st.session_state.df_ha_luyke = None
if 'df_ha_ck' not in st.session_state:
    st.session_state.df_ha_ck = None
if 'df_trung_thang_tt' not in st.session_state:
    st.session_state.df_trung_thang_tt = None
if 'df_trung_luyke_tt' not in st.session_state:
    st.session_state.df_trung_ck_tt = None
if 'df_trung_thang_dy' not in st.session_state:
    st.session_state.df_trung_thang_dy = None
if 'df_trung_luyke_dy' not in st.session_state:
    st.session_state.df_trung_luyke_dy = None
if 'df_trung_ck_dy' not in st.session_state:
    st.session_state.df_trung_ck_dy = None
if 'df_dv_thang' not in st.session_state:
    st.session_state.df_dv_thang = None
if 'df_dv_luyke' not in st.session_state:
    st.session_state.df_dv_luyke = None
if 'df_dv_ck' not in st.session_state:
    st.session_state.df_dv_ck = None


# --- Biến và Hàm hỗ trợ tải dữ liệu từ Google Drive (từ app moi.py) ---
FOLDER_ID = '165Txi8IyqG50uFSFHzWidSZSG9qpsbaq' # ID thư mục Google Drive chứa file Excel

@st.cache_data
def get_drive_service():
    """Khởi tạo và trả về đối tượng dịch vụ Google Drive."""
    try:
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["google"],
            scopes=["https://www.googleapis.com/auth/drive.readonly"] # Chỉ cần quyền đọc
        )
        return build('drive', 'v3', credentials=credentials)
    except Exception as e:
        st.error(f"Lỗi khi xác thực Google Drive: {e}. Vui lòng kiểm tra cấu hình `secrets.toml`.")
        return None

@st.cache_data
def list_excel_files():
    """Liệt kê các file Excel trong thư mục Google Drive đã cho."""
    service = get_drive_service()
    if not service:
        return {}
    query = f"'{FOLDER_ID}' in parents and mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'"
    try:
        results = service.files().list(q=query, fields="files(id, name)").execute()
        return {f['name']: f['id'] for f in results.get('files', [])}
    except Exception as e:
        st.error(f"Lỗi khi liệt kê file từ Google Drive: {e}. Vui lòng kiểm tra ID thư mục và quyền truy cập.")
        return {}

@st.cache_data
def download_excel(file_id):
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
            # st.progress(status.progress()) # Có thể thêm thanh tiến trình
        fh.seek(0)
        return pd.read_excel(fh, sheet_name=0)
    except Exception as e:
        st.warning(f"Không thể tải xuống hoặc đọc file với ID {file_id}. Lỗi: {e}. Có thể file không tồn tại hoặc không đúng định dạng sheet 'dữ liệu'.")
        return pd.DataFrame()

def generate_filenames(year, start_month, end_month):
    """Tạo danh sách tên file dự kiến dựa trên năm và tháng."""
    return [f"TBA_{year}_{str(m).zfill(2)}.xlsx" for m in range(start_month, end_month + 1)]

def load_data(file_list, all_files, nhan="Thực hiện"):
    """Tải và nối các DataFrame từ danh sách file."""
    dfs = []
    for fname in file_list:
        file_id = all_files.get(fname)
        if file_id:
            df = download_excel(file_id)
            if not df.empty:
                df["Kỳ"] = nhan
                dfs.append(df)
        else:
            st.info(f"Không tìm thấy file: {fname}")
    return pd.concat(dfs) if dfs else pd.DataFrame()

def classify_nguong(x):
    """Phân loại tỷ lệ tổn thất vào các ngưỡng."""
    try:
        # Chuyển đổi sang số nếu cần, xử lý dấu phẩy thành dấu chấm
        x = float(str(x).replace(",", "."))
    except (ValueError, TypeError):
        return "Không rõ" # Xử lý các giá trị không phải số

    if x < 2: return "<2%"
    elif 2 <= x < 3: return ">=2 và <3%"
    elif 3 <= x < 4: return ">=3 và <4%"
    elif 4 <= x < 5: return ">=4 và <5%"
    elif 5 <= x < 7: return ">=5 và <7%"
    else: return ">=7%"


# --- Các nút điều hướng chính (Expander) ---

with st.expander("🔌 Tổn thất các TBA công cộng"):
    st.header("Phân tích dữ liệu TBA công cộng")

    # Toàn bộ nội dung từ app moi.py được chèn vào đây
    col1, col2, col3 = st.columns(3)
    with col1:
        mode = st.radio("Chế độ phân tích", ["Theo tháng", "Lũy kế", "So sánh cùng kỳ", "Lũy kế cùng kỳ"], key="tba_mode")
    with col2:
        thang_from = st.selectbox("Từ tháng", list(range(1, 13)), index=0, key="tba_thang_from")
        # Đảm bảo thang_to không nhỏ hơn thang_from
        thang_to_options = list(range(thang_from, 13))
        # Đặt index mặc định để tránh lỗi khi thang_to_options rỗng
        default_index_thang_to = 0 if thang_to_options else None
        if "Lũy kế" in mode:
            # Chọn index sao cho nó không vượt quá kích thước của list options
            # Nếu tháng 5 là index 4 trong list 1-12, khi range bắt đầu từ 5, index 4 có thể là tháng 9
            # Cố gắng giữ tháng 5 làm tháng cuối mặc định nếu có thể
            if 5 in thang_to_options:
                default_index_thang_to = thang_to_options.index(5)
            elif len(thang_to_options) > 4: # Fallback nếu 5 không có, chọn tháng thứ 5 trong list mới
                 default_index_thang_to = 4
            else: # Nếu ít hơn 5 tháng, chọn tháng cuối cùng
                 default_index_thang_to = len(thang_to_options) - 1 if thang_to_options else None

            thang_to = st.selectbox("Đến tháng", thang_to_options, index=default_index_thang_to, key="tba_thang_to")
        else:
            thang_to = thang_from # Nếu không phải lũy kế, tháng đến bằng tháng từ

    with col3:
        nam = st.selectbox("Chọn năm", list(range(2020, datetime.now().year + 1))[::-1], index=0, key="tba_nam")
        nam_cungkỳ = nam - 1 if "cùng kỳ" in mode.lower() else None

    nguong_display = st.selectbox("Ngưỡng tổn thất", ["(All)", "<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%", ">=5 và <7%", ">=7%"], key="tba_nguong_display")

    # Tải dữ liệu từ Google Drive
    all_files = list_excel_files()

    files = generate_filenames(nam, thang_from, thang_to if "Lũy kế" in mode or "cùng kỳ" in mode.lower() else thang_from)
    df = load_data(files, all_files, "Thực hiện")

    if "cùng kỳ" in mode.lower() and nam_cungkỳ:
        files_ck = generate_filenames(nam_cungkỳ, thang_from, thang_to if "Lũy kế" in mode or "cùng kỳ" in mode.lower() else thang_from)
        df_ck = load_data(files_ck, all_files, "Cùng kỳ")
        if not df_ck.empty:
            # Đảm bảo cột "Kỳ" là string để có thể concat
            df_ck["Kỳ"] = "Cùng kỳ"
            df = pd.concat([df, df_ck])

    if not df.empty and "Tỷ lệ tổn thất" in df.columns:
        # Đảm bảo cột Tỷ lệ tổn thất là số để apply classify_nguong
        df["Tỷ lệ tổn thất"] = pd.to_numeric(df["Tỷ lệ tổn thất"].astype(str).str.replace(',', '.'), errors='coerce')
        df["Ngưỡng tổn thất"] = df["Tỷ lệ tổn thất"].apply(classify_nguong)

        # Drop duplicates based on 'Tên TBA' and 'Kỳ' to count unique TBAs per period
        df_unique = df.drop_duplicates(subset=["Tên TBA", "Kỳ"])

        # Create count_df and pivot_df for plotting
        count_df = df_unique.groupby(["Ngưỡng tổn thất", "Kỳ"]).size().reset_index(name="Số lượng")
        pivot_df = count_df.pivot(index="Ngưỡng tổn thất", columns="Kỳ", values="Số lượng").fillna(0).astype(int)
        # Sắp xếp lại thứ tự các ngưỡng
        pivot_df = pivot_df.reindex(["<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%", ">=5 và <7%", ">=7%"])

        # --- Vẽ biểu đồ ---
        # Increased DPI to 600 for sharpness, adjusted figsize for better presentation
        fig, (ax_bar, ax_pie) = plt.subplots(1, 2, figsize=(10, 4), dpi=600)

        # Biểu đồ cột
        x = range(len(pivot_df))
        width = 0.35
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'] # Màu sắc cho các cột
        for i, col in enumerate(pivot_df.columns):
            offset = (i - (len(pivot_df.columns)-1)/2) * width
            bars = ax_bar.bar([xi + offset for xi in x], pivot_df[col], width, label=col, color=colors[i % len(colors)])
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    # Adjusted fontsize for bar value labels
                    ax_bar.text(bar.get_x() + bar.get_width()/2, height + 0.5, f'{int(height)}', ha='center', va='bottom', fontsize=7, fontweight='bold', color='black')

        # Adjusted fontsize for y-axis label
        ax_bar.set_ylabel("Số lượng", fontsize=8)
        # Adjusted fontsize and weight for title
        ax_bar.set_title("Số lượng TBA theo ngưỡng tổn thất", fontsize=10, weight='bold')
        ax_bar.set_xticks(list(x))
        # Adjusted fontsize for x-axis tick labels
        ax_bar.set_xticklabels(pivot_df.index, fontsize=7)
        # Adjusted fontsize for y-axis tick labels
        ax_bar.tick_params(axis='y', labelsize=7)
        # Adjusted fontsize for legend
        ax_bar.legend(title="Kỳ", fontsize=7)
        # Adjusted gridline properties
        ax_bar.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.6)

        # Biểu đồ tròn (Tỷ trọng) - Ưu tiên dữ liệu 'Thực hiện' hoặc kỳ đầu tiên nếu không có
        pie_data = pd.Series(0, index=pivot_df.index) # Default empty
        if 'Thực hiện' in df_unique['Kỳ'].unique():
            df_latest = df_unique[df_unique['Kỳ'] == 'Thực hiện']
            pie_data = df_latest["Ngưỡng tổn thất"].value_counts().reindex(pivot_df.index, fill_value=0)
        elif not df_unique.empty and not pivot_df.empty:
            # Fallback to the first available period if 'Thực hiện' is not present
            first_col_data = pivot_df.iloc[:, 0]
            if first_col_data.sum() > 0:
                pie_data = first_col_data

        if pie_data.sum() > 0:
            wedges, texts, autotexts = ax_pie.pie(
                pie_data,
                labels=pivot_df.index,
                autopct='%1.1f%%',
                startangle=90,
                colors=colors,
                pctdistance=0.75,
                wedgeprops={'width': 0.3, 'edgecolor': 'w'}
            )

            for text in texts:
                # Adjusted fontsize for pie chart labels
                text.set_fontsize(6)
                text.set_fontweight('bold')
            for autotext in autotexts:
                autotext.set_color('black')
                # Adjusted fontsize for autopct values
                autotext.set_fontsize(6)
                autotext.set_fontweight('bold')

            # Adjusted fontsize for total TBA text
            ax_pie.text(0, 0, f"Tổng số TBA\\n{pie_data.sum()}", ha='center', va='center', fontsize=7, fontweight='bold', color='black')
            # Adjusted fontsize and weight for pie chart title
            ax_pie.set_title("Tỷ trọng TBA theo ngưỡng tổn thất", fontsize=10, weight='bold')
        else:
            # Adjusted fontsize for no data text
            ax_pie.text(0.5, 0.5, "Không có dữ liệu tỷ trọng phù hợp", horizontalalignment='center', verticalalignment='center', transform=ax_pie.transAxes, fontsize=8)
            # Adjusted fontsize and weight for pie chart title
            ax_pie.set_title("Tỷ trọng TBA theo ngưỡng tổn thất", fontsize=10, weight='bold')


        st.pyplot(fig)

        # --- Danh sách chi tiết TBA ---
        nguong_filter = st.selectbox("Chọn ngưỡng để lọc danh sách TBA", ["(All)", "<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%", ">=5 và <7%", ">=7%"], key="tba_detail_filter")
        if nguong_filter != "(All)":
            df_filtered = df[df["Ngưỡng tổn thất"] == nguong_filter]
        else:
            df_filtered = df

        st.markdown("### 📋 Danh sách chi tiết TBA")
        st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True)

    else:
        st.warning("Không có dữ liệu phù hợp để hiển thị biểu đồ. Vui lòng kiểm tra các file Excel trên Google Drive và định dạng của chúng (cần cột 'Tỷ lệ tổn thất').")




with st.expander("⚡ Tổn thất hạ thế"):
    st.header("Phân tích dữ liệu tổn thất hạ thế")

    FOLDER_ID_HA = '1_rAY5T-unRyw20YwMgKuG1C0y7oq6GkK'

    @st.cache_data
    def list_excel_files_ha():
        service = get_drive_service()
        if not service:
            return {}
        query = f"'{FOLDER_ID_HA}' in parents and mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'"
        try:
            results = service.files().list(q=query, fields="files(id, name)").execute()
            return {f['name']: f['id'] for f in results.get('files', [])}
        except Exception as e:
            st.error(f"Lỗi liệt kê file hạ thế: {e}")
            return {}

    all_files_ha = list_excel_files_ha()
    nam = st.selectbox("Chọn năm", list(range(2020, datetime.now().year + 1))[::-1], index=0, key="ha_nam")
    loai_bc = st.radio("Loại báo cáo", ["Tháng", "Lũy kế"], horizontal=True, key="ha_loai_bc")
    thang = st.selectbox("Chọn tháng", list(range(1, 13)), index=0, key="ha_thang")

    months = list(range(1, 13))
    df_th = pd.DataFrame({"Tháng": months, "Tỷ lệ": [None]*12})
    df_ck = pd.DataFrame({"Tháng": months, "Tỷ lệ": [None]*12})

    tong_ton_that = 0
    tong_thuong_pham = 0

    for i in range(1, 13):
        fname = f"HA_{nam}_{i:02}.xlsx"
        file_id = all_files_ha.get(fname)

        if file_id and i <= thang:
            df = download_excel(file_id)
            if not df.empty and df.shape[0] >= 1:
                try:
                    ty_le_th = float(str(df.iloc[0, 4]).replace(",", "."))
                    ton_that = float(str(df.iloc[0, 3]).replace(",", "."))
                    thuong_pham = float(str(df.iloc[0, 1]).replace(",", "."))

                    if loai_bc == "Lũy kế":
                        tong_ton_that += ton_that
                        tong_thuong_pham += thuong_pham
                        ty_le_lk = (tong_ton_that / tong_thuong_pham) * 100 if tong_thuong_pham > 0 else 0
                        df_th.loc[df_th["Tháng"] == i, "Tỷ lệ"] = ty_le_lk
                    else:
                        df_th.loc[df_th["Tháng"] == i, "Tỷ lệ"] = ty_le_th
                except:
                    st.warning(f"Lỗi đọc file: {fname}")

        # Cùng kỳ luôn lấy đủ 12 tháng
        fname_ck = f"HA_{nam - 1}_{i:02}.xlsx"
        file_id_ck = all_files_ha.get(fname_ck)
        if file_id_ck:
            df_ck_file = download_excel(file_id_ck)
            if not df_ck_file.empty and df_ck_file.shape[0] >= 1:
                try:
                    ty_le_ck = float(str(df_ck_file.iloc[0, 4]).replace(",", "."))
                    df_ck.loc[df_ck["Tháng"] == i, "Tỷ lệ"] = ty_le_ck
                except:
                    pass

    if df_th["Tỷ lệ"].notna().any():
        # Changed figsize for a slightly smaller plot, and DPI for sharpness
        fig, ax = plt.subplots(figsize=(6, 3), dpi=600) # Increased DPI to 600 for sharpness, adjusted figsize

        ax.plot(df_th["Tháng"], df_th["Tỷ lệ"], color='#1f77b4', label='Thực hiện', linewidth=1, markersize=3, marker='o') # Adjusted linewidth and markersize
        if df_ck["Tỷ lệ"].notna().any():
            ax.plot(df_ck["Tháng"], df_ck["Tỷ lệ"], color='#ff7f0e', label='Cùng kỳ', linewidth=1, markersize=3, marker='o') # Adjusted linewidth and markersize

        for i, v in df_th.dropna(subset=["Tỷ lệ"]).iterrows():
            ax.text(v["Tháng"], v["Tỷ lệ"] + 0.05, f"{v['Tỷ lệ']:.2f}", ha='center', fontsize=6, color='black') # Adjusted fontsize to 6

        if df_ck["Tỷ lệ"].notna().any():
            for i, v in df_ck.dropna(subset=["Tỷ lệ"]).iterrows():
                ax.text(v["Tháng"], v["Tỷ lệ"] + 0.05, f"{v['Tỷ lệ']:.2f}", ha='center', fontsize=6, color='black') # Adjusted fontsize to 6

        ax.set_ylabel("Tỷ lệ (%)", fontsize=7, color='black') # Adjusted fontsize to 7
        ax.set_xlabel("Tháng", fontsize=7, color='black') # Adjusted fontsize to 7
        ax.set_xticks(months)
        ax.tick_params(axis='both', colors='black', labelsize=6) # Adjusted labelsize to 6
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7) # Adjusted linewidth and alpha for grid
        ax.set_title("Biểu đồ tỷ lệ tổn thất hạ thế", fontsize=9, color='black') # Adjusted fontsize to 9
        ax.legend(fontsize=7, frameon=False) # Adjusted fontsize to 7

        st.pyplot(fig)
        st.dataframe(df_th)

    else:
        st.warning("Không có dữ liệu phù hợp để hiển thị.")

with st.expander("⚡ Tổn thất trung thế"):
    st.header("Phân tích dữ liệu TBA Trung thế")

    FOLDER_ID_TRUNG = '1-Ph2auxlinL5Y3bxE7AeeAeYE2KDALJT'

    @st.cache_data
    def list_excel_files_trung():
        service = get_drive_service()
        if not service:
            return {}
        query = f"'{FOLDER_ID_TRUNG}' in parents and mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'"
        try:
            results = service.files().list(q=query, fields="files(id, name)").execute()
            return {f['name']: f['id'] for f in results.get('files', [])}
        except Exception as e:
            st.error(f"Lỗi liệt kê file trung thế: {e}")
            return {}

    all_files_trung = list_excel_files_trung()
    nam = st.selectbox("Chọn năm", list(range(2020, datetime.now().year + 1))[::-1], index=0, key="trung_nam")
    loai_bc = st.radio("Loại báo cáo", ["Tháng", "Lũy kế"], horizontal=True, key="trung_loai_bc")
    thang = st.selectbox("Chọn tháng", list(range(1, 13)), index=0, key="trung_thang")

    months = list(range(1, 13))
    df_th = pd.DataFrame({"Tháng": months, "Tỷ lệ": [None]*12})
    df_ck = pd.DataFrame({"Tháng": months, "Tỷ lệ": [None]*12})

    tong_ton_that = 0
    tong_thuong_pham = 0

    for i in range(1, 13):
        fname = f"TA_{nam}_{i:02}.xlsx"
        file_id = all_files_trung.get(fname)

        if file_id and i <= thang:
            df = download_excel(file_id)
            if not df.empty and df.shape[0] >= 1:
                try:
                    ty_le_th = float(str(df.iloc[0, 4]).replace(",", "."))
                    ton_that = float(str(df.iloc[0, 3]).replace(",", "."))
                    thuong_pham = float(str(df.iloc[0, 1]).replace(",", "."))

                    if loai_bc == "Lũy kế":
                        tong_ton_that += ton_that
                        tong_thuong_pham += thuong_pham
                        ty_le_lk = (tong_ton_that / tong_thuong_pham) * 100 if tong_thuong_pham > 0 else 0
                        df_th.loc[df_th["Tháng"] == i, "Tỷ lệ"] = ty_le_lk
                    else:
                        df_th.loc[df_th["Tháng"] == i, "Tỷ lệ"] = ty_le_th
                except:
                    st.warning(f"Lỗi đọc file: {fname}")

        fname_ck = f"TA_{nam - 1}_{i:02}.xlsx"
        file_id_ck = all_files_trung.get(fname_ck)
        if file_id_ck:
            df_ck_file = download_excel(file_id_ck)
            if not df_ck_file.empty and df_ck_file.shape[0] >= 1:
                try:
                    ty_le_ck = float(str(df_ck_file.iloc[0, 4]).replace(",", "."))
                    df_ck.loc[df_ck["Tháng"] == i, "Tỷ lệ"] = ty_le_ck
                except:
                    pass

    if df_th["Tỷ lệ"].notna().any():
        fig, ax = plt.subplots(figsize=(6, 3), dpi=600)

        ax.plot(df_th["Tháng"], df_th["Tỷ lệ"], color='#1f77b4', label='Thực hiện', linewidth=1, markersize=3, marker='o')
        if df_ck["Tỷ lệ"].notna().any():
            ax.plot(df_ck["Tháng"], df_ck["Tỷ lệ"], color='#ff7f0e', label='Cùng kỳ', linewidth=1, markersize=3, marker='o')

        for i, v in df_th.dropna(subset=["Tỷ lệ"]).iterrows():
            ax.text(v["Tháng"], v["Tỷ lệ"] + 0.05, f"{v['Tỷ lệ']:.2f}", ha='center', fontsize=6, color='black')

        if df_ck["Tỷ lệ"].notna().any():
            for i, v in df_ck.dropna(subset=["Tỷ lệ"]).iterrows():
                ax.text(v["Tháng"], v["Tỷ lệ"] + 0.05, f"{v['Tỷ lệ']:.2f}", ha='center', fontsize=6, color='black')

        ax.set_ylabel("Tỷ lệ (%)", fontsize=7, color='black')
        ax.set_xlabel("Tháng", fontsize=7, color='black')
        ax.set_xticks(months)
        ax.tick_params(axis='both', colors='black', labelsize=6)
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
        ax.set_title("Biểu đồ tỷ lệ tổn thất trung thế", fontsize=9, color='black')
        ax.legend(fontsize=7, frameon=False)

        st.pyplot(fig)
        st.dataframe(df_th)

    else:
        st.warning("Không có dữ liệu phù hợp để hiển thị.")
FOLDER_ID_DY = '1ESynjLXJrw8TaF3zwlQm-BR3mFf4LIi9'

@st.cache_data
def get_drive_service():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["google"],
        scopes=["https://www.googleapis.com/auth/drive.readonly"]
    )
    return build('drive', 'v3', credentials=credentials)

@st.cache_data
def list_excel_files():
    service = get_drive_service()
    query = f"'{FOLDER_ID_DY}' in parents and mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return {f['name']: f['id'] for f in results.get('files', [])}

@st.cache_data
def download_excel(file_id):
    service = get_drive_service()
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return pd.read_excel(fh, sheet_name=0)

st.set_page_config(layout="wide", page_title="Báo cáo tổn thất Đường dây Trung thế")

with st.expander("⚡ Tổn thất các đường dây trung thế"):
    st.header("Phân tích dữ liệu tổn thất đường dây trung thế")

    all_files = list_excel_files()

    all_years = sorted({int(fname.split("_")[1]) for fname in all_files.keys() if "_" in fname})

    selected_year = st.selectbox("Chọn năm", all_years)
    include_cungkỳ = st.checkbox("So sánh cùng kỳ năm trước", value=True)
    mode = st.radio("Chọn chế độ báo cáo", ["Tháng", "Lũy kế"], horizontal=True)
    chart_type = st.radio("Chọn kiểu biểu đồ", ["Cột", "Đường line"], horizontal=True)

    data_list = []

    for fname, file_id in all_files.items():
        try:
            year = int(fname.split("_")[1])
            month = int(fname.split("_")[2].split(".")[0])
        except:
            continue

        if year == selected_year or (include_cungkỳ and year == selected_year - 1):
            df = download_excel(file_id)

            for idx, row in df.iterrows():
                ten_dd = str(row.iloc[1]).strip()
                dien_ton_that = row.iloc[5]
                thuong_pham = row.iloc[2]
                ky = "Cùng kỳ" if year == selected_year - 1 else "Thực hiện"

                data_list.append({
                    "Năm": year,
                    "Tháng": month,
                    "Đường dây": ten_dd,
                    "Điện tổn thất": dien_ton_that,
                    "Thương phẩm": thuong_pham,
                    "Kỳ": ky
                })

    df_all = pd.DataFrame(data_list)

    if not df_all.empty:
        duong_day_list = df_all["Đường dây"].unique()

        for dd in duong_day_list:
            df_dd = df_all[df_all["Đường dây"] == dd]

            df_dd = df_dd.sort_values("Tháng")

            if mode == "Lũy kế":
                df_dd["Tổng Điện tổn thất"] = df_dd.groupby(["Kỳ"])["Điện tổn thất"].cumsum()
                df_dd["Tổng Thương phẩm"] = df_dd.groupby(["Kỳ"])["Thương phẩm"].cumsum()
                df_dd["Tổn thất (%)"] = (df_dd["Tổng Điện tổn thất"] / df_dd["Tổng Thương phẩm"] * 100).round(2)
            else:
                df_dd["Tổn thất (%)"] = (df_dd["Điện tổn thất"] / df_dd["Thương phẩm"] * 100).round(2)

            pivot_df = df_dd.pivot(index="Tháng", columns="Kỳ", values="Tổn thất (%)").reindex(range(1, 13)).fillna(0)

            st.write(f"### Biểu đồ tỷ lệ tổn thất - Đường dây {dd}")

            fig, ax = plt.subplots(figsize=(10, 4), dpi=150)

            if chart_type == "Cột":
                pivot_df.plot(kind="bar", ax=ax)
                ax.set_xticklabels(pivot_df.index, rotation=0, ha='center') # Changed rotation to 0, ha='center'
                ax.tick_params(axis='y', labelrotation=0) # Ensure y-axis labels are not rotated
                for container in ax.containers:
                    for bar in container:
                        height = bar.get_height()
                        if height > 0:
                            ax.text(bar.get_x() + bar.get_width()/2, height + 0.2, f"{height:.2f}", ha='center', fontsize=7)
            else:
                for col in pivot_df.columns:
                    valid_data = pivot_df[col].replace(0, pd.NA).dropna()
                    ax.plot(valid_data.index, valid_data.values, marker='o', label=col)
                    for x, y in zip(valid_data.index, valid_data.values):
                        ax.text(x, y + 0.2, f"{y:.2f}", ha='center', fontsize=7)
                ax.set_xticks(range(1, 13))
                ax.set_xticklabels(range(1, 13), rotation=0, ha='center') # Changed rotation to 0, ha='center'
                ax.tick_params(axis='y', labelrotation=0) # Ensure y-axis labels are not rotated

            ax.set_xlabel("Tháng")
            ax.set_ylabel("Tổn thất (%)")
            ax.set_title(f"Đường dây {dd} - Năm {selected_year}")
            ax.legend()
            ax.grid(axis='y', linestyle='--', alpha=0.7)

            st.pyplot(fig, use_container_width=True)

    else:
        st.warning("Không có dữ liệu để hiển thị cho năm đã chọn.")
with st.expander("⚡ Tổn thất toàn đơn vị"):
    st.header("Phân tích dữ liệu toàn đơn vị")

    FOLDER_ID_TOAN_DON_VI = '1bPmINKlAHJMWUcxonMSnuLGz9ErlPEUi'

    @st.cache_data
    def list_excel_files_toan_don_vi():
        service = get_drive_service()
        if not service:
            return {}
        query = f"'{FOLDER_ID_TOAN_DON_VI}' in parents and mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'"
        try:
            results = service.files().list(q=query, fields="files(id, name)").execute()
            return {f['name']: f['id'] for f in results.get('files', [])}
        except Exception as e:
            st.error(f"Lỗi liệt kê file toàn đơn vị: {e}")
            return {}

    all_files_toan_don_vi = list_excel_files_toan_don_vi()
    nam = st.selectbox("Chọn năm", list(range(2020, datetime.now().year + 1))[::-1], index=0, key="dv_nam")
    loai_bc = st.radio("Loại báo cáo", ["Tháng", "Lũy kế"], horizontal=True, key="dv_loai_bc")
    thang = st.selectbox("Chọn tháng", list(range(1, 13)), index=0, key="dv_thang")

    months = list(range(1, 13))
    df_th = pd.DataFrame({"Tháng": months, "Tỷ lệ": [None]*12})
    df_ck = pd.DataFrame({"Tháng": months, "Tỷ lệ": [None]*12})

    tong_ton_that = 0
    tong_thuong_pham = 0

    for i in range(1, 13):
        fname = f"DV_{nam}_{i:02}.xlsx"
        file_id = all_files_toan_don_vi.get(fname)

        if file_id and i <= thang:
            df = download_excel(file_id)
            if not df.empty and df.shape[0] >= 1:
                try:
                    ty_le_th = float(str(df.iloc[0, 4]).replace(",", "."))
                    ton_that = float(str(df.iloc[0, 3]).replace(",", "."))
                    thuong_pham = float(str(df.iloc[0, 1]).replace(",", "."))

                    if loai_bc == "Lũy kế":
                        tong_ton_that += ton_that
                        tong_thuong_pham += thuong_pham
                        ty_le_lk = (tong_ton_that / tong_thuong_pham) * 100 if tong_thuong_pham > 0 else 0
                        df_th.loc[df_th["Tháng"] == i, "Tỷ lệ"] = ty_le_lk
                    else:
                        df_th.loc[df_th["Tháng"] == i, "Tỷ lệ"] = ty_le_th
                except:
                    st.warning(f"Lỗi đọc file: {fname}")

        fname_ck = f"DV_{nam - 1}_{i:02}.xlsx"
        file_id_ck = all_files_toan_don_vi.get(fname_ck)
        if file_id_ck:
            df_ck_file = download_excel(file_id_ck)
            if not df_ck_file.empty and df_ck_file.shape[0] >= 1:
                try:
                    ty_le_ck = float(str(df_ck_file.iloc[0, 4]).replace(",", "."))
                    df_ck.loc[df_ck["Tháng"] == i, "Tỷ lệ"] = ty_le_ck
                except:
                    pass

    if df_th["Tỷ lệ"].notna().any():
        fig, ax = plt.subplots(figsize=(6, 3), dpi=600)

        ax.plot(df_th["Tháng"], df_th["Tỷ lệ"], color='#1f77b4', label='Thực hiện', linewidth=1, markersize=3, marker='o')
        if df_ck["Tỷ lệ"].notna().any():
            ax.plot(df_ck["Tháng"], df_ck["Tỷ lệ"], color='#ff7f0e', label='Cùng kỳ', linewidth=1, markersize=3, marker='o')

        for i, v in df_th.dropna(subset=["Tỷ lệ"]).iterrows():
            ax.text(v["Tháng"], v["Tỷ lệ"] + 0.05, f"{v['Tỷ lệ']:.2f}", ha='center', fontsize=6, color='black')

        if df_ck["Tỷ lệ"].notna().any():
            for i, v in df_ck.dropna(subset=["Tỷ lệ"]).iterrows():
                ax.text(v["Tháng"], v["Tỷ lệ"] + 0.05, f"{v['Tỷ lệ']:.2f}", ha='center', fontsize=6, color='black')

        ax.set_ylabel("Tỷ lệ (%)", fontsize=7, color='black')
        ax.set_xlabel("Tháng", fontsize=7, color='black')
        ax.set_xticks(months)
        ax.tick_params(axis='both', colors='black', labelsize=6)
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
        ax.set_title("Biểu đồ tỷ lệ tổn thất toàn đơn vị", fontsize=9, color='black')
        ax.legend(fontsize=7, frameon=False)

        st.pyplot(fig)
        st.dataframe(df_th)

    else:
        st.warning("Không có dữ liệu phù hợp để hiển thị.")