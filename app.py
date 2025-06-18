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
import re

st.set_page_config(layout="wide")
st.markdown("<style>html, body, [class*='css']  {font-size: 1.3em !important;}</style>", unsafe_allow_html=True)
st.title("📍 Dự báo điểm sự cố")

marker_locations = {}
kmz_file = st.file_uploader("📂 Tải file KMZ để lấy dữ liệu tọa độ cột", type="kmz")
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
    st.success(f"✅ Đã trích xuất {len(marker_locations)} điểm từ file KMZ.")

st.subheader("📝 Nhập các vụ sự cố lịch sử")
uploaded_excel = st.file_uploader("📥 Tải dữ liệu lịch sử từ file Excel (.xlsx)", type="xlsx")
if uploaded_excel is not None:
    try:
        df_uploaded = pd.read_excel(uploaded_excel)
        st.session_state.suco_data = df_uploaded.to_dict(orient="records")
        st.success("✅ Đã nạp dữ liệu lịch sử từ file thành công.")
    except Exception as e:
        st.warning(f"⚠️ Không thể đọc file: {e}")

if "suco_data" not in st.session_state:
    st.session_state.suco_data = []

with st.form("suco_form"):
    col1, col2 = st.columns(2)
    with col1:
        ten_mc = st.text_input("Tên máy cắt")
        ngay = st.date_input("Ngày xảy ra sự cố", format="DD/MM/YYYY")
        dong_suco = st.text_input("Dòng sự cố (Ia, Ib, Ic, Io, 3Uo...)")
        loai_suco = st.selectbox("Loại sự cố", [
            "1 pha chạm đất (Io)",
            "2 pha chạm đất (Ia+Ib)",
            "3 pha chạm đất (Ia+Ib+Ic)",
            "Ngắn mạch 2 pha (Ia+Ib)",
            "Ngắn mạch 3 pha (Ia+Ib+Ic)",
            "Ngắn mạch 2 pha có Io (Ia+Ib+Io)",
            "Ngắn mạch 3 pha có Io (Ia+Ib+Ic+Io)",
            "Ngắn mạch 1 pha có Io (Ia+Io)",
            "Ngắn mạch 2 pha có Io (Ib+Ic+Io)",
            "Ngắn mạch 3 pha có Io (Ia+Ib+Ic+Io)"
        ])
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
            "Loại sự cố": loai_suco,
            "Vị trí": vi_tri,
            "Nguyên nhân": nguyen_nhan,
            "Thời tiết": thoi_tiet
        })
        st.success("✔️ Đã lưu vụ sự cố!")

if st.session_state.suco_data:
    st.write("### 📋 Danh sách sự cố đã nhập")
    df_suco = pd.DataFrame(st.session_state.suco_data)
    edited_df = st.data_editor(df_suco, num_rows="dynamic", use_container_width=True)

    if st.button("Cập nhật dữ liệu đã sửa"):
        st.session_state.suco_data = edited_df.to_dict(orient="records")
        st.success("✔️ Đã cập nhật danh sách sau khi chỉnh sửa!")

    def convert_df(df):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='SuCo', index=False)
        writer.close()
        return output.getvalue()

    st.download_button(
        label="📤 Xuất báo cáo Excel",
        data=convert_df(df_suco),
        file_name="bao_cao_su_co.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    df_suco.to_excel("du_lieu_su_co.xlsx", index=False)

# ============================
# TÍNH TOÁN KHOẢNG CÁCH SỰ CỐ
# ============================
def extract_current(dong_suco_str, loai_suco):
    try:
        values = re.findall(r'\d+', dong_suco_str)
        values = [int(v) for v in values]
        if not values:
            return None
        if "Io" in loai_suco:
            return values[-1]  # mặc định Io là cuối
        else:
            return sum(values)
    except:
        return None

def tinh_khoang_cach(I_suco, U0_kV, z_ohm_per_km):
    try:
        U0 = U0_kV * 1000  # Đã là điện áp pha
        return round((U0 / (I_suco * z_ohm_per_km)), 2)
    except:
        return None

st.subheader("🔍 Dự báo điểm sự cố từ dòng điện")
ten_mc_input = st.text_input("Tên máy cắt muốn dự báo")
dong_input = st.text_input("Dòng sự cố (ví dụ: Ia=500, Ib=600, Ic=50, Io=400)")
cap_dien_ap = st.selectbox("Cấp điện áp đường dây", ["22kV", "35kV", "110kV"])
loai_suco_input = st.selectbox("Loại sự cố", [
    "1 pha chạm đất (Io)",
    "2 pha chạm đất (Ia+Ib)",
    "3 pha chạm đất (Ia+Ib+Ic)",
    "Ngắn mạch 2 pha (Ia+Ib)",
    "Ngắn mạch 3 pha (Ia+Ib+Ic)",
    "Ngắn mạch 2 pha có Io (Ia+Ib+Io)",
    "Ngắn mạch 3 pha có Io (Ia+Ib+Ic+Io)",
    "Ngắn mạch 1 pha có Io (Ia+Io)",
    "Ngắn mạch 2 pha có Io (Ib+Ic+Io)",
    "Ngắn mạch 3 pha có Io (Ia+Ib+Ic+Io)"
])

if st.button("Phân tích"):
    U0_map = {"22kV": 22000 / math.sqrt(3), "35kV": 35000 / math.sqrt(3), "110kV": 110000 / math.sqrt(3)}
    z_default = 0.3  # suất trở mặc định
    I = extract_current(dong_input, loai_suco_input)
    if I:
        d = tinh_khoang_cach(I, U0_map[cap_dien_ap], z_default)
        if d:
            st.success(f"✅ Khoảng cách dự kiến đến điểm sự cố: {d} km")
        else:
            st.warning("⚠️ Không tính được khoảng cách.")
    else:
        st.warning("⚠️ Không nhận diện được dòng sự cố hợp lệ.")

# BỔ SUNG: Dự báo từ dữ liệu lịch sử
st.subheader("📚 Dự báo điểm sự cố từ dữ liệu lịch sử")
ten_mc_ls = st.text_input("🔎 Nhập tên máy cắt để lọc dữ liệu")
dong_moi = st.text_input("Nhập dòng sự cố mới (Ia, Ib, Ic, Io)")
if dong_moi:
    try:
        input_values = [int(x.strip()) for x in re.findall(r'\d+', dong_moi)]
        def euclidean(a, b):
            return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

        min_dist = float('inf')
        nearest_case = None
        for case in st.session_state.suco_data:
            try:
                if ten_mc_ls and ten_mc_ls not in case.get("Tên máy cắt", ""):
                    continue
                case_values = [int(x.strip()) for x in re.findall(r'\d+', case["Dòng sự cố"])]
                if len(case_values) == len(input_values):
                    dist = euclidean(input_values, case_values)
                    if dist < min_dist:
                        min_dist = dist
                        nearest_case = case
            except:
                continue

        if nearest_case:
            st.success(f"✅ Dự báo gần nhất theo lịch sử: {nearest_case['Vị trí']} – Nguyên nhân: {nearest_case['Nguyên nhân']}")
        else:
            st.warning("⚠️ Không tìm thấy dòng sự cố tương đồng trong dữ liệu lịch sử.")
    except:
        st.warning("⚠️ Định dạng dòng sự cố không hợp lệ. Vui lòng nhập theo dạng: 500, 600, 50, 400")
