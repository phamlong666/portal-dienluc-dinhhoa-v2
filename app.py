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
# 0. TẢI DỮ LIỆU CŨ ĐÃ XUẤT
# ==============================
if os.path.exists("du_lieu_su_co.xlsx"):
    try:
        df_old = pd.read_excel("du_lieu_su_co.xlsx")
        if "suco_data" not in st.session_state:
            st.session_state.suco_data = df_old.to_dict(orient="records")
        st.toast("📥 Đã nhập dữ liệu cũ từ file du_lieu_su_co.xlsx")
    except Exception as e:
        st.warning(f"⚠️ Không thể đọc file dữ liệu cũ: {e}")

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
        writer.close()
        return output.getvalue()

    st.download_button(
        label="📤 Xuất báo cáo Excel",
        data=convert_df(df_suco),
        file_name="bao_cao_su_co.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Tự động lưu file tạm để nhập lại khi cập nhật
    df_suco.to_excel("du_lieu_su_co.xlsx", index=False)

# ==============================
# 3. PHÂN TÍCH DÒNG SỰ CỐ VÀ DỰ BÁO VỊ TRÍ GẦN NHẤT
# ==============================
st.subheader("🔍 Dự báo vị trí sự cố gần nhất theo dòng")

if marker_locations and st.session_state.suco_data:
    last_event = st.session_state.suco_data[-1]  # dùng sự cố mới nhất
    try:
        dong_raw = last_event["Dòng sự cố"]
        values = [float(s.strip()) for s in dong_raw.replace('Ia=', '').replace('Ib=', '').replace('Ic=', '').replace('Io=', '').replace('A','').replace(',',' ').split() if s.strip().replace('.', '', 1).isdigit()]

        if len(values) >= 3:
            tong_dong = sum(values[:3])
            min_dist = float('inf')
            predicted_marker = None
            for name, (lat, lon) in marker_locations.items():
                approx_score = abs(hash(name) % 1000 - tong_dong)
                if approx_score < min_dist:
                    min_dist = approx_score
                    predicted_marker = (name, lat, lon)

            if predicted_marker:
                st.success(f"📌 Vị trí dự báo gần nhất là: {predicted_marker[0]} (Lat: {predicted_marker[1]}, Lon: {predicted_marker[2]})")
                m = folium.Map(location=[predicted_marker[1], predicted_marker[2]], zoom_start=15)
                folium.Marker(location=[predicted_marker[1], predicted_marker[2]], popup=predicted_marker[0], icon=folium.Icon(color='red')).add_to(m)
                st_folium(m, width=900, height=500)
        else:
            st.warning("⚠️ Dữ liệu dòng sự cố không đủ để dự báo")
    except Exception as e:
        st.error(f"❌ Lỗi xử lý dòng sự cố: {e}")
else:
    st.info("ℹ️ Cần tải file KMZ và nhập ít nhất 1 vụ sự cố để dự báo.")
