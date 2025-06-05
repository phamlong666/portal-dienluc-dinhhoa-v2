
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Trung tâm điều hành số", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.title("📊 Trung tâm điều hành số")
    menu = st.radio("Chọn chức năng:", ["Trang chính", "Tổn thất"])

# --- Trang chính ---
if menu == "Trang chính":
    st.title("🖥️ Trang chính - EVNNPC Điện lực Định Hóa")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("📈 BIGDATA", use_container_width=True)
    with col2:
        st.button("🤖 Trợ lý AI", use_container_width=True)
    with col3:
        st.button("📊 TỔN THẤT", use_container_width=True)

# --- Tổn thất ---
elif menu == "Tổn thất":
    st.title("📊 Phân tích tổn thất điện năng")

    tab1, tab2, tab3 = st.tabs(["Toàn đơn vị", "Trung áp", "Hạ áp"])

    # ========== TOÀN ĐƠN VỊ ==========
    with tab1:
        st.subheader("Tổn thất toàn đơn vị")

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
                ax.plot(months, df_selected.iloc[idx], label=df_selected.iloc[idx - 1, 0], marker="o")

        ax.set_xticks(months)
        ax.set_xticklabels([f"Tháng {m}" for m in months])
        ax.set_title(f"Biểu đồ tổn thất toàn đơn vị năm {selected_year}")
        ax.set_xlabel("Tháng")
        ax.set_ylabel("Giá trị")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    # ========== TRUNG ÁP ==========
    with tab2:
        st.subheader("Tổn thất trung áp")
        st.info("Chức năng đang được cập nhật. Sẽ lấy dữ liệu từ sheet 'Tổn thất trung-hạ áp'.")

    # ========== HẠ ÁP ==========
    with tab3:
        st.subheader("Tổn thất hạ áp")
        st.info("Chức năng đang được cập nhật. Sẽ lấy dữ liệu từ sheet 'Tổn thất trung-hạ áp'.")
