import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os # Import os module to handle file paths

st.set_page_config(page_title="Báo cáo tổn thất TBA", layout="wide")
st.title("📥 AI_Trợ lý tổn thất")

st.markdown("### 🔍 Chọn loại dữ liệu tổn thất để tải lên:")

# --- Khởi tạo Session State cho dữ liệu tải lên ---
if 'df_tba_thang' not in st.session_state:
    st.session_state.df_tba_thang = None
if 'df_tba_luyke' not in st.session_state:
    st.session_state.df_tba_luyke = None
if 'df_tba_ck' not in st.session_state:
    st.session_state.df_tba_ck = None
if 'df_ha_thang' not in st.session_state:
    st.session_state.df_ha_thang = None
if 'df_ha_luyke' not in st.session_state:
    st.session_state.df_ha_luyke = None
if 'df_ha_ck' not in st.session_state:
    st.session_state.df_ha_ck = None
if 'df_trung_thang_tt' not in st.session_state:
    st.session_state.df_trung_thang_tt = None
if 'df_trung_luyke_tt' not in st.session_state:
    st.session_state.df_trung_ck_tt = None # This also seems like a typo, should be df_trung_luyke_tt
if 'df_trung_thang_dy' not in st.session_state:
    st.session_state.df_trung_thang_dy = None
if 'df_trung_luyke_dy' not in st.session_state:
    st.session_state.df_trung_luyke_dy = None
if 'df_trung_ck_dy' not in st.session_state:
    st.session_state.df_trung_ck_dy = None
if 'df_dv_thang' not in st.session_state:
    st.session_state.df_dv_thang = None
if 'df_dv_luyke' not in st.session_state:
    st.session_state.df_dv_luyke = None
if 'df_dv_ck' not in st.session_state:
    st.session_state.df_dv_ck = None


# Hàm phân loại tổn thất theo ngưỡng
def phan_loai_nghiem(x):
    try:
        x = float(str(x).replace(",", "."))
    except (ValueError, AttributeError):
        return "Không rõ"
    if x < 2:
        return "<2%"
    elif 2 <= x < 3:
        return ">=2 và <3%"
    elif 3 <= x < 4:
        return ">=3 và <4%"
    elif 4 <= x < 5:
        return ">=4 và <5%"
    elif 5 <= x < 7:
        return ">=5 và <7%"
    else:
        return ">=7%"

# Hàm xử lý DataFrame và trả về số lượng TBA theo ngưỡng
def process_tba_data(df):
    if df is None:
        return None, None
    df_temp = pd.DataFrame()

    # Ưu tiên tìm cột 'Tỷ lệ tổn thất' theo tên
    # Nếu không tìm thấy, thử 'Tỷ lệ tổn thất (%)' (ví dụ từ file mẫu)
    # Nếu vẫn không tìm thấy, kiểm tra chỉ số cột 14 như fallback cuối cùng
    loss_rate_col_found = False
    if 'Tỷ lệ tổn thất' in df.columns:
        df_temp["Tỷ lệ tổn thất"] = df['Tỷ lệ tổn thất'].map(lambda x: f"{x:.2f}".replace(".", ",") if pd.notna(x) else "")
        loss_rate_col_found = True
    elif 'Tỷ lệ tổn thất (%)' in df.columns: # Giả định một tên cột khác có thể có
        df_temp["Tỷ lệ tổn thất"] = df['Tỷ lệ tổn thất (%)'].map(lambda x: f"{x:.2f}".replace(".", ",") if pd.notna(x) else "")
        loss_rate_col_found = True
    elif df.shape[1] > 14: # fallback to index 14 (15th column)
        # Cảnh báo: Sử dụng iloc có thể không ổn định nếu thứ tự cột thay đổi
        st.warning("Cảnh báo: Cột 'Tỷ lệ tổn thất' không tìm thấy theo tên. Đang sử dụng cột thứ 15 (chỉ số 14) làm 'Tỷ lệ tổn thất'. Vui lòng kiểm tra file Excel để đảm bảo chính xác.")
        df_temp["Tỷ lệ tổn thất"] = df.iloc[:, 14].map(lambda x: f"{x:.2f}".replace(".", ",") if pd.notna(x) else "")
        loss_rate_col_found = True
    else:
        st.error("Lỗi: File Excel không có cột 'Tỷ lệ tổn thất' (theo tên hoặc theo chỉ số 14). Vui lòng kiểm tra định dạng file và sheet 'dữ liệu' của bạn.")
        return None, None

    if not loss_rate_col_found:
        return None, None # Không có cột tỷ lệ tổn thất, không thể xử lý

    df_temp["Ngưỡng"] = df_temp["Tỷ lệ tổn thất"].apply(phan_loai_nghiem)
    tong_so = len(df_temp)
    tong_theo_nguong = df_temp["Ngưỡng"].value_counts().reindex(["<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%", ">=5 và <7%", ">=7%"], fill_value=0)
    return tong_so, tong_theo_nguong

# --- Đặt các nút "Làm mới dữ liệu" và "Tải file mẫu" cạnh nhau ---
col_refresh, col_download_folder = st.columns([1, 1])

with col_refresh:
    if st.button("🔄 Làm mới dữ liệu"):
        st.session_state.df_tba_thang = None
        st.session_state.df_tba_luyke = None
        st.session_state.df_tba_ck = None
        st.session_state.df_ha_thang = None
        st.session_state.df_ha_luyke = None
        st.session_state.df_ha_ck = None
        st.session_state.df_trung_thang_tt = None
        st.session_state.df_trung_luyke_tt = None
        st.session_state.df_trung_ck_tt = None
        st.session_state.df_trung_thang_dy = None
        st.session_state.df_trung_luyke_dy = None
        st.session_state.df_trung_ck_dy = None
        st.session_state.df_dv_thang = None
        st.session_state.df_dv_luyke = None
        st.session_state.df_dv_ck = None
        st.experimental_rerun()

with col_download_folder:
    with st.expander("📁 Tải file mẫu"):
        st.markdown("Bạn có thể tải xuống các file Excel mẫu dưới đây để sử dụng với chương trình:")

        # Đường dẫn tới thư mục chứa file mẫu
        template_folder = "templates"

        # Đảm bảo thư mục templates tồn tại
        if not os.path.exists(template_folder):
            st.warning(f"Thư mục '{template_folder}' không tồn tại. Vui lòng tạo thư mục này và đặt các file mẫu vào đó.")
        else:
            # Lặp qua các file trong thư mục templates và tạo nút download
            for filename in os.listdir(template_folder):
                if filename.endswith(".xlsx"): # Chỉ hiển thị các file Excel
                    file_path = os.path.join(template_folder, filename)
                    with open(file_path, "rb") as file:
                        st.download_button(
                            label=f"Tải xuống {filename}",
                            data=file,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key=f"download_{filename}"
                        )


# Tạo các tiện ích con theo phân nhóm
with st.expander("🔌 Tổn thất các TBA công cộng"):
    temp_upload_tba_thang = st.file_uploader("📅 Tải dữ liệu TBA công cộng - Theo tháng", type=["xlsx"], key="tba_thang")
    if temp_upload_tba_thang:
        try:
            # Đã thay thế "TÊN_SHEET_CHÍNH_XÁC_CỦA_BẠN" bằng "dữ liệu"
            st.session_state.df_tba_thang = pd.read_excel(temp_upload_tba_thang, sheet_name="dữ liệu")
            st.success("✅ Đã tải dữ liệu tổn thất TBA công cộng theo tháng!")
        except ValueError as e:
            st.error(f"Lỗi khi đọc sheet: {e}. Vui lòng kiểm tra tên sheet trong file Excel.")
            st.session_state.df_tba_thang = None
        except Exception as e:
            st.error(f"Đã xảy ra lỗi không mong muốn khi đọc file: {e}")
            st.session_state.df_tba_thang = None


    temp_upload_tba_luyke = st.file_uploader("📊 Tải dữ liệu TBA công cộng - Lũy kế", type=["xlsx"], key="tba_luyke")
    if temp_upload_tba_luyke:
        try:
            # Đã thay thế "TÊN_SHEET_CHÍNH_XÁC_CỦA_BẠN" bằng "dữ liệu"
            st.session_state.df_tba_luyke = pd.read_excel(temp_upload_tba_luyke, sheet_name="dữ liệu")
            st.success("✅ Đã tải dữ liệu tổn thất TBA công cộng - Lũy kế!")
        except ValueError as e:
            st.error(f"Lỗi khi đọc sheet: {e}. Vui lòng kiểm tra tên sheet.")
            st.session_state.df_tba_luyke = None
        except Exception as e:
            st.error(f"Đã xảy ra lỗi không mong muốn khi đọc file Lũy kế: {e}")
            st.session_state.df_tba_luyke = None

    temp_upload_tba_ck = st.file_uploader("📈 Tải dữ liệu TBA công cộng - Cùng kỳ", type=["xlsx"], key="tba_ck")
    if temp_upload_tba_ck:
        try:
            # Đã thay thế "TÊN_SHEET_CHÍNH_XÁC_CỦA_BẠN" bằng "dữ liệu"
            st.session_state.df_tba_ck = pd.read_excel(temp_upload_tba_ck, sheet_name="dữ liệu")
            st.success("✅ Đã tải dữ liệu tổn thất TBA công cộng - Cùng kỳ!")
        except ValueError as e:
            st.error(f"Lỗi khi đọc sheet: {e}. Vui lòng kiểm tra tên sheet.")
            st.session_state.df_tba_ck = None
        except Exception as e:
            st.error(f"Đã xảy ra lỗi không mong muốn khi đọc file Cùng kỳ: {e}")
            st.session_state.df_tba_ck = None


# --- Xử lý và hiển thị dữ liệu tổng hợp nếu có ít nhất một file được tải lên ---
if st.session_state.df_tba_thang is not None or \
   st.session_state.df_tba_luyke is not None or \
   st.session_state.df_tba_ck is not None:

    st.markdown("### 📊 Kết quả ánh xạ dữ liệu:")

    # Xử lý dữ liệu từng loại và chuẩn bị cho biểu đồ
    tong_so_thang, tong_theo_nguong_thang = process_tba_data(st.session_state.df_tba_thang)
    tong_so_luyke, tong_theo_nguong_luyke = process_tba_data(st.session_state.df_tba_luyke)
    tong_so_ck, tong_theo_nguong_ck = process_tba_data(st.session_state.df_tba_ck)

    col1, col2 = st.columns([2,2])

    with col1:
        st.markdown("#### 📊 Số lượng TBA theo ngưỡng tổn thất")
        fig_bar = go.Figure()
        colors = ['steelblue', 'darkorange', 'forestgreen', 'goldenrod', 'teal', 'red'] # Màu sắc cho từng ngưỡng

        # Thêm các thanh cho "Theo tháng"
        if tong_theo_nguong_thang is not None:
            fig_bar.add_trace(go.Bar(
                name='Theo tháng',
                x=tong_theo_nguong_thang.index,
                y=tong_theo_nguong_thang.values,
                text=tong_theo_nguong_thang.values,
                textposition='outside',
                textfont=dict(color='black', size=13, family='Arial')
            ))

        # Thêm các thanh cho "Lũy kế"
        if tong_theo_nguong_luyke is not None:
            fig_bar.add_trace(go.Bar(
                name='Lũy kế',
                x=tong_theo_nguong_luyke.index,
                y=tong_theo_nguong_luyke.values,
                text=tong_theo_nguong_luyke.values,
                textposition='outside',
                textfont=dict(color='black', size=13, family='Arial')
            ))

        # Thêm các thanh cho "Cùng kỳ"
        if tong_theo_nguong_ck is not None:
            fig_bar.add_trace(go.Bar(
                name='Cùng kỳ',
                x=tong_theo_nguong_ck.index,
                y=tong_theo_nguong_ck.values,
                text=tong_theo_nguong_ck.values,
                textposition='outside',
                textfont=dict(color='black', size=13, family='Arial')
            ))

        fig_bar.update_layout(
    xaxis=dict(title_font=dict(color='black', size=14, family='Arial',), tickfont=dict(color='black', size=13, family='Arial')),
    yaxis=dict(title_font=dict(color='black', size=14, family='Arial'), tickfont=dict(color='black', size=13, family='Arial')),
            barmode='group',
            height=400,
            xaxis_title='Ngưỡng tổn thất',
            yaxis_title='Số lượng TBA',
            margin=dict(l=20, r=20, t=40, b=40),
            legend_title_text='Loại dữ liệu'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.markdown("#### 🧩 Tỷ trọng TBA theo ngưỡng tổn thất")

        if tong_theo_nguong_thang is not None:
            st.markdown(f"##### Theo tháng (Tổng số: {tong_so_thang})")
            fig_pie_thang = go.Figure(data=[
                go.Pie(
                    labels=tong_theo_nguong_thang.index,
                    values=tong_theo_nguong_thang.values,
                    hole=0.5,
                    marker=dict(colors=colors),
                    textinfo='percent+label', textfont=dict(color='black', size=13, family='Arial'),
                    name='Theo tháng'
                )
            ])
            fig_pie_thang.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=40), showlegend=False)
            st.plotly_chart(fig_pie_thang, use_container_width=True)

        if tong_theo_nguong_luyke is not None:
            st.markdown(f"##### Lũy kế (Tổng số: {tong_so_luyke})")
            fig_pie_luyke = go.Figure(data=[
                go.Pie(
                    labels=tong_theo_nguong_luyke.index,
                    values=tong_theo_nguong_luyke.values,
                    hole=0.5,
                    marker=dict(colors=colors),
                    textinfo='percent+label', textfont=dict(color='black', size=13, family='Arial'),
                    name='Lũy kế'
                )
            ])
            fig_pie_luyke.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=40), showlegend=False)
            st.plotly_chart(fig_pie_luyke, use_container_width=True)

        if tong_theo_nguong_ck is not None:
            st.markdown(f"##### Cùng kỳ (Tổng số: {tong_so_ck})")
            fig_pie_ck = go.Figure(data=[
                go.Pie(
                    labels=tong_theo_nguong_ck.index,
                    values=tong_theo_nguong_ck.values,
                    hole=0.5,
                    marker=dict(colors=colors),
                    textinfo='percent+label', textfont=dict(color='black', size=13, family='Arial'),
                    name='Cùng kỳ'
                )
            ])
            fig_pie_ck.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=40), showlegend=False)
            st.plotly_chart(fig_pie_ck, use_container_width=True)


    # Hiển thị DataFrame ánh xạ cho file "Theo tháng" nếu nó tồn tại
    if st.session_state.df_tba_thang is not None:
        st.markdown("##### Dữ liệu TBA công cộng - Theo tháng:")
        df_test = st.session_state.df_tba_thang
        df_result = pd.DataFrame()

        # Giả định tên cột CHÍNH XÁC trong "dữ liệu"
        # Các tên cột này CẦN PHẢI khớp chính xác với tiêu đề trong file Excel của bạn
        expected_cols = {
            "Tên TBA": "Tên TBA",
            "Công suất": "Công suất",
            "Điện nhận": "Điện nhận",
            "Điện thương phẩm": "Điện thương phẩm", # Cột này dùng để tính Thương phẩm
            "Điện tổn thất": "Điện tổn thất", # Cột này là giá trị tổn thất hiển thị
            "Tỷ lệ tổn thất": "Tỷ lệ tổn thất", # hoặc 'Tỷ lệ tổn thất (%)'
            "Kế hoạch": "Kế hoạch",
            "So sánh": "So sánh"
        }

        # Kiểm tra sự tồn tại của các cột cần thiết
        missing_cols = [col_name for df_col_name, col_name in expected_cols.items() if col_name not in df_test.columns]

        # Điều chỉnh tên cột 'Tỷ lệ tổn thất' nếu trong Excel là 'Tỷ lệ tổn thất (%)'
        if 'Tỷ lệ tổn thất' not in df_test.columns and 'Tỷ lệ tổn thất (%)' in df_test.columns:
            expected_cols['Tỷ lệ tổn thất'] = 'Tỷ lệ tổn thất (%)'
            missing_cols = [col_name for df_col_name, col_name in expected_cols.items() if col_name not in df_test.columns]


        if missing_cols:
            st.warning(f"Dữ liệu TBA công cộng - Theo tháng: Thiếu các cột sau để ánh xạ: {', '.join(missing_cols)}. Vui lòng kiểm tra cấu trúc sheet 'dữ liệu'.")
        else:
            try:
                df_result["STT"] = range(1, len(df_test) + 1)
                df_result["Tên TBA"] = df_test[expected_cols["Tên TBA"]]
                df_result["Công suất"] = df_test[expected_cols["Công suất"]]
                df_result["Điện nhận"] = df_test[expected_cols["Điện nhận"]]

                # Cần đảm bảo cả hai cột đều tồn tại để tính toán Thương phẩm
                if expected_cols["Điện nhận"] in df_test.columns and expected_cols["Điện thương phẩm"] in df_test.columns:
                     df_result["Thương phẩm"] = df_test[expected_cols["Điện nhận"]] - df_test[expected_cols["Điện thương phẩm"]]
                else:
                    df_result["Thương phẩm"] = np.nan # Hoặc giá trị mặc định khác nếu không đủ cột
                    st.warning("Không đủ cột để tính Thương phẩm. Đảm bảo có cột 'Điện nhận' và 'Điện thương phẩm'.")

                df_result["Điện tổn thất"] = df_test[expected_cols["Điện tổn thất"]].round(0).astype("Int64", errors='ignore')
                df_result["Tỷ lệ tổn thất"] = df_test[expected_cols["Tỷ lệ tổn thất"]].map(lambda x: f"{x:.2f}".replace(".", ",") if pd.notna(x) else "")
                df_result["Kế hoạch"] = df_test[expected_cols["Kế hoạch"]].map(lambda x: f"{x:.2f}".replace(".", ",") if pd.notna(x) else "")
                df_result["So sánh"] = df_test[expected_cols["So sánh"]].map(lambda x: f"{x:.2f}".replace(".", ",") if pd.notna(x) else "")
                
                df_result["Ngưỡng"] = df_test[expected_cols["Tỷ lệ tổn thất"]].map(lambda x: phan_loai_nghiem(x))
                nguong_options = ["Tất cả", "<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%", ">=5 và <7%", ">=7%"]
                
                # Hiển thị selectbox lọc ngay phía trên dataframe
                chon_nguong = st.selectbox("🎯 Lọc theo ngưỡng tổn thất:", nguong_options, key="tba_thang_nguong_filter") 
                
                if chon_nguong != "Tất cả":
                    df_result = df_result[df_result["Ngưỡng"] == chon_nguong]
                
                df_result["Ngưỡng"] = pd.Categorical(df_result["Ngưỡng"], categories=["<2%", ">=2 và <3%", ">=3 và <4%", ">=4 và <5%", ">=5 và <7%", ">=7%"], ordered=True)

                st.dataframe(df_result, use_container_width=True) # Ensure it uses full width
            except KeyError as e:
                st.error(f"Lỗi khi ánh xạ dữ liệu: Không tìm thấy cột cần thiết '{e}'. Vui lòng kiểm tra tên cột trong file Excel của bạn trên sheet 'dữ liệu'.")
            except Exception as e:
                st.error(f"Đã xảy ra lỗi không mong muốn khi hiển thị DataFrame: {e}")


with st.expander("⚡ Tổn thất hạ thế"):
    upload_ha_thang = st.file_uploader("📅 Tải dữ liệu hạ áp - Theo tháng", type=["xlsx"], key="ha_thang")
    if upload_ha_thang:
        try:
            # Đã thay thế "TÊN_SHEET_CHÍNH_XÁC_CỦA_BẠN" bằng "dữ liệu"
            st.session_state.df_ha_thang = pd.read_excel(upload_ha_thang, sheet_name="dữ liệu", skiprows=6)
            st.success("✅ Đã tải dữ liệu tổn thất hạ áp - Theo tháng!")
        except ValueError as e:
            st.error(f"Lỗi khi đọc sheet hạ áp theo tháng: {e}. Vui lòng kiểm tra tên sheet trong file Excel.")
            st.session_state.df_ha_thang = None
        except Exception as e:
            st.error(f"Đã xảy ra lỗi không mong muốn khi đọc file hạ áp theo tháng: {e}")
            st.session_state.df_ha_thang = None

    upload_ha_luyke = st.file_uploader("📊 Tải dữ liệu hạ áp - Lũy kế", type=["xlsx"], key="ha_luyke")
    if upload_ha_luyke:
        try:
            # Đã thay thế "TÊN_SHEET_CHÍNH_XÁC_CỦA_BẠN" bằng "dữ liệu"
            st.session_state.df_ha_luyke = pd.read_excel(upload_ha_luyke, sheet_name="dữ liệu", skiprows=6)
            st.success("✅ Đã tải dữ liệu tổn thất hạ áp - Lũy kế!")
        except ValueError as e:
            st.error(f"Lỗi khi đọc sheet hạ áp lũy kế: {e}. Vui lòng kiểm tra tên sheet trong file Excel.")
            st.session_state.df_ha_luyke = None
        except Exception as e:
            st.error(f"Đã xảy ra lỗi không mong muốn khi đọc file hạ áp lũy kế: {e}")
            st.session_state.df_ha_luyke = None

    upload_ha_ck = st.file_uploader("📈 Tải dữ liệu hạ áp - Cùng kỳ", type=["xlsx"], key="ha_ck")
    if upload_ha_ck:
        try:
            # Đã thay thế "TÊN_SHEET_CHÍNH_XÁC_CỦA_BẠN" bằng "dữ liệu"
            st.session_state.df_ha_ck = pd.read_excel(upload_ha_ck, sheet_name="dữ liệu", skiprows=6)
            st.success("✅ Đã tải dữ liệu tổn thất hạ áp - Cùng kỳ!")
        except ValueError as e:
            st.error(f"Lỗi khi đọc sheet hạ áp cùng kỳ: {e}. Vui lòng kiểm tra tên sheet trong file Excel.")
            st.session_state.df_ha_ck = None
        except Exception as e:
            st.error(f"Đã xảy ra lỗi không mong muốn khi đọc file hạ áp cùng kỳ: {e}")
            st.session_state.df_ha_ck = None


with st.expander("⚡ Tổn thất trung thế (TBA Trung thế)"): # Đổi tên hiển thị cho rõ ràng
    upload_trung_thang_tt = st.file_uploader("📅 Tải dữ liệu TBA Trung áp - Theo tháng", type=["xlsx"], key="trung_thang_tt")
    if upload_trung_thang_tt:
        try:
            # Đã thay thế "TÊN_SHEET_CHÍNH_XÁC_CỦA_BẠN" bằng "dữ liệu"
            st.session_state.df_trung_thang_tt = pd.read_excel(upload_trung_thang_tt, sheet_name="dữ liệu", skiprows=6)
            st.success("✅ Đã tải dữ liệu tổn thất TBA Trung áp (Trung thế) - Theo tháng!")
        except ValueError as e:
            st.error(f"Lỗi khi đọc sheet trung áp (TT) theo tháng: {e}. Vui lòng kiểm tra tên sheet trong file Excel.")
            st.session_state.df_trung_thang_tt = None
        except Exception as e:
            st.error(f"Đã xảy ra lỗi không mong muốn khi đọc file trung áp (TT) theo tháng: {e}")
            st.session_state.df_trung_thang_tt = None

    upload_trung_luyke_tt = st.file_uploader("📊 Tải dữ liệu TBA Trung áp - Lũy kế", type=["xlsx"], key="trung_luyke_tt")
    if upload_trung_luyke_tt:
        try:
            # Đã thay thế "TÊN_SHEET_CHÍNH_XÁC_CỦA_BẠN" bằng "dữ liệu"
            st.session_state.df_trung_luyke_tt = pd.read_excel(upload_trung_luyke_tt, sheet_name="dữ liệu", skiprows=6)
            st.success("✅ Đã tải dữ liệu tổn thất TBA Trung áp (Trung thế) - Lũy kế!")
        except ValueError as e:
            st.error(f"Lỗi khi đọc sheet trung áp (TT) lũy kế: {e}. Vui lòng kiểm tra tên sheet trong file Excel.")
            st.session_state.df_trung_luyke_tt = None
        except Exception as e:
            st.error(f"Đã xảy ra lỗi không mong muốn khi đọc file trung áp (TT) lũy kế: {e}")
            st.session_state.df_trung_luyke_tt = None

    upload_trung_ck_tt = st.file_uploader("📈 Tải dữ liệu TBA Trung áp - Cùng kỳ", type=["xlsx"], key="trung_ck_tt")
    if upload_trung_ck_tt:
        try:
            # Đã thay thế "TÊN_SHEET_CHÍNH_XÁC_CỦA_BẠN" bằng "dữ liệu"
            st.session_state.df_trung_ck_tt = pd.read_excel(upload_trung_ck_tt, sheet_name="dữ liệu", skiprows=6)
            st.success("✅ Đã tải dữ liệu tổn thất TBA Trung áp (Trung thế) - Cùng kỳ!")
        except ValueError as e:
            st.error(f"Lỗi khi đọc sheet trung áp (TT) cùng kỳ: {e}. Vui lòng kiểm tra tên sheet trong file Excel.")
            st.session_state.df_trung_ck_tt = None
        except Exception as e:
            st.error(f"Đã xảy ra lỗi không mong muốn khi đọc file trung áp (TT) cùng kỳ: {e}")
            st.session_state.df_trung_ck_tt = None


with st.expander("⚡ Tổn thất các đường dây trung thế"):
    upload_trung_thang_dy = st.file_uploader("📅 Tải dữ liệu Đường dây Trung thế - Theo tháng", type=["xlsx"], key="trung_thang_dy")
    if upload_trung_thang_dy:
        try:
            # Đã thay thế "TÊN_SHEET_CHÍNH_XÁC_CỦA_BẠN" bằng "dữ liệu"
            st.session_state.df_trung_thang_dy = pd.read_excel(upload_trung_thang_dy, sheet_name="dữ liệu", skiprows=6)
            st.success("✅ Đã tải dữ liệu tổn thất Đường dây Trung thế - Theo tháng!")
        except ValueError as e:
            st.error(f"Lỗi khi đọc sheet đường dây trung thế theo tháng: {e}. Vui lòng kiểm tra tên sheet trong file Excel.")
            st.session_state.df_trung_thang_dy = None
        except Exception as e:
            st.error(f"Đã xảy ra lỗi không mong muốn khi đọc file đường dây trung thế theo tháng: {e}")
            st.session_state.df_trung_thang_dy = None

    upload_trung_luyke_dy = st.file_uploader("📊 Tải dữ liệu Đường dây Trung thế - Lũy kế", type=["xlsx"], key="trung_luyke_dy")
    if upload_trung_luyke_dy:
        try:
            # Đã thay thế "TÊN_SHEET_CHÍNH_XÁC_CỦA_BẠN" bằng "dữ liệu"
            st.session_state.df_trung_luyke_dy = pd.read_excel(upload_trung_luyke_dy, sheet_name="dữ liệu", skiprows=6)
            st.success("✅ Đã tải dữ liệu tổn thất Đường dây Trung thế - Lũy kế!")
        except ValueError as e:
            st.error(f"Lỗi khi đọc sheet đường dây trung thế lũy kế: {e}. Vui lòng kiểm tra tên sheet trong file Excel.")
            st.session_state.df_trung_luyke_dy = None
        except Exception as e:
            st.error(f"Đã xảy ra lỗi không mong muốn khi đọc file đường dây trung thế lũy kế: {e}")
            st.session_state.df_trung_luyke_dy = None

    upload_trung_ck_dy = st.file_uploader("📈 Tải dữ liệu Đường dây Trung thế - Cùng kỳ", type=["xlsx"], key="trung_ck_dy")
    if upload_trung_ck_dy:
        try:
            # Đã thay thế "TÊN_SHEET_CHÍNH_XÁC_CỦA_BẠN" bằng "dữ liệu"
            st.session_state.df_trung_ck_dy = pd.read_excel(upload_trung_ck_dy, sheet_name="dữ liệu", skiprows=6)
            st.success("✅ Đã tải dữ liệu tổn thất Đường dây Trung thế - Cùng kỳ!")
        except ValueError as e:
            st.error(f"Lỗi khi đọc sheet đường dây trung thế cùng kỳ: {e}. Vui lòng kiểm tra tên sheet trong file Excel.")
            st.session_state.df_trung_ck_dy = None
        except Exception as e:
            st.error(f"Đã xảy ra lỗi không mong muốn khi đọc file đường dây trung thế cùng kỳ: {e}")
            st.session_state.df_trung_ck_dy = None


with st.expander("🏢 Tổn thất toàn đơn vị"):
    upload_dv_thang = st.file_uploader("📅 Tải dữ liệu Đơn vị - Theo tháng", type=["xlsx"], key="dv_thang")
    if upload_dv_thang:
        try:
            # Đã thay thế "TÊN_SHEET_CHÍNH_XÁC_CỦA_BẠN" bằng "dữ liệu"
            st.session_state.df_dv_thang = pd.read_excel(upload_dv_thang, sheet_name="dữ liệu", skiprows=6)
            st.success("✅ Đã tải dữ liệu tổn thất Toàn đơn vị - Theo tháng!")
        except ValueError as e:
            st.error(f"Lỗi khi đọc sheet đơn vị theo tháng: {e}. Vui lòng kiểm tra tên sheet trong file Excel.")
            st.session_state.df_dv_thang = None
        except Exception as e:
            st.error(f"Đã xảy ra lỗi không mong muốn khi đọc file đơn vị theo tháng: {e}")
            st.session_state.df_dv_thang = None

    upload_dv_luyke = st.file_uploader("📊 Tải dữ liệu Đơn vị - Lũy kế", type=["xlsx"], key="dv_luyke")
    if upload_dv_luyke:
        try:
            # Đã thay thế "TÊN_SHEET_CHÍNH_XÁC_CỦA_BẠN" bằng "dữ liệu"
            st.session_state.df_dv_luyke = pd.read_excel(upload_dv_luyke, sheet_name="dữ liệu", skiprows=6)
            st.success("✅ Đã tải dữ liệu tổn thất Toàn đơn vị - Lũy kế!")
        except ValueError as e:
            st.error(f"Lỗi khi đọc sheet đơn vị lũy kế: {e}. Vui lòng kiểm tra tên sheet trong file Excel.")
            st.session_state.df_dv_luyke = None
        except Exception as e:
            st.error(f"Đã xảy ra lỗi không mong muốn khi đọc file đơn vị lũy kế: {e}")
            st.session_state.df_dv_luyke = None

    upload_dv_ck = st.file_uploader("📈 Tải dữ liệu Đơn vị - Cùng kỳ", type=["xlsx"], key="dv_ck")
    if upload_dv_ck:
        try:
            # Đã thay thế "TÊN_SHEET_CHÍNH_XÁC_CỦA_BẠN" bằng "dữ liệu"
            st.session_state.df_dv_ck = pd.read_excel(upload_dv_ck, sheet_name="dữ liệu", skiprows=6)
            st.success("✅ Đã tải dữ liệu tổn thất Toàn đơn vị - Cùng kỳ!")
        except ValueError as e:
            st.error(f"Lỗi khi đọc sheet đơn vị cùng kỳ: {e}. Vui lòng kiểm tra tên sheet trong file Excel.")
            st.session_state.df_dv_ck = None
        except Exception as e:
            st.error(f"Đã xảy ra lỗi không mong muốn khi đọc file đơn vị cùng kỳ: {e}")
            st.session_state.df_dv_ck = None