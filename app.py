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
st.markdown("<style>html, body, [class*='css']  {font-size: 1.3em !important;}</style>", unsafe_allow_html=True)
st.title("📍 Dự báo điểm sự cố")

# ==============================
# ==============================
# 1. NÚT TẢI FILE KMZ
# ==============================
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

# ==============================
# NHẬP DỮ LIỆU LỊCH SỬ SỰ CỐ (PT2)
# ==============================
st.subheader("📝 Nhập các vụ sự cố lịch sử")

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
# 2. NHẬP TÊN MC + DÒNG SỰ CỐ ĐỂ DỰ BÁO [PT1, PT2]
# ==============================
st.subheader("📌 Phân tích sự cố tổng hợp")

col_a, col_b = st.columns(2)
with col_a:
    ten_mc_new = st.text_input("🔧 Nhập tên máy cắt để lọc tuyến (ví dụ: MC471, MC472)")
with col_b:
    dong_input = st.text_input("🔌 Nhập dòng sự cố (ví dụ: Ia=1032; Ib=928; Ic=112; Io=400)")

if st.button("🔎 Phân tích sự cố tổng hợp"):
    if dong_input and ten_mc_new:
        try:
            dong_raw = dong_input.replace(';', ' ').replace(',', ' ')
            dong_raw = dong_raw.replace('Ia=', '').replace('Ib=', '').replace('Ic=', '').replace('Io=', '').replace('In=', '').replace('3Uo=', '')
            values = [float(s.strip()) for s in dong_raw.split() if s.strip().replace('.', '', 1).isdigit()]

            if len(values) >= 3:
                tong_dong = sum(values[:3])

                # PT1: marker gần đúng
                min_dist = float('inf')
                predicted_marker = None
                for name, (lat, lon) in marker_locations.items():
                    if ten_mc_new in name:
                        approx_score = abs(hash(name) % 1000 - tong_dong)
                        if approx_score < min_dist:
                            min_dist = approx_score
                            predicted_marker = (name, lat, lon)
                if predicted_marker:
                    st.success(f"[PT1] Vị trí gần nhất theo đường dây: {predicted_marker[0]}")
                    pt_markers.append((predicted_marker[1], predicted_marker[2], f"[PT1] {predicted_marker[0]}"))

                # PT2: so sánh lịch sử
                if "suco_data" in st.session_state:
                    matched = None
                    min_diff = float('inf')
                    for row in st.session_state.suco_data:
                        if ten_mc_new.lower() in row['Tên máy cắt'].lower():
                            hist_raw = row['Dòng sự cố'].replace(';', ' ').replace(',', ' ')
                            hist_raw = hist_raw.replace('Ia=', '').replace('Ib=', '').replace('Ic=', '').replace('Io=', '').replace('In=', '')
                            vals = [float(s.strip()) for s in hist_raw.split() if s.strip().replace('.', '', 1).isdigit()]
                            if len(vals) >= 3:
                                diff = sum(abs(a - b) for a, b in zip(values[:3], vals[:3]))
                                if diff < min_diff:
                                    min_diff = diff
                                    matched = row
                    if matched:
                        st.info(f"[PT2] Gần nhất theo lịch sử: {matched['Vị trí']} ({matched['Ngày']})")
            else:
                st.warning("⚠️ Thiếu dữ liệu dòng sự cố")
        except Exception as e:
            st.error(f"❌ Lỗi xử lý PT1/PT2: {e}")

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
        sheet_names = pd.ExcelFile(uploaded_qlkt).sheet_names
        target_sheet = next((s for s in sheet_names if s.strip().lower() == "qlkt"), None)
        if not target_sheet:
            st.error("❌ Sheet 'QLKT' không tồn tại trong file.")
            raise ValueError("Missing QLKT sheet")
        df_qlkt = pd.read_excel(uploaded_qlkt, sheet_name=target_sheet)
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
                if len(values) >= 4:
                    # Với trung tính nối đất trực tiếp, nếu chạm đất thì lấy dòng Io
                    tong_dong = values[3]  # dòng Io
                else:
                    tong_dong = sum(values[:3])  # nếu không đủ thì lấy tổng 3 pha
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

                # ==============================
# XỬ LÝ LỖI marker_locations NẾU CHƯA ĐƯỢC KHAI BÁO
# ==============================
                if "marker_locations" not in globals():
                    marker_locations = {}

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
