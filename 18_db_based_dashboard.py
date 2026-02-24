import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import warnings

# 1. 경고 메시지 숨기기
warnings.filterwarnings('ignore')

# 2. 대시보드 화면 설정
st.set_page_config(page_title="브라질 이커머스 DB 대시보드", layout="wide")

# 3. DB에서 데이터를 가져오는 함수
@st.cache_data
def load_data_from_db():
    conn = sqlite3.connect('./data/ecommerce_analytics.db')
    # rfm 데이터 로드
    rfm = pd.read_sql("SELECT * FROM rfm_analysis", conn)
    # 매출 예측 데이터 로드 (파일)
    forecast = pd.read_csv('./data/13_sales_forecast.csv')
    forecast.columns = ['Date', 'Predicted_Revenue']
    forecast['Date'] = pd.to_datetime(forecast['Date'])
    conn.close()
    return rfm, forecast

rfm, forecast = load_data_from_db()

# 4. [추가됨] 왼쪽 사이드바 필터
st.sidebar.title("🔍 데이터 필터")
all_segments = rfm['Segment'].unique().tolist()
selected_segments = st.sidebar.multiselect("고객 등급 선택", options=all_segments, default=all_segments)

# 5. [추가됨] 필터링 적용
filtered_rfm = rfm[rfm['Segment'].isin(selected_segments)]

# 6. 대시보드 본문 그리기
st.title("🚀 DB 기반 실시간 전략 대시보드")
st.success("✅ 현재 SQLite 데이터베이스 엔진으로부터 실시간 데이터를 서빙 중입니다.")
st.markdown("---")

# 7. [추가됨] 차트 배치 (이 부분이 있어야 그래프가 나옵니다!)
col1, col2 = st.columns(2)

with col1:
    st.subheader("👥 고객 등급 분포")
    fig1 = px.pie(filtered_rfm, names='Segment', hole=0.4)
    st.plotly_chart(fig1, use_container_width=True) # width='stretch' 대신 호환성 위해 변경

with col2:
    st.subheader("📈 향후 매출 예측 트렌드")
    fig2 = px.line(forecast, x='Date', y='Predicted_Revenue', markers=True)
    st.plotly_chart(fig2, use_container_width=True)