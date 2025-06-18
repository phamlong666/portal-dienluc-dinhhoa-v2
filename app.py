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
st.title("📍 Dự báo điểm sự cố")

# ==============================
# 1. TẢI FILE KMZ VÀ CHUYỂN THÀNH marker_locations.json
# ==============================
st.subheader("📂 Cập nhật bản đồ bằng file .KMZ")

kmz_file = st.file_uploader("Tải lên file KMZ", type="kmz")
marker_locations = {}

if kmz_file is not None:
    with zipfile.ZipFile(kmz_file, 'r') as z:
        for filename in z.namelist():
            if filename.endswith('.kml'):
                with z.open(filename) as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
                    for pm in root.findall('.//kml:Placemark', ns):
                        name_tag = pm.find('kml:name', ns)
                        point = pm.find('.//kml:coordinates', ns)
                        if name_tag is not None and point is not None:
                            name = name_tag.text.strip()
                            coords = point.text.strip().split(',')
                            lon, lat = float(coords[0]), float(coords[1])
                            marker_locations[name] = (lat, lon)
    st.success(f"✔️ Đã trích xuất {len(marker_locations)} điểm từ file KMZ.")
    with open("marker_locations.json", "w") as f:
        json.dump(marker_locations, f)

# ==============================
# 2. BẢNG NHẬP THỦ CÔNG CÁC VỤ SỰ CỐ GẦN ĐÂY
# ==============================
st.subheader("📝 Nhập thủ công các vụ sự cố gần nhất")

if "suco_data" not in st.session_state:
    st.session_state.suco_data = []

with st.form("suco_form"):
    col1, col2 = st.columns(2)
    with col1:
        ten_mc = st.text_input("Tên máy cắt")
        ngay = st.date_input("Ngày xảy ra sự cố", format="DD/MM/YYYY")
        dong_suco = st.text_input("Dòng sự cố (Ia, Ib, Ic, Io, 3Uo...)")
    with col2:
        vi_tri = st.text_input("Vị trí sự cố")
        nguyen_nhan = st.text_input("Nguyên nhân")
        thoi_tiet = st.text_input("Thời tiết")

    submitted = st.form_submit_button("Lưu vụ sự cố")
    if submitted:
        st.session_state.suco_data.append({
            "Tên máy cắt": ten_mc,
            "Ngày": ngay.strftime("%d/%m/%Y"),
            "Dòng sự cố": dong_suco,
            "Vị trí": vi_tri,
            "Nguyên nhân": nguyen_nhan,
            "Thời tiết": thoi_tiet
        })
        st.success("✔️ Đã lưu vụ sự cố!")

# Hiển thị bảng đã lưu và cho phép sửa/xóa
if st.session_state.suco_data:
    st.write("### 📋 Danh sách sự cố đã nhập")
    df_suco = pd.DataFrame(st.session_state.suco_data)
    edited_df = st.data_editor(df_suco, num_rows="dynamic", use_container_width=True)

    # Cập nhật lại dữ liệu nếu sửa
    if st.button("Cập nhật dữ liệu đã sửa"):
        st.session_state.suco_data = edited_df.to_dict(orient="records")
        st.success("✔️ Đã cập nhật danh sách sau khi chỉnh sửa!")

    # Cho phép xuất Excel
    def convert_df(df):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='SuCo', index=False)
        return output.getvalue()

    st.download_button(
        label="📤 Xuất báo cáo Excel",
        data=convert_df(df_suco),
        file_name="bao_cao_su_co.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# (Phần phân tích sự cố và hiển thị marker sẽ được ghép ở giai đoạn tiếp theo)
