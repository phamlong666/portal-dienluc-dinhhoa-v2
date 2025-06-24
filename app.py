
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Báo cáo tổn thất TBA", layout="wide")
st.title("📥 Tải dữ liệu đầu vào - Báo cáo tổn thất")

st.markdown("### 🔍 Chọn loại dữ liệu tổn thất để tải lên:")

# Tạo các tiện ích con theo phân nhóm
with st.expander("🔌 Tổn thất các TBA công cộng"):
    upload_tba_thang = st.file_uploader("📅 Tải dữ liệu TBA công cộng - Theo tháng", type=["xlsx"], key="tba_thang")
    upload_tba_luyke = st.file_uploader("📊 Tải dữ liệu TBA công cộng - Lũy kế", type=["xlsx"], key="tba_luyke")
    upload_tba_cungkyd = st.file_uploader("📈 Tải dữ liệu TBA công cộng - Cùng kỳ", type=["xlsx"], key="tba_ck")

with st.expander("⚡ Tổn thất hạ thế"):
    upload_ha_thang = st.file_uploader("📅 Tải dữ liệu hạ áp - Theo tháng", type=["xlsx"], key="ha_thang")
    upload_ha_luyke = st.file_uploader("📊 Tải dữ liệu hạ áp - Lũy kế", type=["xlsx"], key="ha_luyke")
    upload_ha_ck = st.file_uploader("📈 Tải dữ liệu hạ áp - Cùng kỳ", type=["xlsx"], key="ha_ck")

with st.expander("⚡ Tổn thất trung thế"):
    upload_Trung_thang = st.file_uploader("📅 Tải dữ liệu Trung áp - Theo tháng", type=["xlsx"], key="Trung_thang")
    upload_Trung_luyke = st.file_uploader("📊 Tải dữ liệu Trung áp - Lũy kế", type=["xlsx"], key="Trung_luyke")
    upload_Trung_ck = st.file_uploader("📈 Tải dữ liệu Trung áp - Cùng kỳ", type=["xlsx"], key="Trung_ck")

with st.expander("⚡ Tổn thất các đường dây trung thế"):
    upload_trung_thang = st.file_uploader("📅 Tải dữ liệu Trung áp - Theo tháng", type=["xlsx"], key="trung_thang")
    upload_trung_luyke = st.file_uploader("📊 Tải dữ liệu Trung áp - Lũy kế", type=["xlsx"], key="trung_luyke")
    upload_trung_ck = st.file_uploader("📈 Tải dữ liệu Trung áp - Cùng kỳ", type=["xlsx"], key="trung_ck")

with st.expander("🏢 Tổn thất toàn đơn vị"):
    upload_dv_thang = st.file_uploader("📅 Tải dữ liệu Đơn vị - Theo tháng", type=["xlsx"], key="dv_thang")
    upload_dv_luyke = st.file_uploader("📊 Tải dữ liệu Đơn vị - Lũy kế", type=["xlsx"], key="dv_luyke")
    upload_dv_ck = st.file_uploader("📈 Tải dữ liệu Đơn vị - Cùng kỳ", type=["xlsx"], key="dv_ck")

