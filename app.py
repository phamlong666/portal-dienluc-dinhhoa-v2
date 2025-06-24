
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Báo cáo tổn thất TBA", layout="wide")
st.title("📥 Tải dữ liệu đầu vào - Báo cáo tổn thất")

# === Nút làm mới ===
if st.button("🔄 Làm mới"):
    st.session_state.clear()
    st.experimental_rerun()

with st.expander("🔌 Tổn thất các TBA công cộng"):
    upload_tba_thang = st.file_uploader("📅 Tải dữ liệu TBA công cộng - Theo tháng", type=["xlsx"], key="tba_thang")

    if upload_tba_thang is not None:
        try:
            xls = pd.ExcelFile(upload_tba_thang)
            sheet_names = xls.sheet_names

            sheet_target = None
            for s in sheet_names:
                if s.strip().lower() == "bảng kết quả ánh xạ dữ liệu".lower():
                    sheet_target = s
                    break

            if sheet_target is None:
                st.error(f"❌ Không tìm thấy sheet 'Bảng Kết quả ánh xạ dữ liệu'. Sheet hiện có: {sheet_names}")
            else:
                # Lấy tháng/năm từ dòng đầu tiên của Sheet1
                try:
                    df_info = pd.read_excel(upload_tba_thang, sheet_name="Sheet1", nrows=1, header=None)
                    thong_tin_thang = df_info.iloc[0, 0] if not df_info.empty else ""
                except:
                    thong_tin_thang = ""

                df = xls.parse(sheet_target)

                # Format dữ liệu: giữ 2 số sau dấu phẩy cho tỷ lệ, có . ngăn cách nghìn
                def format_number(x):
                    try:
                        return f"{int(x):,}".replace(",", ".")
                    except:
                        return x

                df["Tỷ lệ tổn thất (%)"] = df["Tỷ lệ tổn thất (%)"].map(lambda x: f"{float(x):.2f}".replace(".", ",") if pd.notna(x) else "")
                if "So sánh (%)" in df.columns:
                    df["So sánh (%)"] = df["So sánh (%)"].map(lambda x: f"{float(x):.2f}".replace(".", ",") if pd.notna(x) else "")
                if "Điện nhận (kWh)" in df.columns:
                    df["Điện nhận (kWh)"] = df["Điện nhận (kWh)"].map(format_number)
                if "Thương phẩm (kWh)" in df.columns:
                    df["Thương phẩm (kWh)"] = df["Thương phẩm (kWh)"].map(format_number)
                if "Điện tổn thất (kWh)" in df.columns:
                    df["Điện tổn thất (kWh)"] = df["Điện tổn thất (kWh)"].map(format_number)

                with st.expander("📋 Xem bảng dữ liệu đã ánh xạ", expanded=False):
                    st.dataframe(df)

                # Phân loại tổn thất
                def phan_loai(x):
                    try:
                        x = float(x)
                    except:
                        return "Không rõ"
                    if x < 2:
                        return "<2%"
                    elif x < 3:
                        return ">=2 và <3%"
                    elif x < 4:
                        return ">=3 và <4%"
                    elif x < 5:
                        return ">=4 và <5%"
                    elif x < 7:
                        return ">=5 và <7%"
                    else:
                        return ">=7%"

                df["Ngưỡng"] = df["Tỷ lệ tổn thất (%)"].apply(phan_loai)
                tong_theo_nguong = df["Ngưỡng"].value_counts().reindex(
                    ["<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%", ">=5 và <7%", ">=7%"],
                    fill_value=0
                )

                colors = {
                    "<2%": "steelblue",
                    ">=2 và <3%": "darkorange",
                    ">=3 và <4%": "forestgreen",
                    ">=4 và <5%": "goldenrod",
                    ">=5 và <7%": "teal",
                    ">=7%": "crimson"
                }

                col1, col2 = st.columns([2, 2])
                with col1:
                    st.markdown(f"#### 📊 Số lượng TBA theo ngưỡng tổn thất {thong_tin_thang}")
                    fig_bar = go.Figure()
                    for nguong, color in colors.items():
                        fig_bar.add_trace(go.Bar(
                            name=nguong,
                            x=["Thực hiện"],
                            y=[tong_theo_nguong[nguong]],
                            marker_color=color,
                            text=[tong_theo_nguong[nguong]],
                            textposition="outside",
                            textfont=dict(size=14, color="black")
                        ))
                    fig_bar.update_layout(
                        barmode='group',
                        xaxis_title="",
                        yaxis_title="Số lượng TBA",
                        height=400,
                        font=dict(color="black", size=14),
                        showlegend=False
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)

                with col2:
                    st.markdown(f"#### 🧩 Tỷ trọng TBA theo ngưỡng tổn thất {thong_tin_thang}")
                    fig_pie = go.Figure(data=[
                        go.Pie(
                            labels=list(colors.keys()),
                            values=[tong_theo_nguong[k] for k in colors.keys()],
                            marker=dict(colors=list(colors.values())),
                            hole=0.5,
                            textinfo='percent+label',
                            textfont=dict(size=14, color="black")
                        )
                    ])
                    fig_pie.update_layout(
                        annotations=[dict(text=f"Tổng số TBA<br><b>{df.shape[0]}</b>", x=0.5, y=0.5, font_size=16, showarrow=False, font_color="black")],
                        height=400,
                        font=dict(color="black", size=14)
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)

        except Exception as e:
            st.error(f"Lỗi khi đọc file: {e}")
