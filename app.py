import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# ... (your existing code) ...

with st.expander("🔌 Tổn thất các TBA công cộng"):
    temp_upload_tba_thang = st.file_uploader("📅 Tải dữ liệu TBA công cộng - Theo tháng", type=["xlsx"], key="tba_thang")
    if temp_upload_tba_thang:
        # --- DEBUGGING STEP: INSPECT SHEET NAMES ---
        try:
            xls = pd.ExcelFile(temp_upload_tba_thang)
            st.info(f"Các sheet có trong file: {xls.sheet_names}")
            # If 'Bảng Kết quả ánh xạ dữ liệu' is not listed, you have your answer!
        except Exception as e:
            st.error(f"Không thể đọc sheet names: {e}")
        # --- END DEBUGGING STEP ---

        try:
            st.session_state.df_tba_thang = pd.read_excel(temp_upload_tba_thang, sheet_name="Bảng Kết quả ánh xạ dữ liệu", skiprows=6)
            st.success("✅ Đã tải dữ liệu tổn thất TBA công cộng theo tháng!")
        except ValueError as e:
            st.error(f"Lỗi khi đọc sheet 'Bảng Kết quả ánh xạ dữ liệu': {e}. Vui lòng kiểm tra tên sheet trong file Excel.")
            st.session_state.df_tba_thang = None # Clear the session state if there's an error
        except Exception as e:
            st.error(f"Đã xảy ra lỗi không mong muốn khi đọc file: {e}")
            st.session_state.df_tba_thang = None


    temp_upload_tba_luyke = st.file_uploader("📊 Tải dữ liệu TBA công cộng - Lũy kế", type=["xlsx"], key="tba_luyke")
    if temp_upload_tba_luyke:
        # --- DEBUGGING STEP: INSPECT SHEET NAMES ---
        try:
            xls = pd.ExcelFile(temp_upload_tba_luyke)
            st.info(f"Các sheet có trong file Lũy kế: {xls.sheet_names}")
        except Exception as e:
            st.error(f"Không thể đọc sheet names Lũy kế: {e}")
        # --- END DEBUGGING STEP ---

        try:
            st.session_state.df_tba_luyke = pd.read_excel(temp_upload_tba_luyke, sheet_name="Bảng Kết quả ánh xạ dữ liệu", skiprows=6)
            st.success("✅ Đã tải dữ liệu tổn thất TBA công cộng - Lũy kế!")
        except ValueError as e:
            st.error(f"Lỗi khi đọc sheet 'Bảng Kết quả ánh xạ dữ liệu' cho file Lũy kế: {e}. Vui lòng kiểm tra tên sheet.")
            st.session_state.df_tba_luyke = None
        except Exception as e:
            st.error(f"Đã xảy ra lỗi không mong muốn khi đọc file Lũy kế: {e}")
            st.session_state.df_tba_luyke = None

    temp_upload_tba_ck = st.file_uploader("📈 Tải dữ liệu TBA công cộng - Cùng kỳ", type=["xlsx"], key="tba_ck")
    if temp_upload_tba_ck:
        # --- DEBUGGING STEP: INSPECT SHEET NAMES ---
        try:
            xls = pd.ExcelFile(temp_upload_tba_ck)
            st.info(f"Các sheet có trong file Cùng kỳ: {xls.sheet_names}")
        except Exception as e:
            st.error(f"Không thể đọc sheet names Cùng kỳ: {e}")
        # --- END DEBUGGING STEP ---
        try:
            st.session_state.df_tba_ck = pd.read_excel(temp_upload_tba_ck, sheet_name="Bảng Kết quả ánh xạ dữ liệu", skiprows=6)
            st.success("✅ Đã tải dữ liệu tổn thất TBA công cộng - Cùng kỳ!")
        except ValueError as e:
            st.error(f"Lỗi khi đọc sheet 'Bảng Kết quả ánh xạ dữ liệu' cho file Cùng kỳ: {e}. Vui lòng kiểm tra tên sheet.")
            st.session_state.df_tba_ck = None
        except Exception as e:
            st.error(f"Đã xảy ra lỗi không mong muốn khi đọc file Cùng kỳ: {e}")
            st.session_state.df_tba_ck = None

# ... (Continue with similar try-except blocks and sheet name debugging for other file uploaders) ...