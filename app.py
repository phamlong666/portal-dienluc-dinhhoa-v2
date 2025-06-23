import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
from docx import Document
from docx.shared import Inches
from pptx import Presentation
from pptx.util import Inches as PPT_Inches
from fpdf import FPDF

st.set_page_config(page_title="Báo cáo tổn thất TBA", layout="wide")

st.title("📥 Tải dữ liệu đầu vào - Báo cáo tổn thất")
st.markdown("### 🔍 Chọn loại dữ liệu tổn thất để tải lên:")
with st.expander("🔌 Tổn thất các TBA công cộng"):
    file_thang = st.file_uploader("📅 Tải dữ liệu TBA công cộng - Theo tháng", type=["xlsx"], key="tba_thang")
    file_luyke = st.file_uploader("📊 Tải dữ liệu TBA công cộng - Lũy kế", type=["xlsx"], key="tba_luyke")
    file_cungky = st.file_uploader("📈 Tải dữ liệu TBA công cộng - Cùng kỳ", type=["xlsx"], key="tba_ck")

def read_mapping_sheet(uploaded_file):
    xls = pd.ExcelFile(uploaded_file)
    sheet_name = None
    for name in xls.sheet_names:
        if name.strip().lower() == "bảng kết quả ánh xạ dữ liệu".lower():
            sheet_name = name
            break
    if sheet_name is None:
        st.error(f"❌ Không tìm thấy sheet 'Bảng Kết quả ánh xạ dữ liệu' trong file {uploaded_file.name}")
        return None
    df = pd.read_excel(xls, sheet_name=sheet_name)
    # Đảm bảo các cột số dạng Int (loại Int64 để giữ giá trị trống nếu có)
    num_cols = ["Công suất (KVA)", "Số KH", "Điện nhận (kWh)", "Điện thương phẩm (kWh)", "Điện tổn thất (kWh)"]
    for col in num_cols:
        if col in df.columns:
            df[col] = df[col].round(0).astype("Int64")
    return df

if file_thang and file_luyke and file_cungky:
    df_thang = read_mapping_sheet(file_thang)
    df_luyke = read_mapping_sheet(file_luyke)
    df_cungky = read_mapping_sheet(file_cungky)
    if df_thang is not None and df_luyke is not None and df_cungky is not None:
        # Định dạng các cột % (2 decimal, dấu phẩy, thêm %)
        format_percent = lambda x: (f"{x:.2f}".replace('.', ',') + '%') if pd.notna(x) else ""
        percent_cols = ["Tỷ lệ tổn thất (%)", "Kế hoạch (%)", "So sánh (%)"]
        for df in [df_thang, df_luyke, df_cungky]:
            for col in percent_cols:
                if col in df.columns:
                    # Chuyển chuỗi "x,xx%" về số float trước khi định dạng lại, nếu đã định dạng sẵn
                    if isinstance(df[col].iloc[0], str):
                        df[col] = df[col].str.replace('%','').str.replace(',','.').astype(float)
                    df[col] = df[col].map(format_percent)

        st.markdown("### 📊 Bảng Kết quả ánh xạ dữ liệu:")
        with st.expander("Dữ liệu TBA công cộng - Theo Tháng", expanded=False):
            st.dataframe(df_thang, use_container_width=True)
        with st.expander("Dữ liệu TBA công cộng - Lũy kế", expanded=False):
            st.dataframe(df_luyke, use_container_width=True)
        with st.expander("Dữ liệu TBA công cộng - Cùng kỳ", expanded=False):
            st.dataframe(df_cungky, use_container_width=True)

        # Tính tỷ lệ tổn thất thực tế và kế hoạch cho từng kỳ
        def calc_overall_rate(df):
            total_input = df["Điện nhận (kWh)"].sum()
            total_loss = df["Điện tổn thất (kWh)"].sum()
            actual_rate = (total_loss / total_input * 100) if total_input else 0.0
            plan_rate = 0.0
            if total_input:
                # Chuyển giá trị kế hoạch (%) về số để tính trung bình gia quyền
                plan_series = df["Kế hoạch (%)"]
                if isinstance(plan_series.iloc[0], str):
                    plan_series = plan_series.str.replace('%','').str.replace(',','.').astype(float)
                plan_rate = ((plan_series/100) * df["Điện nhận (kWh)"]).sum() / total_input * 100
            return actual_rate, plan_rate

        act_thang, plan_thang = calc_overall_rate(df_thang)
        act_luyke, plan_luyke = calc_overall_rate(df_luyke)
        act_cungky, plan_cungky = calc_overall_rate(df_cungky)

        # Vẽ biểu đồ cột (Thực tế vs Kế hoạch cho Tháng, Lũy kế, Cùng kỳ)
        categories = ["Tháng", "Lũy kế", "Cùng kỳ"]
        actuals = [act_thang, act_luyke, act_cungky]
        plans   = [plan_thang, plan_luyke, plan_cungky]
        fig_bar, ax = plt.subplots(figsize=(4,3))
        x = np.arange(len(categories))
        width = 0.35
        bars1 = ax.bar(x - width/2, actuals, width, label="Thực tế")
        bars2 = ax.bar(x + width/2, plans,  width, label="Kế hoạch")
        ax.set_xticks(x); ax.set_xticklabels(categories)
        ax.set_ylabel("Tỷ lệ tổn thất (%)")
        ax.set_title("So sánh Tỷ lệ tổn thất Thực tế vs Kế hoạch")
        ax.legend()
        # Gắn nhãn giá trị trên cột
        for bar in bars1:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.1,
                    f"{h:.2f}".replace('.', ',') + '%',
                    ha='center', va='bottom', fontsize=8)
        for bar in bars2:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.1,
                    f"{h:.2f}".replace('.', ',') + '%',
                    ha='center', va='bottom', fontsize=8)

        # Vẽ biểu đồ tròn (tỷ trọng điện thương phẩm vs tổn thất cho Lũy kế)
        labels = ["Điện thương phẩm", "Điện tổn thất"]
        values = [df_luyke["Điện thương phẩm (kWh)"].sum(), df_luyke["Điện tổn thất (kWh)"].sum()]
        fig_pie, ax2 = plt.subplots(figsize=(3,3))
        def autopct_format(pct):
            return f"{pct:.2f}".replace('.', ',') + '%'
        ax2.pie(values, autopct=autopct_format, startangle=90, colors=["#4E79A7", "#F28E2B"])
        ax2.axis('equal')
        ax2.set_title("Tỷ trọng Điện thương phẩm vs Tổn thất (Lũy kế)")
        formatted_vals = [format(val, ",").replace(",", ".") for val in values]
        legend_texts = [f"{labels[i]}: {formatted_vals[i]} kWh" for i in range(len(labels))]
        ax2.legend(legend_texts, loc="best")

        st.markdown("### 📉 Biểu đồ minh họa kết quả:")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.pyplot(fig_bar)
        with col2:
            st.pyplot(fig_pie)

        # Tạo file báo cáo Word, PDF, PPT
        doc = Document()
        doc.add_heading("Báo cáo tổn thất TBA công cộng", 0)
        doc.add_paragraph(f"Tỷ lệ tổn thất lũy kế: {act_luyke:.2f}% (Kế hoạch: {plan_luyke:.2f}%)".replace('.', ','))
        doc.add_paragraph("Biểu đồ so sánh tỷ lệ tổn thất:")
        img_bar = io.BytesIO(); fig_bar.savefig(img_bar, format='png'); img_bar.seek(0)
        doc.add_picture(img_bar, width=Inches(4))
        doc.add_paragraph("Biểu đồ tỷ trọng điện thương phẩm vs tổn thất:")
        img_pie = io.BytesIO(); fig_pie.savefig(img_pie, format='png'); img_pie.seek(0)
        doc.add_picture(img_pie, width=Inches(4))
        doc_buffer = io.BytesIO(); doc.save(doc_buffer)
        doc_bytes = doc_buffer.getvalue()

        prs = Presentation()
        slide_layout = prs.slide_layouts[5]
        slide = prs.slides.add_slide(slide_layout)
        title_shape = slide.shapes.title or slide.shapes.add_textbox(PPT_Inches(0.5), PPT_Inches(0.5), PPT_Inches(9), PPT_Inches(1)).text_frame
        title_shape.text = "Báo cáo tổn thất TBA công cộng"
        slide.shapes.add_picture(img_bar, PPT_Inches(0.5), PPT_Inches(1.5), width=PPT_Inches(4))
        slide.shapes.add_picture(img_pie, PPT_Inches(5.5), PPT_Inches(1.5), width=PPT_Inches(4))
        prs_buffer = io.BytesIO(); prs.save(prs_buffer)
        ppt_bytes = prs_buffer.getvalue()

        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
        pdf.set_font('DejaVu', size=12)
        pdf.cell(0, 10, "Báo cáo tổn thất TBA công cộng", ln=1, align="C")
        pdf.cell(0, 10, f"Tỷ lệ tổn thất lũy kế: {act_luyke:.2f}% (Kế hoạch: {plan_luyke:.2f}%)".replace('.', ','), ln=1)
        img_bar.seek(0); img_pie.seek(0)
        with open("chart_bar.png", "wb") as f: f.write(img_bar.getvalue())
        with open("chart_pie.png", "wb") as f: f.write(img_pie.getvalue())
        pdf.image("chart_bar.png", x=10, y=50, w=90)
        pdf.image("chart_pie.png", x=110, y=50, w=90)
        pdf_bytes = pdf.output(dest='S').encode('latin-1')

        st.download_button("⬇️ Tải báo cáo (Word)", data=doc_bytes, file_name="BaoCao_TBA.docx",
                           mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        st.download_button("⬇️ Tải báo cáo (PDF)", data=pdf_bytes, file_name="BaoCao_TBA.pdf", mime="application/pdf")
        st.download_button("⬇️ Tải báo cáo (PowerPoint)", data=ppt_bytes, file_name="BaoCao_TBA.pptx",
                           mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")
else:
    st.info("Hãy tải lên đầy đủ 3 file dữ liệu (Tháng, Lũy kế, Cùng kỳ) để xem kết quả.")
