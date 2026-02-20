import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="Brazil E-commerce Insight", layout="wide")

# 2. 데이터 로드 (파일 유무 체크 추가)
@st.cache_data
def load_data():
    try:
        rfm = pd.read_csv('./data/rfm_result.csv')
        forecast = pd.read_csv('./data/13_sales_forecast.csv')
        return rfm, forecast
    except FileNotFoundError:
        st.error("⚠️ 데이터를 찾을 수 없습니다. 분석 스크립트를 먼저 실행하세요.")
        return None, None

rfm, forecast = load_data()

if rfm is not None:
    # 3. 사이드바 - 요약 지표
    st.sidebar.title("📊 핵심 성과 지표 (KPI)")
    total_rev = forecast.iloc[:, 1].sum()
    st.sidebar.metric("차월 예상 매출액", f"{total_rev:,.0f} BRL", delta="9.65%")
    st.sidebar.metric("이탈 위험률", "17.93%", delta="-2.1%", delta_color="inverse")

    # 4. 메인 화면
    st.title("🚀 브라질 이커머스 전략 대시보드")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👥 고객 세그먼트 분포")
        fig1 = px.pie(rfm, names='Segment', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        # 최신 문법 반영: width='stretch'
        st.plotly_chart(fig1, width='stretch')

    with col2:
        st.subheader("📈 향후 30일 매출 예측")
        forecast.columns = ['Date', 'Predicted_Revenue']
        fig2 = px.line(forecast, x='Date', y='Predicted_Revenue', markers=True)
        # 최신 문법 반영: width='stretch'
        st.plotly_chart(fig2, width='stretch')

    st.warning("⚠️ **전략 제안:** 이탈 위험이 높은 VIP 고객을 대상으로 연관 상품 프로모션 집행이 시급합니다.")