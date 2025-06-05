
import matplotlib.pyplot as plt
import pandas as pd

# Tạo menu chính
selected_menu = st.sidebar.radio("📂 Menu chức năng", ["🏠 Trang chính", "📊 TỔN THẤT"])

if selected_menu == "🏠 Trang chính":
    st.title("🏠 Trung tâm điều hành số - Điện lực Định Hóa")
    # Các nút chính khác giữ nguyên tại đây
    st.markdown("### Chào mừng bạn đến với hệ thống điều hành số")

elif selected_menu == "📊 TỔN THẤT":
    st.title("📊 Phân tích tổn thất điện năng")
    sub_tab = st.radio("Chọn phân tích", ["Tổn thất toàn đơn vị", "Tổn thất trung áp", "Tổn thất hạ áp"])

    if sub_tab == "Tổn thất toàn đơn vị":
        st.subheader("📈 Biểu đồ tổn thất toàn đơn vị")
        sheet_url = "https://docs.google.com/spreadsheets/d/13MqQzvV3Mf9bLOAXwICXclYVQ-8WnvBDPAR8VJfOGJg/export?format=csv&id=13MqQzvV3Mf9bLOAXwICXclYVQ-8WnvBDPAR8VJfOGJg&gid=2115988437"
        df = pd.read_csv(sheet_url)
        df = df.rename(columns={df.columns[0]: "Năm"})
        years = df["Năm"].dropna().unique()
        selected_year = st.selectbox("Chọn năm", sorted(years, reverse=True))
        df_selected = df[df["Năm"] == selected_year].reset_index(drop=True)
        df_selected = df_selected.drop(columns=["Năm"], errors="ignore")
        months = list(range(1, len(df_selected.columns) + 1))

        fig, ax = plt.subplots()
        for idx in range(1, 6):
            if idx < len(df_selected):
                ax.plot(months, df_selected.iloc[idx], label=f"Dòng {idx+1}", marker="o")

        ax.set_xticks(months)
        ax.set_xticklabels([f"Tháng {m}" for m in months])
        ax.set_title(f"Tổn thất toàn đơn vị - Năm {selected_year}")
        ax.set_xlabel("Tháng")
        ax.set_ylabel("Giá trị")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    elif sub_tab == "Tổn thất trung áp":
        st.info("🔧 Đang cập nhật: Phân tích tổn thất trung áp")

    elif sub_tab == "Tổn thất hạ áp":
        st.info("🔧 Đang cập nhật: Phân tích tổn thất hạ áp")



import streamlit as st
import pandas as pd
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
            background-color: #42A5F5;
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
            background-color: #1E88E5 !important;
            transform: translateY(-2px);
            box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
        }

        .main-button {
            display: inline-block;
            background-color: #FFCC80;
            color: white;
            text-align: center;
            padding: 22px 30px;
            border-radius: 14px;
            font-weight: bold;
            text-decoration: none;
            margin: 14px;
            transition: 0.3s;
            font-size: 24px;
        }

        .main-button:hover {
            transform: scale(1.05);
            box-shadow: 3px 3px 12px rgba(0,0,0,0.3);
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
👋 Chào mừng anh Long đến với Trung tâm điều hành số - phần mềm Điện lực Định Hóa

📌 **Các tính năng nổi bật:**
- Phân tích thất bại, báo cáo kỹ thuật
- Lưu trữ và truy xuất lịch sử GPT
- Truy cập hệ thống nhanh chóng qua Sidebar

✅ Mọi bản cập nhật chỉ cần chỉnh sửa Google Sheet đều tự động hiển thị!
""")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="display: flex; justify-content: center; flex-wrap: wrap;">
    <a href="https://terabox.com/s/1cegqu7nP7rd0BdL_MIyrtA" target="_blank" class="main-button">📦 Bigdata_Terabox</a>
    <a href="https://chat.openai.com/c/2d132e26-7b53-46b3-bbd3-8a5229e77973" target="_blank" class="main-button">🤖 AI. PHẠM HỒNG LONG</a>
    <a href="https://www.youtube.com" target="_blank" class="main-button">🎬 video tuyên truyền</a>
    <a href="https://www.dropbox.com/scl/fo/yppcs3fy1sxrilyzjbvxa/APan4-c_N5NwbIDtTzUiuKo?dl=0" target="_blank" class="main-button">📄 Báo cáo CMIS</a>
</div>
""", unsafe_allow_html=True)
