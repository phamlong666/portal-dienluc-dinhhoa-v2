
import streamlit as st
from modules import nhac_viec, phuc_vu_hop

st.set_page_config(page_title="Trung tâm điều hành số - EVNNPC Định Hóa", layout="wide")

st.title("🏠 Trung tâm điều hành số - EVNNPC Định Hóa")
st.markdown("### Chào mừng anh Long!")

tab = st.sidebar.radio("🔘 Chọn chức năng", ["⏰ Nhắc việc", "📑 Phục vụ họp"])

if tab == "⏰ Nhắc việc":
    nhac_viec.run()

elif tab == "📑 Phục vụ họp":
    phuc_vu_hop.run()
