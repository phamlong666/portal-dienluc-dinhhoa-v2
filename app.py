
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa", layout="wide")

if "view" not in st.session_state:
    st.session_state["view"] = "home"

# Sidebar
sheet_url = "https://docs.google.com/spreadsheets/d/18kYr8DmDLnUUYzJJVHxzit5KCY286YozrrrIpOeojXI/gviz/tq?tqx=out:csv"
try:
    df = pd.read_csv(sheet_url)
    df = df[['Tên ứng dụng', 'Liên kết', 'Nhóm chức năng']].dropna()
    grouped = df.groupby('Nhóm chức năng')
    st.sidebar.markdown("<h3 style='color:#003399'>📚 Danh mục hệ thống</h3>", unsafe_allow_html=True)
    for group_name, group_data in grouped:
        with st.sidebar.expander(f"📂 {group_name}", expanded=False):
            for _, row in group_data.iterrows():
                st.markdown(f"<a href='{row['Liên kết']}' target='_blank' class='sidebar-button'>🚀 {row['Tên ứng dụng']}</a>", unsafe_allow_html=True)
except Exception as e:
    st.sidebar.error(f"🚫 Không thể tải menu: {e}")

# Style
st.markdown("""
    <style>
        .sidebar-button {
            display: block;
            background-color: #66a3ff;
            color: white;
            padding: 10px;
            border-radius: 8px;
            margin: 5px 0;
            font-weight: bold;
            text-decoration: none;
        }
        .sidebar-button:hover {
            background-color: #3385ff;
        }
        .main-button {
            display: inline-block;
            background-color: #66a3ff;
            color: white;
            padding: 20px 30px;
            border-radius: 14px;
            font-weight: bold;
            font-size: 24px;
            margin: 14px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            text-decoration: none;
        }
        .main-button:hover {
            transform: scale(1.07);
            background-color: #3399ff;
        }
    </style>
""", unsafe_allow_html=True)

# Header
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

# Giao diện chính
if st.session_state["view"] == "home":
    st.markdown("""
    <div style="display: flex; justify-content: center; flex-wrap: wrap;">
        <a href="https://terabox.com/s/1cegqu7nP7rd0BdL_MIyrtA" target="_blank" class="main-button">📦 Bigdata_Terabox</a>
        <a href="https://chat.openai.com" target="_blank" class="main-button">💬 ChatGPT công khai</a>
        <a href="https://www.youtube.com/@dienlucdinhhoa" target="_blank" class="main-button">🎬 video tuyên truyền</a>
        <a href="https://www.dropbox.com/home/3.%20Bao%20cao/4.%20B%C3%A1o%20c%C3%A1o%20CMIS" target="_blank" class="main-button">📄 Báo cáo CMIS</a>
        <a href="#" onclick="window.location.search='?ton_that=1'" class="main-button">📊 TỔN THẤT</a>
    </div>
    """, unsafe_allow_html=True)

    if st.query_params.get("ton_that") == ["1"]:
        st.session_state["view"] = "ton_that"
        st.rerun()

# Giao diện tổn thất
elif st.session_state["view"] == "ton_that":
    st.button("🔙 Về trang chính", on_click=lambda: st.session_state.update({"view": "home"}))
    st.markdown("## 📊 PHÂN TÍCH TỔN THẤT TOÀN ĐƠN VỊ")

    col1, col2 = st.columns(2)
    year = col1.selectbox("Chọn năm", list(range(2018, 2026)), index=7)
    max_month = 5 if year == 2025 else 12
    month = col2.selectbox("Chọn tháng", list(range(1, max_month + 1)), index=max_month - 1)

    # Dữ liệu đủ 12 tháng, riêng 2025 chỉ đến tháng 5
    full_months = list(range(1, 13))
    values_now = [round(7.1 + (i % 4) * 0.3 + (year - 2021)*0.05, 2) if i <= max_month else None for i in full_months]
    values_last = [round(7.1 + (i % 3) * 0.2 + (year - 2022)*0.04, 2) for i in full_months]

    df = pd.DataFrame({
        "Tháng": full_months,
        "Tỷ lệ tổn thất": values_now,
        "Cùng kỳ năm trước": values_last
    })

    with st.expander("📈 Biểu đồ tổn thất", expanded=True):
        fig, ax = plt.subplots(figsize=(5, 2))  # nhỏ hơn nữa
        ax.plot(full_months, values_now, marker='o', label=f"Năm {year}")
        ax.plot(full_months, values_last, marker='s', linestyle='-', color='gray', label=f"Năm {year-1}")
        ax.set_xticks(full_months)
        ax.set_xlabel("Tháng")
        ax.set_ylabel("Tỷ lệ tổn thất (%)")
        ax.set_title(f"Tỷ lệ tổn thất năm {year}")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

    st.markdown("### 📊 Bảng dữ liệu tổn thất")
    st.dataframe(df.style.format({"Tỷ lệ tổn thất": "{:.2f}", "Cùng kỳ năm trước": "{:.2f}"}), use_container_width=True)
