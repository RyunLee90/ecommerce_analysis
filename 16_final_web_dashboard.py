import streamlit as st
import pandas as pd
import plotly.express as px
import warnings

# 1. 시스템 로그 및 경고 차단
warnings.filterwarnings('ignore')

# 2. 페이지 설정
st.set_page_config(page_title="Brazil E-commerce Insight Pro", layout="wide")

# 3. 데이터 로드 (캐싱 적용)
@st.cache_data
def load_data():
    try:
        rfm = pd.read_csv('./data/rfm_result.csv')
        forecast = pd.read_csv('./data/13_sales_forecast.csv')
        forecast.columns = ['Date', 'Predicted_Revenue']
        forecast['Date'] = pd.to_datetime(forecast['Date'])
        return rfm, forecast
    except Exception:
        return None, None

rfm, forecast = load_data()

if rfm is not None and forecast is not None:
    # 4. 사이드바 - 동적 필터링 도구
    st.sidebar.title("🔍 데이터 컨트롤 센터")
    
    # [필터 1] 세그먼트 다중 선택
    all_segments = rfm['Segment'].unique().tolist()
    selected_segments = st.sidebar.multiselect(
        "분석할 고객 등급 선택",
        options=all_segments,
        default=all_segments
    )
    
    # [필터 2] 예측 날짜 범위 조절
    min_date = forecast['Date'].min().date()
    max_date = forecast['Date'].max().date()
    date_range = st.sidebar.slider(
        "매출 예측 기간 설정",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
    )

    # 5. 실시간 데이터 필터링 적용
    filtered_rfm = rfm[rfm['Segment'].isin(selected_segments)]
    filtered_forecast = forecast[
        (forecast['Date'].dt.date >= date_range[0]) & 
        (forecast['Date'].dt.date <= date_range[1])
    ]

    # 6. 메인 화면 구성
    st.title("🚀 브라질 이커머스 전략 대시보드 v2.0")
    st.markdown(f"현재 **{len(filtered_rfm):,}명**의 고객 데이터를 분석 중입니다.")
    st.markdown("---")

    col1, col2 = st.columns([1, 1.2]) # 비율 조절

    with col1:
        st.subheader("👥 고객 세그먼트 분포")
        fig1 = px.pie(filtered_rfm, names='Segment', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig1, key="pie_v2", width='stretch')

    with col2:
        st.subheader("📈 매출 예측 트렌드 (선택 기간)")
        fig2 = px.line(filtered_forecast, x='Date', y='Predicted_Revenue', markers=True)
        st.plotly_chart(fig2, key="line_v2", width='stretch')

    # 7. 상세 데이터 테이블 (하단 배치)
    st.markdown("---")
    with st.expander("📑 필터링된 고객 상세 데이터 보기 (상위 100명)"):
        st.dataframe(filtered_rfm.head(100), width='stretch')

    st.success("✅ 실시간 필터링이 적용되었습니다. 왼쪽 사이드바에서 조건을 변경해 보세요!")
else:
    st.error("⚠️ 데이터를 불러올 수 없습니다. 분석 스크립트를 먼저 실행해 주세요.")