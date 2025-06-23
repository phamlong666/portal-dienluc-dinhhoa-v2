import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
from docx import Document
from docx.shared import Inches
from pptx import Presentation
from pptx.util import Inches as PptInches, Pt

st.set_page_config(page_title="Báo cáo tổn thất TBA", layout="wide")
st.title("📊 Báo cáo tổn thất các TBA công cộng")

# Tải file và lưu tạm
file_keys = ["Theo Tháng", "Lũy kế", "Cùng kỳ"]
uploaded_data = {}

col_uploads = st.columns(3)
for i, key in enumerate(file_keys):
    with col_uploads[i]:
        file = st.file_uploader(f"📁 File {key}", type=["xlsx"], key=f"upload_{key}")
        if file:
            xls = pd.ExcelFile(file)
            sheet_name = [s for s in xls.sheet_names if "ánh xạ" in s.lower()][0]
            df = pd.read_excel(xls, sheet_name=sheet_name)
            uploaded_data[key] = df

# Nút tạo báo cáo
if uploaded_data:
    if st.button("📌 Tạo báo cáo"):

        def export_powerpoint(title, actual, plan):
            prs = Presentation()
            slide = prs.slides.add_slide(prs.slide_layouts[5])
            shapes = slide.shapes
            title_shape = shapes.title
            title_shape.text = title

            txBox = shapes.add_textbox(PptInches(1), PptInches(1.5), PptInches(8), PptInches(5))
            tf = txBox.text_frame
            tf.text = f"Tỷ lệ tổn thất thực tế: {actual:.2f}%"
            p = tf.add_paragraph()
            p.text = f"Tỷ lệ tổn thất kế hoạch: {plan:.2f}%"
            return prs

        for key, df in uploaded_data.items():
            st.subheader(f"🔍 Dữ liệu: {key}")
            df_copy = df.copy()
            percent_cols = [col for col in df_copy.columns if "%" in col]
            for col in percent_cols:
                df_copy[col] = pd.to_numeric(df_copy[col], errors="coerce")
                df_copy[col] = df_copy[col].map(lambda x: f"{x:.2f}%" if pd.notna(x) else "")
            st.dataframe(df_copy.style.set_properties(**{"font-size": "18pt"}), use_container_width=True)

            # Biểu đồ tổn thất
            total_input = df["Điện nhận (kWh)"].sum()
            total_loss = df["Điện tổn thất (kWh)"].sum()
            actual = (total_loss / total_input * 100) if total_input else 0
            plan_col = [c for c in df.columns if "kế hoạch" in c.lower()][0]
            plan_series = df[plan_col]
            plan = ((plan_series / 100 * df["Điện nhận (kWh)"]).sum() / total_input * 100) if total_input else 0

            st.markdown(f"#### 📉 Biểu đồ tổn thất - {key}")
            fig, ax = plt.subplots(figsize=(2.5, 1.8))  # giảm 70%
            x = np.arange(2)
            ax.bar(x, [actual, plan], width=0.4, tick_label=["Thực tế", "Kế hoạch"], color=["#3498DB", "#F4D03F"])
            for i, v in enumerate([actual, plan]):
                ax.text(i, v + 0.2, f"{v:.2f}%", ha="center", fontsize=10)
            ax.set_ylim(0, max(actual, plan) * 1.4 if max(actual, plan) > 0 else 5)
            st.pyplot(fig)

            # Xuất Word
            with io.BytesIO() as doc_bytes:
                doc = Document()
                doc.add_heading(f"Báo cáo tổn thất TBA - {key}", 0)
                doc.add_paragraph(f"Tỷ lệ tổn thất thực tế: {actual:.2f}%")
                doc.add_paragraph(f"Tỷ lệ tổn thất kế hoạch: {plan:.2f}%")
                img_stream = io.BytesIO()
                fig.savefig(img_stream, format="png")
                img_stream.seek(0)
                doc.add_picture(img_stream, width=Inches(4))
                doc.save(doc_bytes)
                st.download_button(f"⬇️ Tải báo cáo Word ({key})", doc_bytes.getvalue(), f"BaoCao_{key}.docx")

            # Xuất PowerPoint
            ppt = export_powerpoint(f"Báo cáo tổn thất TBA - {key}", actual, plan)
            ppt_bytes = io.BytesIO()
            ppt.save(ppt_bytes)
            st.download_button(f"⬇️ Tải báo cáo PowerPoint ({key})", ppt_bytes.getvalue(), f"BaoCao_{key}.pptx")

        # Biểu đồ hợp nhất
        if len(uploaded_data) == 3:
            st.markdown("### 📊 Biểu đồ hợp nhất tổn thất các file")
            data_total = []
            for key in file_keys:
                df = uploaded_data[key]
                total_input = df["Điện nhận (kWh)"].sum()
                total_loss = df["Điện tổn thất (kWh)"].sum()
                actual = (total_loss / total_input * 100) if total_input else 0
                plan_col = [c for c in df.columns if "kế hoạch" in c.lower()][0]
                plan_series = df[plan_col]
                plan = ((plan_series / 100 * df["Điện nhận (kWh)"]).sum() / total_input * 100) if total_input else 0
                data_total.append((key, actual, plan))

            fig2, ax2 = plt.subplots(figsize=(5, 3))
            x = np.arange(3)
            actuals = [d[1] for d in data_total]
            plans = [d[2] for d in data_total]
            ax2.bar(x - 0.2, actuals, width=0.4, label="Thực tế", color="#3498DB")
            ax2.bar(x + 0.2, plans, width=0.4, label="Kế hoạch", color="#F1C40F")
            ax2.set_xticks(x)
            ax2.set_xticklabels(file_keys)
            ax2.legend()
            for i, (a, p) in enumerate(zip(actuals, plans)):
                ax2.text(i - 0.2, a + 0.1, f"{a:.2f}%", ha="center", fontsize=8)
                ax2.text(i + 0.2, p + 0.1, f"{p:.2f}%", ha="center", fontsize=8)
            st.pyplot(fig2)
