<style>
    html, body, [class*="css"]  {
        font-size: 1.8em !important;
    }
</style>

import streamlit as st
import pandas as pd
import math
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from datetime import datetime
import zipfile
import xml.etree.ElementTree as ET
import json
import os
import io

st.set_page_config(layout="wide")
st.markdown("<style>html, body, [class*='css']  {font-size: 1.8em !important;}</style>", unsafe_allow_html=True)
st.title("📍 Dự báo điểm sự cố")

# ==============================
# (phần nội dung giữ nguyên sau dòng này...)

m = None  # khởi tạo bản đồ để ghép các PT lên chung
pt_markers = []

# ==============================
# 4. DỰ BÁO VỊ TRÍ SỰ CỐ THEO PHƯƠNG ÁN [PT3] - TỔNG TRỞ
# ==============================
st.subheader("🧮 [PT3] Dự báo theo tổng trở và dòng sự cố")

st.markdown("👉 Nhập tên đường dây và dòng sự cố để tính toán khoảng cách đến điểm sự cố.")

col1, col2 = st.columns(2)
with col1:
    ten_duongday = st.text_input("🔌 Nhập tên đường dây (ví dụ: 471 E6.22)")
with col2:
    dong_suco_pt3 = st.text_input("📈 Nhập dòng sự cố (ví dụ: Ia=1032; Ib=928; Ic=112)")

uploaded_qlkt = st.file_uploader("📎 Tải file chứa sheet QLKT (Excel)", type="xlsx")

if st.button("📊 Phân tích tổng trở") and uploaded_qlkt and ten_duongday and dong_suco_pt3:
    try:
        df_qlkt = pd.read_excel(uploaded_qlkt, sheet_name="QLKT")
        row = df_qlkt[df_qlkt["Tên đường dây"].astype(str).str.contains(ten_duongday, case=False)]
        if not row.empty:
            chieu_dai_km = float(row.iloc[0]["File/số liệu đã gửi"].split("chiều dài ")[1].split("km")[0].strip())
            chieu_dai_m = chieu_dai_km * 1000
            tiet_dien = 70  # giả định dây AC70
            dien_tro_suat = 0.028  # Ω·mm²/m (nhôm)
            z = round(dien_tro_suat * chieu_dai_m / tiet_dien, 2)

            dong_raw = dong_suco_pt3.replace(';', ' ').replace(',', ' ')
            dong_raw = dong_raw.replace('Ia=', '').replace('Ib=', '').replace('Ic=', '')
            values = [float(s.strip()) for s in dong_raw.split() if s.strip().replace('.', '', 1).isdigit()]

            if len(values) >= 3:
                tong_dong = sum(values[:3])
                u_dinh_muc = 22000  # 22kV
                kc_m = round((u_dinh_muc / tong_dong) * z, 2)
                so_cot = int(kc_m // 80)

                st.success(f"📏 Tổng trở Z = {z} Ω | Dòng sự cố: {tong_dong} A")
                st.info(f"📌 Dự báo khoảng cách đến điểm sự cố: {kc_m} m → khoảng cột thứ {so_cot}")

                # Thêm marker PT3 vào bản đồ chung
                if marker_locations:
                    for name, (lat, lon) in marker_locations.items():
                        if ten_duongday.replace(' ', '').split('.')[0][-3:] in name:
                            pt_markers.append((lat, lon, f"[PT3] Cột gần {so_cot}"))
                            break

                # Khởi tạo bản đồ nếu chưa có
                if not m and pt_markers:
                    m = folium.Map(location=pt_markers[0][:2], zoom_start=14)

                # Gắn tất cả marker PT vào bản đồ
                for lat, lon, label in pt_markers:
                    folium.Marker(
                        location=[lat, lon],
                        popup=label,
                        icon=folium.Icon(color='green')
                    ).add_to(m)

                if m:
                    st_folium(m, width=900, height=500)
            else:
                st.warning("⚠️ Dữ liệu dòng sự cố chưa đủ để tính toán")
        else:
            st.warning("⚠️ Không tìm thấy thông tin đường dây trong sheet QLKT")
    except Exception as e:
        st.error(f"❌ Lỗi xử lý: {e}")
