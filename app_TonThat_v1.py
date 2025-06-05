
import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Cổng điều hành số - phần mềm Điện lực Định Hóa", layout="wide")

# --- SESSION STATE ---
if "page" not in st.session_state:
    st.session_state["page"] = "home"

def go_home():
    st.session_state["page"] = "home"

def go_ton_that():
    st.session_state["page"] = "ton_that"

# --- SIDEBAR ---
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] > div:first-child {
            max-height: 95vh;
            overflow-y: auto;
        }
        .main-button {
            display: inline-block;
            background-color: #90CAF9;
            color: black;
            padding: 16px 24px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 12px;
            margin: 10px;
            box-shadow: 3px 3px 6px rgba(0,0,0,0.2);
            text-align: center;
        }
        .main-button:hover {
            background-color: #42A5F5;
            color: white;
            transform: scale(1.05);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- MAIN UI ---
if st.session_state["page"] == "home":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="main-button">📊 TỔN THẤT</div>', unsafe_allow_html=True)
        if st.button("👉 Vào phân tích Tổn thất", key="btn_ton_that"):
            go_ton_that()
    with col2:
        st.markdown('<div class="main-button">📈 BIGDATA</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="main-button">🤖 TRỢ LÝ</div>', unsafe_allow_html=True)

elif st.session_state["page"] == "ton_that":
    st.title("📊 PHÂN TÍCH TỔN THẤT")
    st.markdown("Chọn loại tổn thất bạn muốn xem:")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.button("Tổn thất toàn đơn vị")
    with c2:
        st.button("Tổn thất trung áp")
    with c3:
        st.button("Tổn thất hạ áp")
    st.button("🔙 Quay về trang chính", on_click=go_home)
