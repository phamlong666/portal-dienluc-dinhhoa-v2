
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
from docx import Document
from docx.shared import Inches

st.set_page_config(page_title="Báo cáo tổn thất TBA", layout="wide")
st.title("📊 Báo cáo tổn thất các TBA công cộng")

def read_mapping_sheet(uploaded_file):
    try:
        xls = pd.ExcelFile(uploaded_file)
        sheet_name = [s for s in xls.sheet_names if "ánh xạ" in s.lower()][0]
        df = pd.read_excel(xls, sheet_name=sheet_name)

        for col in df.columns:
            if df[col].dtype in [np.float64, np.int64]:
                df[col] = df[col].round(0).astype("Int64")

        percent_cols = [col for col in df.columns if "%" in col]
        for col in percent_cols:
            df[col] = pd.to_numeric(
                df[col].astype(str)
                .str.replace("%", "", regex=False)
                .str.replace(",", ".", regex=False)
                .replace("", np.nan),
                errors="coerce",
            )
        return df
    except Exception as e:
        st.warning(f"Lỗi khi đọc file {uploaded_file.name}: {e}")
        return None

def calc_overall_rate(df):
    try:
        total_input = df["Điện nhận (kWh)"].sum()
        total_loss = df["Điện tổn thất (kWh)"].sum()
        actual_rate = (total_loss / total_input * 100) if total_input else 0.0
        plan_col = [col for col in df.columns if "kế hoạch" in col.lower()][0]
        plan_series = df[plan_col]
        plan_rate = (
            ((plan_series / 100) * df["Điện nhận (kWh)"]).sum() / total_input * 100
            if total_input
            else 0.0
        )
        return round(actual_rate, 2), round(plan_rate, 2)
    except:
        return 0.0, 0.0

col_uploads = st.columns(3)
with col_uploads[0]:
    file_thang = st.file_uploader("📅 File Theo Tháng", type=["xlsx"], key="tba_thang")
with col_uploads[1]:
    file_luyke = st.file_uploader("📊 File Lũy kế", type=["xlsx"], key="tba_luyke")
with col_uploads[2]:
    file_cungky = st.file_uploader("📈 File Cùng kỳ", type=["xlsx"], key="tba_ck")

uploaded_files = {
    "Theo Tháng": file_thang,
    "Lũy kế": file_luyke,
    "Cùng kỳ": file_cungky,
}

for label, file in uploaded_files.items():
    if file:
        df = read_mapping_sheet(file)
        if df is not None:
            st.markdown(f"### 📄 Bảng dữ liệu: {label}")
            with st.expander(f"📌 Xem bảng {label}", expanded=False):
                percent_cols = [col for col in df.columns if "%" in col]
                for col in percent_cols:
                    df[col] = df[col].map(lambda x: f"{x:.2f}".replace(".", ",") + "%" if pd.notna(x) else "")
                st.dataframe(df.style.set_properties(**{'font-size': '24pt'}), use_container_width=True)

            act, plan = calc_overall_rate(df)

            st.markdown(f"#### 📉 Biểu đồ tổn thất - {label}")
            fig, ax = plt.subplots(figsize=(1.5, 0.9))
            x = np.arange(2)
            ax.bar(x, [act, plan], width=0.4, tick_label=["Thực tế", "Kế hoạch"])
            for i, v in enumerate([act, plan]):
                ax.text(i, v + 0.2, f"{v:.2f}".replace(".", ",") + "%", ha="center", fontsize=8)
            ax.set_ylim(0, max(act, plan) * 1.5 if max(act, plan) > 0 else 5)
            st.pyplot(fig)

            # Tạo báo cáo Word
            doc = Document()
            doc.add_heading(f"Báo cáo tổn thất TBA - {label}", 0)
            doc.add_paragraph(f"Tỷ lệ tổn thất thực tế: {act:.2f}%")
            doc.add_paragraph(f"Tỷ lệ tổn thất kế hoạch: {plan:.2f}%")
            chart_stream = io.BytesIO()
            fig.savefig(chart_stream, format="png")
            chart_stream.seek(0)
            doc.add_picture(chart_stream, width=Inches(4))

            word_bytes = io.BytesIO()
            doc.save(word_bytes)
            st.download_button(
                label=f"⬇️ Tải báo cáo Word ({label})",
                data=word_bytes.getvalue(),
                file_name=f"BaoCao_{label}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import io

st.set_page_config(page_title="Tổn thất điện năng - EVNNPC", layout="wide")

# ====================== FUNCTION =======================
def load_data(uploaded_files):
    dfs = []
    for file in uploaded_files:
        df = pd.read_excel(file)
        dfs.append(df)
    return dfs

def draw_combined_chart(dfs, titles):
    fig, ax = plt.subplots(figsize=(8, 4))
    width = 0.25
    x = range(len(titles))

    for i, df in enumerate(dfs):
        try:
            values = [
                float(df[df['Chỉ tiêu'] == 'Tỷ lệ tổn thất theo tháng']['Giá trị'].values[0]),
                float(df[df['Chỉ tiêu'] == 'Tỷ lệ tổn thất lũy kế']['Giá trị'].values[0]),
                float(df[df['Chỉ tiêu'] == 'Tỷ lệ tổn thất cùng kỳ']['Giá trị'].values[0]),
            ]
            ax.bar([p + width * i for p in x], values, width=width, label=f"File {i+1}")
        except:
            continue

    ax.set_xticks([p + width for p in x])
    ax.set_xticklabels(titles)
    ax.set_ylabel("Tỷ lệ tổn thất")
    ax.set_title("So sánh tổn thất điện")
    ax.legend()
    st.pyplot(fig)
    return fig

def export_pdf(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="BÁO CÁO TỔN THẤT ĐIỆN NĂM 2025", ln=True, align="C")
    pdf.image(buf, x=10, y=30, w=180)
    pdf.output("bao_cao_ton_that.pdf")
    st.success("✅ Đã tạo file bao_cao_ton_that.pdf")

# ====================== APP =========================
# Đã xoá nội dung Phân tích tổn thất điện năng - Điện lực Định Hóa

uploaded_files = st.file_uploader("Tải lên 1 đến 3 file tổn thất", type=["xlsx"], accept_multiple_files=True)

if uploaded_files:
    dfs = load_data(uploaded_files)
    titles = ['Theo Tháng', 'Lũy kế', 'Cùng kỳ']
    st.subheader("🔍 Biểu đồ so sánh tổn thất")
    fig = draw_combined_chart(dfs, titles)

    st.subheader("⬇️ Xuất báo cáo")
    if st.button("Tải báo cáo PDF"):
        export_pdf(fig)




# ========== PHÂN TÍCH TỔNG HỢP TỔN THẤT 3 FILE ==========
import matplotlib.pyplot as plt
from pptx import Presentation
from pptx.util import Inches
from fpdf import FPDF
import io

def create_combined_chart(data_dict):
    fig, ax = plt.subplots(figsize=(6, 3))
    width = 0.25
    labels = ["Thực tế", "Kế hoạch"]
    x = range(len(labels))

    for idx, (label, (act, plan)) in enumerate(data_dict.items()):
        ax.bar([i + idx * width for i in x], [act, plan], width=width, label=label)

    ax.set_xticks([i + width for i in x])
    ax.set_xticklabels(labels)
    ax.set_ylabel("Tỷ lệ tổn thất (%)")
    ax.set_title("So sánh tổn thất các báo cáo")
    ax.legend()
    fig.tight_layout()
    return fig

def export_pdf_ascii_title(image_path, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="BAO CAO TON THAT TONG HOP", ln=True, align="C")
    pdf.image(image_path, x=10, y=30, w=180)
    output_path = f"/mnt/data/{filename}.pdf"
    pdf.output(output_path)
    return output_path

def export_pptx_from_file(image_path, filename):
    prs = Presentation()
    slide_layout = prs.slide_layouts[5]
    slide = prs.slides.add_slide(slide_layout)
    left = Inches(1)
    top = Inches(1.5)
    slide.shapes.add_picture(image_path, left, top, width=Inches(8))
    output_path = f"/mnt/data/{filename}.pptx"
    prs.save(output_path)
    return output_path

# ======= Giao diện phân tích tổn thất tổng hợp =======
st.markdown("## 📊 Tổng hợp tổn thất từ 3 file")
file1 = st.file_uploader("📥 File Theo Tháng", type=["xlsx"], key="file1")
file2 = st.file_uploader("📥 File Lũy kế", type=["xlsx"], key="file2")
file3 = st.file_uploader("📥 File Cùng kỳ", type=["xlsx"], key="file3")

uploaded_files_combo = {
    "Theo Tháng": file1,
    "Lũy kế": file2,
    "Cùng kỳ": file3
}

def read_mapping_sheet(uploaded_file):
    try:
        xls = pd.ExcelFile(uploaded_file)
        sheet_name = [s for s in xls.sheet_names if "ánh xạ" in s.lower()][0]
        df = pd.read_excel(xls, sheet_name=sheet_name)

        for col in df.columns:
            if df[col].dtype in [np.float64, np.int64]:
                df[col] = df[col].round(0).astype("Int64")

        percent_cols = [col for col in df.columns if "%" in col]
        for col in percent_cols:
            df[col] = pd.to_numeric(
                df[col].astype(str)
                .str.replace("%", "", regex=False)
                .str.replace(",", ".", regex=False)
                .replace("", np.nan),
                errors="coerce",
            )
        return df
    except Exception as e:
        st.warning(f"Lỗi khi đọc file {uploaded_file.name}: {e}")
        return None

def calc_overall_rate(df):
    try:
        total_input = df["Điện nhận (kWh)"].sum()
        total_loss = df["Điện tổn thất (kWh)"].sum()
        actual_rate = (total_loss / total_input * 100) if total_input else 0.0
        plan_col = [col for col in df.columns if "kế hoạch" in col.lower()][0]
        plan_series = df[plan_col]
        plan_rate = (
            ((plan_series / 100) * df["Điện nhận (kWh)"]).sum() / total_input * 100
            if total_input
            else 0.0
        )
        return round(actual_rate, 2), round(plan_rate, 2)
    except:
        return 0.0, 0.0

result_dict = {}
for name, file in uploaded_files_combo.items():
    if file:
        df = read_mapping_sheet(file)
        if df is not None:
            act, plan = calc_overall_rate(df)
            result_dict[name] = (act, plan)

if result_dict:
    st.success("✅ Đã xử lý xong dữ liệu tổn thất từ các file.")
    fig = create_combined_chart(result_dict)
    image_path = "/mnt/data/bieu_do_ton_that_tong_hop.png"
    fig.savefig(image_path)
    st.image(image_path, caption="Biểu đồ tổn thất tổng hợp", use_column_width=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬇️ Xuất PDF"):
            export_pdf_ascii_title(image_path, "bao_cao_ton_that_thuc_te")
            st.success("✅ Đã xuất file PDF")
            st.markdown("[📄 Tải PDF](sandbox:/mnt/data/bao_cao_ton_that_thuc_te.pdf)")
    with col2:
        if st.button("⬇️ Xuất PowerPoint"):
            export_pptx_from_file(image_path, "bao_cao_ton_that_thuc_te")
            st.success("✅ Đã xuất file PowerPoint")
            st.markdown("[📊 Tải PPTX](sandbox:/mnt/data/bao_cao_ton_that_thuc_te.pptx)")
