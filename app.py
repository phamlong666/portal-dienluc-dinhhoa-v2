import matplotlib.pyplot as plt
import numpy as np

def ve_bieu_do_ton_that(counts_thuchien, counts_cungkỳ=None):
    labels = ["<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%", ">=5 và <7%", ">=7%"]
    colors_bar = ["#2f69bf", "#f28e2b", "#bab0ac", "#59a14f", "#e6b000", "#d62728"]

    if counts_cungkỳ is None:
        counts_cungkỳ = [0] * len(labels)

    fig, (ax_bar, ax_pie) = plt.subplots(1, 2, figsize=(14, 6), width_ratios=[2, 1])

    x = np.arange(len(labels))
    width = 0.35
    bars1 = ax_bar.bar(x - width / 2, counts_thuchien, width=width, color=colors_bar, label="Thực hiện")
    bars2 = ax_bar.bar(x + width / 2, counts_cungkỳ, width=width, color="#d3d3d3", label="Cùng kỳ")

    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax_bar.text(bar.get_x() + bar.get_width() / 2, height + 1, str(int(height)),
                            ha='center', va='bottom', fontsize=9, fontweight='bold', color='black')

    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(labels, fontsize=10, fontweight='bold')
    ax_bar.set_ylabel("Số lượng", fontsize=11)
    ax_bar.set_title("Số lượng TBA theo ngưỡng tổn thất", fontsize=12, fontweight='bold')
    ax_bar.legend(fontsize=9)

    total = sum(counts_thuchien)
    wedges, texts, autotexts = ax_pie.pie(
        counts_thuchien,
        labels=None,
        autopct=lambda p: f'{p:.2f}%' if p > 0 else '',
        startangle=90,
        colors=colors_bar,
        wedgeprops={'width': 0.3}
    )
    for autotext in autotexts:
        autotext.set_fontweight('bold')
        autotext.set_color('black')
        autotext.set_fontsize(9)
    ax_pie.text(0, 0, f"Tổng số TBA\n{total}", ha='center', va='center', fontsize=11, fontweight='bold')
    ax_pie.set_title("Tỷ trọng TBA theo ngưỡng tổn thất", fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.show()

# Demo chạy thử
if __name__ == "__main__":
    counts_thuchien = [12, 12, 29, 42, 76, 32]
    counts_cungkỳ = [0, 0, 0, 0, 0, 0]
    ve_bieu_do_ton_that(counts_thuchien, counts_cungkỳ)
