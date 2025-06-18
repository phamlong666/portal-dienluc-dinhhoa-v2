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

uploaded_recovery_file = st.file_uploader("🔁 Nhập lại dữ liệu từ file Excel đã lưu trước đó:", type="xlsx")
if uploaded_recovery_file:
    try:
        df_recovery = pd.read_excel(uploaded_recovery_file)
        st.session_state.suco_data = df_recovery.to_dict(orient="records")
        st.success("✅ Đã khôi phục dữ liệu từ file thành công!")
    except Exception as e:
        st.error(f"❌ Lỗi đọc file: {e}")

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
# 2. NHẬP CÁC VỤ SỰ CỐ LỊCH SỬ
# ==============================
st.subheader("📚 Nhập các vụ sự cố lịch sử")

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

# ==============================
# 3. NHẬP DÒNG SỰ CỐ MỚI ĐỂ DỰ BÁO VỊ TRÍ
# ==============================
st.subheader("🔍 Nhập dòng sự cố mới để dự báo vị trí")

if marker_locations:
    col1, col2 = st.columns(2)
    with col1:
        ten_mc_new = st.text_input("🔧 Nhập tên máy cắt để lọc tuyến (ví dụ: MC471, MC472)")
    with col2:
        dong_input = st.text_input("🔌 Nhập dòng sự cố (ví dụ: Ia=1032; Ib=928; Ic=112; Io=400):")

    if st.button("🔎 Phân tích"):
        if dong_input and ten_mc_new:
            try:
                dong_raw = dong_input.replace(';', ' ').replace(',', ' ')
                dong_raw = dong_raw.replace('Ia=', '').replace('Ib=', '').replace('Ic=', '').replace('Io=', '').replace('In=', '').replace('3Uo=', '')
                values = [float(s.strip()) for s in dong_raw.split() if s.strip().replace('.', '', 1).isdigit()]

                if len(values) >= 3:
                    tong_dong = sum(values[:3])

                    # Phân tích 1: Dự báo theo marker gần đúng
                    min_dist = float('inf')
                    predicted_marker = None
                    for name, (lat, lon) in marker_locations.items():
                        if ten_mc_new in name:
                            approx_score = abs(hash(name) % 1000 - tong_dong)
                            if approx_score < min_dist:
                                min_dist = approx_score
                                predicted_marker = (name, lat, lon)

                    if predicted_marker:
                        st.success(f"📌 [PT1] Dự báo theo đường dây: {predicted_marker[0]} (Lat: {predicted_marker[1]}, Lon: {predicted_marker[2]})")
                        m = folium.Map(location=[predicted_marker[1], predicted_marker[2]], zoom_start=15)
                        folium.Marker(location=[predicted_marker[1], predicted_marker[2]], popup=predicted_marker[0], icon=folium.Icon(color='blue')).add_to(m)
                        st_folium(m, width=900, height=500)

                    # Phân tích 2: Dự báo theo vụ sự cố lịch sử gần nhất
                    if st.session_state.suco_data:
                        min_diff = float('inf')
                        matched = None
                        for row in st.session_state.suco_data:
                            if ten_mc_new.lower() in row['Tên máy cắt'].lower():
                                dong_hist = row['Dòng sự cố']
                                dong_hist_raw = dong_hist.replace(';', ' ').replace(',', ' ')
                                dong_hist_raw = dong_hist_raw.replace('Ia=', '').replace('Ib=', '').replace('Ic=', '').replace('Io=', '').replace('In=', '').replace('3Uo=', '')
                                values_hist = [float(s.strip()) for s in dong_hist_raw.split() if s.strip().replace('.', '', 1).isdigit()]
                                if len(values_hist) >= 3:
                                    diff = sum(abs(a - b) for a, b in zip(values[:3], values_hist[:3]))
                                    if diff < min_diff:
                                        min_diff = diff
                                        matched = row

                        if matched:
                            st.info(f"📌 [PT2] Dự báo theo lịch sử: {matched['Vị trí']} (từ vụ: {matched['Ngày']})")

                else:
                    st.warning("⚠️ Dữ liệu dòng sự cố không đủ để dự báo")
            except Exception as e:
                st.error(f"❌ Lỗi xử lý dòng sự cố: {e}")
else:
    st.info("ℹ️ Cần tải file KMZ để dự báo được vị trí.")
