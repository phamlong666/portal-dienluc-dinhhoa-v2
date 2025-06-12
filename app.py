
import streamlit as st
import pandas as pd
import os
from PIL import Image
from datetime import datetime

st.set_page_config(page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa", layout="wide")

# ====== Logo và tiêu đề ======
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

# ====== Sidebar ======
sheet_url = "https://docs.google.com/spreadsheets/d/18kYr8DmDLnUUYzJJVHxzit5KCY286YozrrrIpOeojXI/gviz/tq?tqx=out:csv"
try:
    df = pd.read_csv(sheet_url)
    df = df[['Tên ứng dụng', 'Liên kết', 'Nhóm chức năng']].dropna()
    grouped = df.groupby('Nhóm chức năng')
    st.sidebar.markdown("<h3 style='color:#003399'>📚 Danh mục hệ thống</h3>", unsafe_allow_html=True)
    for group_name, group_data in grouped:
        with st.sidebar.expander(f"📂 {group_name}", expanded=False):
            for _, row in group_data.iterrows():
                st.markdown(f"""
                    <a href="{row['Liên kết']}" target="_blank" style="display:block; padding:8px; background-color:#66a3ff; color:white; border-radius:6px; margin:4px 0; text-decoration:none;">
                        🚀 {row['Tên ứng dụng']}
                    </a>
                """, unsafe_allow_html=True)
except Exception as e:
    st.sidebar.error(f"🚫 Không thể tải menu từ Google Sheet. Lỗi: {e}")

# ====== Giao diện chính hoặc phục vụ họp ======
query = st.query_params
if "hop" in query:
    # ========== TRANG PHỤC VỤ HỌP ==========
    st.title("🧾 Phục vụ họp – Ghi báo cáo và xuất file")

    ten = st.text_input("🔹 Tên cuộc họp")
    ngay = st.date_input("📅 Ngày họp", value=pd.Timestamp.today())
    gio = st.time_input("🕐 Giờ họp", value=pd.to_datetime("07:30").time())
    nd = st.text_area("📝 Nội dung cuộc họp", height=250)
    files = st.file_uploader("📎 Đính kèm tài liệu", accept_multiple_files=True)

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    def luu():
        saved_files = []
        if files:
            for file in files:
                file_path = os.path.join(upload_dir, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.read())
                saved_files.append(file_path)
        df = pd.DataFrame([{
            "Tên cuộc họp": ten,
            "Ngày": ngay.strftime("%d/%m/%Y"),
            "Giờ": gio.strftime("%H:%M"),
            "Nội dung": nd,
            "Tệp đính kèm": ", ".join(saved_files) if saved_files else ""
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
            st.success("✅ Lịch sử cuộc họp đã được lưu")

    st.markdown("---")
    st.subheader("📚 Lịch sử cuộc họp đã được lưu")

    if os.path.exists("lich_su_cuoc_hop.csv"):
        lich_su = pd.read_csv("lich_su_cuoc_hop.csv", encoding="utf-8-sig")

    for i, row in lich_su.iterrows():
            st.markdown(f"### 📅 {row['Ngày']} {row['Giờ']} – `{row['Tên cuộc họp']}`")
            st.write(row['Nội dung'])
            if row['Tệp đính kèm'] != '':
                st.write('📎 Tệp đính kèm:', row['Tệp đính kèm'])
            delete_nd = st.checkbox(f'Xoá nội dung dòng {i+1}', key=f'delnd_{i}')
            delete_file = st.checkbox(f'Xoá file đính kèm dòng {i+1}', key=f'delfile_{i}')
            if delete_nd:
                row['Nội dung'] = ''
                row['Nội dung'] = ''
            if delete_file:
                row['Tệp đính kèm'] = ''
                row['Tệp đính kèm'] = ''
    # Giao diện hiển thị từng dòng lịch sử
        if delete_nd:
            row['Nội dung'] = ''
        if delete_file:
            row['Tệp đính kèm'] = ''
        row['Tệp đính kèm'] = ''  # Xóa nội dung file đính kèm

            st.markdown(f"### 📅 {row['Ngày']} {row['Giờ']} – `{row['Tên cuộc họp']}`")
            st.markdown(f"{row['Nội dung']}")
            if pd.notna(row["Tệp đính kèm"]):
                for f in row["Tệp đính kèm"].split(", "):
                    try:
                        if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                            st.image(f, width=300)
                        elif f.lower().endswith('.pdf'):
                            st.markdown(f'<iframe src="{f}" width="100%" height="400px"></iframe>', unsafe_allow_html=True)
                        else:
                            st.markdown(f"📎 [{os.path.basename(f)}]({f})")
                    except:
                        st.warning(f"Không thể hiển thị file: {f}")
            if st.button(f"🗑️ Xoá dòng {i+1}", key=f"xoa_{i}"):
                lich_su = lich_su.drop(i)
                lich_su.to_csv("lich_su_cuoc_hop.csv", index=False, encoding="utf-8-sig")
                st.warning("🗑️ Đã xoá một dòng lịch sử cuộc họp")
                st.rerun()

        if st.button("🗑️ Xoá toàn bộ lịch sử"):
            os.remove("lich_su_cuoc_hop.csv")
            st.warning("🗑️ Đã xoá toàn bộ lịch sử cuộc họp")
    else:
        st.info("Chưa có lịch sử nào.")

else:
    # ========== TRANG CHÍNH ==========
    st.info("""
👋 Chào mừng bạn đến với Trung tâm điều hành số - phần mềm Điện lực Định Hóa

📌 **Các tính năng nổi bật:**
- Phân tích tổn thất, báo cáo kỹ thuật
- Lưu trữ và truy xuất lịch sử GPT
- Truy cập hệ thống nhanh chóng qua Sidebar

✅ Mọi bản cập nhật chỉ cần chỉnh sửa Google Sheet đều tự động hiển thị!
    """)

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