
import streamlit as st
import pandas as pd
import os
from PIL import Image

st.set_page_config(page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa", layout="wide")

st.markdown("""
    <style>
        section[data-testid="stSidebar"] > div:first-child {
            max-height: 95vh;
            overflow-y: auto;
        }

        .sidebar-button {
            display: block;
            background-color: #66a3ff;
            color: white;
            padding: 10px;
            border-radius: 8px;
            margin: 5px 0;
            font-weight: bold;
            box-shadow: 1px 1px 3px rgba(0,0,0,0.3);
            transition: all 0.2s ease-in-out;
            text-decoration: none;
        }

        .sidebar-button:hover {
            background-color: #3385ff !important;
            transform: translateY(-2px);
            box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
        }

        .main-button {
            display: inline-block;
            background-color: #66a3ff;
            color: white;
            text-align: center;
            padding: 22px 30px;
            border-radius: 14px;
            font-weight: bold;
            text-decoration: none;
            margin: 14px;
            transition: 0.3s;
            font-size: 24px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        }

        .main-button:hover {
            transform: scale(1.07);
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 10])
with col1:
    try:
        logo = Image.open("assets/logo_hinh_tron_hoan_chinh.png")
        st.image(logo, width=70)
    except:
        st.warning("⚠️ Không tìm thấy logo.")

with col2:
    st.markdown("""
        <h1 style='color:#003399; font-size:42px; margin-top:18px;'>
        Trung tâm điều hành số - phần mềm Điện lực Định Hóa
        </h1>
        <p style='font-size:13px; color:gray;'>Bản quyền © 2025 by Phạm Hồng Long & Brown Eyes</p>
    """, unsafe_allow_html=True)

sheet_url = "https://docs.google.com/spreadsheets/d/18kYr8DmDLnUUYzJJVHxzit5KCY286YozrrrIpOeojXI/gviz/tq?tqx=out:csv"

try:
    df = pd.read_csv(sheet_url)
    df = df[['Tên ứng dụng', 'Liên kết', 'Nhóm chức năng']].dropna()

    grouped = df.groupby('Nhóm chức năng')

    st.sidebar.markdown("<h3 style='color:#003399'>📚 Danh mục hệ thống</h3>", unsafe_allow_html=True)

    for group_name, group_data in grouped:
        with st.sidebar.expander(f"📂 {group_name}", expanded=False):
            for _, row in group_data.iterrows():
                label = row['Tên ứng dụng']
                link = row['Liên kết']
                st.markdown(f"""
                    <a href="{link}" target="_blank" class="sidebar-button">
                        🚀 {label}
                    </a>
                """, unsafe_allow_html=True)
except Exception as e:
    st.sidebar.error(f"🚫 Không thể tải menu từ Google Sheet. Lỗi: {e}")

st.info("""
👋 Chào mừng bạn đến với Trung tâm điều hành số - phần mềm Điện lực Định Hóa

📌 **Các tính năng nổi bật:**
- Phân tích tổn thất, báo cáo kỹ thuật
- Lưu trữ và truy xuất lịch sử GPT
- Truy cập hệ thống nhanh chóng qua Sidebar

✅ Mọi bản cập nhật chỉ cần chỉnh sửa Google Sheet đều tự động hiển thị!
""")

st.markdown("<br>", unsafe_allow_html=True)

# Thêm nút Phục vụ họp + chức năng phía sau
col = st.columns(5)
with col[0]:
    st.markdown('<a href="?hop=1" class="main-button">🧾 Phục vụ họp</a>', unsafe_allow_html=True)
with col[1]:
    st.markdown('<a href="https://terabox.com/s/1cegqu7nP7rd0BdL_MIyrtA" target="_blank" class="main-button">📦 Bigdata_Terabox</a>', unsafe_allow_html=True)
with col[2]:
    st.markdown('<a href="https://chat.openai.com" target="_blank" class="main-button">💬 ChatGPT công khai</a>', unsafe_allow_html=True)
with col[3]:
    st.markdown('<a href="https://www.youtube.com/@dienlucdinhhoa" target="_blank" class="main-button">🎬 video tuyên truyền</a>', unsafe_allow_html=True)
with col[4]:
    st.markdown('<a href="https://www.dropbox.com/home/3.%20Bao%20cao/4.%20B%C3%A1o%20c%C3%A1o%20CMIS" target="_blank" class="main-button">📄 Báo cáo CMIS</a>', unsafe_allow_html=True)

query = st.query_params
if "hop" in query:
    st.header("🧾 Phục vụ họp – Ghi báo cáo và xuất file")

    ten = st.text_input("🔹 Tên cuộc họp")
    ngay = st.date_input("📅 Ngày họp", value=pd.Timestamp.today())
    gio = st.time_input("🕐 Giờ họp", value=pd.to_datetime("07:30").time())
    nd = st.text_area("📝 Nội dung cuộc họp", height=250)
    files = st.file_uploader("📎 Đính kèm tài liệu", accept_multiple_files=True)

    def luu():
        df = pd.DataFrame([{
            "Tên cuộc họp": ten,
            "Ngày": ngay.strftime("%d/%m/%Y"),
            "Giờ": gio.strftime("%H:%M"),
            "Nội dung": nd,
            "Tệp đính kèm": ", ".join([f.name for f in files]) if files else ""
        }])
        if os.path.exists("lich_su_cuoc_hop.csv"):
            df.to_csv("lich_su_cuoc_hop.csv", mode="a", index=False, header=False, encoding="utf-8-sig")
        else:
            df.to_csv("lich_su_cuoc_hop.csv", index=False, encoding="utf-8-sig")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📤 Tạo Word"):
            st.success("✅ Đã tạo Word (demo)")
            luu()
    with col2:
        if st.button("📽️ Tạo PowerPoint"):
            st.success("✅ Đã tạo PowerPoint (demo)")
            luu()
    with col3:
        if st.button("📜 Lưu lịch sử"):
            luu()
            st.success("✅ Đã lưu vào file CSV")

    st.markdown("---")
    st.subheader("📚 Lịch sử cuộc họp đã lưu")
    if os.path.exists("lich_su_cuoc_hop.csv"):
        lich_su = pd.read_csv("lich_su_cuoc_hop.csv", encoding="utf-8-sig")
        for _, row in lich_su.iterrows():
            st.markdown(f"📅 **{row['Ngày']} {row['Giờ']}** – `{row['Tên cuộc họp']}`  <br>{row['Nội dung']}", unsafe_allow_html=True)
            if pd.notna(row["Tệp đính kèm"]):
                for f in row["Tệp đính kèm"].split(", "):
                    st.markdown(f"📎 {f}")
    else:
        st.info("Chưa có lịch sử nào.")
