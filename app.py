# ============================================
# Mắt Nâu xin phục hồi toàn bộ modul biểu đồ và xuất file PDF cho anh Long
def export_pdf_from_charts(fig_list, filename="bao_cao_ton_that.pdf"):
    from fpdf import FPDF
    import matplotlib.pyplot as plt
    import tempfile
    import os

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Báo cáo tổn thất - Trung tâm điều hành số", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(5)

    for fig in fig_list:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            fig.savefig(tmpfile.name, dpi=150, bbox_inches='tight')
            pdf.image(tmpfile.name, w=160)  # width ~ A4 size - margin
            os.unlink(tmpfile.name)
            pdf.ln(10)

    pdf.output(filename)
    return filename

# ============================================
# Biểu đồ ngưỡng tổn thất

def ve_bieu_do_nguong(df):
    import matplotlib.pyplot as plt
    import seaborn as sns

    nguong_labels = [
        "<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%",
        ">=5 và <7%", ">=7%"
    ]

    df_group = df.groupby(["Ngưỡng tổn thất", "Loại"]).size().unstack().reindex(nguong_labels).fillna(0)
    df_group = df_group.astype(int)

    # Bar chart
    fig, ax = plt.subplots(figsize=(10, 5))
    df_group.plot(kind="bar", ax=ax, color=["lightgray", "#0072B2"])
    ax.set_title("Số lượng TBA theo ngưỡng tổn thất", fontsize=14)
    ax.set_ylabel("Số lượng")
    ax.set_xlabel("")
    ax.legend(title="Loại")
    plt.xticks(rotation=0)
    plt.tight_layout()

    return fig

# ============================================
# Biểu đồ tròn tỷ trọng

def ve_bieu_do_ti_trong(df):
    import matplotlib.pyplot as plt

    df_ratio = df["Ngưỡng tổn thất"].value_counts().reindex([
        "<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%",
        ">=5 và <7%", ">=7%"
    ]).fillna(0)

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d4aa00", "#17becf", "#d62728"]

    fig, ax = plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = ax.pie(
        df_ratio,
        labels=df_ratio.index,
        colors=colors,
        autopct='%1.2f%%',
        startangle=90,
        textprops={'fontsize': 10}
    )
    ax.set_title("Tỷ trọng TBA theo ngưỡng tổn thất", fontsize=13)
    plt.tight_layout()
    return fig

# ============================================
# Biểu đồ hợp nhất so sánh

def ve_bieu_do_hop_nhat(df):
    import matplotlib.pyplot as plt
    import seaborn as sns

    df_count = df.groupby(["Ngưỡng tổn thất", "Loại"]).size().unstack().fillna(0)
    df_ratio = df["Ngưỡng tổn thất"].value_counts().sort_index()
    nguong_labels = [
        "<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%",
        ">=5 và <7%", ">=7%"
    ]

    fig, ax1 = plt.subplots(figsize=(10, 5))

    df_count = df_count.reindex(nguong_labels)
    df_count.plot(kind="bar", ax=ax1, position=0, width=0.4, color=["gray", "orange"], legend=False)
    ax1.set_ylabel("Số TBA")
    ax1.set_xlabel("")
    ax1.set_title("So sánh ngưỡng tổn thất (Số TBA - Tỷ trọng)")
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()
    ax2.plot(df_ratio.index, df_ratio.values / df_ratio.values.sum(), 'o--', color='blue')
    ax2.set_ylabel("Tỷ trọng")
    ax2.tick_params(axis='y')

    fig.tight_layout()
    return fig
