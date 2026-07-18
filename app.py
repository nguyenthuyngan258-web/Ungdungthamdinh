import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Cấu hình giao diện
st.set_page_config(page_title="Hệ thống Thẩm định Tín dụng", layout="wide")

st.markdown("""
    <style>
    .metric-card {background-color: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0;}
    </style>
""", unsafe_allow_html=True)

st.title("🏦 Hệ thống Thẩm định Tín dụng Cá nhân")

# --- INPUT SECTION ---
with st.container():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Thông tin Khoản vay")
        so_tien_vay = st.number_input("Số tiền vay (VNĐ)", 0, 10000000000, 500000000)
        thoi_han = st.slider("Thời gian vay (tháng)", 6, 360, 60)
        lai_suat = st.number_input("Lãi suất cho vay (%/năm)", 0.0, 30.0, 10.0)
        
    with col2:
        st.subheader("Thông tin Khách hàng")
        thu_nhap = st.number_input("Thu nhập hàng tháng (VNĐ)", 0, 1000000000, 20000000)
        so_nguoi_pt = st.number_input("Số người phụ thuộc", 0, 10, 0)
        du_no_cu = st.number_input("Dư nợ khoản vay cũ (VNĐ)", 0)
        
    with col3:
        st.subheader("Tài sản & CIC")
        gia_tri_tsdb = st.number_input("Giá trị TSĐB (VNĐ)", 1, 10000000000, 1000000000)
        cic_score = st.selectbox("Điểm tín dụng CIC", ["Tốt (Nhóm 1)", "Trung bình (Nhóm 2)", "Xấu (Nhóm 3+)"])

# --- CALCULATIONS ---
goc_lai_hang_thang = (so_tien_vay / thoi_han) + (so_tien_vay * (lai_suat/100/12))
dti = ((du_no_cu + goc_lai_hang_thang) / (thu_nhap + 1)) * 100
ltv = (so_tien_vay / gia_tri_tsdb) * 100

# --- ANALYSIS SECTION ---
st.divider()
st.subheader("📊 Kết quả Phân tích")

c1, c2, c3 = st.columns(3)
c1.metric("Chỉ số DTI", f"{dti:.2f}%")
c2.metric("Chỉ số LTV", f"{ltv:.2f}%")
c3.metric("Kết luận sơ bộ", "ĐẠT" if dti < 45 and ltv < 80 else "RỦI RO")

# Biểu đồ Gauge
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = dti,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Tỷ lệ DTI (%)"},
    gauge = {'axis': {'range': [0, 100]},
             'steps' : [{'range': [0, 40], 'color': "lightgreen"},
                        {'range': [40, 70], 'color': "yellow"},
                        {'range': [70, 100], 'color': "red"}]}))

st.plotly_chart(fig, use_container_width=True)

# Lịch trả nợ dự kiến
if st.checkbox("Xem lịch trả nợ chi tiết"):
    data = {'Tháng': range(1, thoi_han + 1), 
            'Số tiền phải trả': [goc_lai_hang_thang] * thoi_han}
    st.dataframe(pd.DataFrame(data), use_container_width=True)
