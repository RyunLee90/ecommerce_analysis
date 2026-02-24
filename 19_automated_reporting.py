import pandas as pd
import sqlite3
from datetime import datetime

# 1. DB 연결 (우리가 만든 금고에서 데이터를 가져옵니다)
def generate_report():
    conn = sqlite3.connect('./data/ecommerce_analytics.db')
    
    # [데이터 분석 1] VIP 고객 리스트 추출
    vip_query = "SELECT customer_unique_id, Segment FROM rfm_analysis WHERE Segment = 'VIP (최상위)'"
    vips = pd.read_sql(vip_query, conn)
    
    # [데이터 분석 2] 전체 고객 수 및 등급별 요약
    summary_query = "SELECT Segment, COUNT(*) as count FROM rfm_analysis GROUP BY Segment"
    summary = pd.read_sql(summary_query, conn)
    
    conn.close()

    # 2. 보고서 파일 내용 구성 (텍스트 형식)
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report_content = f"""
    ==================================================
    🚀 브라질 이커머스 비즈니스 분석 요약 보고서
    ==================================================
    - 생성 일시: {report_date}
    
    [1. 고객 세그먼트 현황]
    {summary.to_string(index=False)}
    
    [2. 핵심 인사이트]
    - 현재 집중 관리 대상인 VIP 고객은 총 {len(vips)}명입니다.
    - 이탈 위험군에 대한 선제적 마케팅 캠페인이 필요합니다.
    
    [3. 향후 권장 액션 플랜]
    - VIP 대상 전용 쿠폰 발송 (24시간 이내)
    - 매출 예측 트렌드에 따른 재고 확보 전략 수립
    ==================================================
    """
    
    # 3. 파일로 저장 (data 폴더 안에 report.txt 생성)
    report_path = './data/business_report.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✅ 보고서 생성 완료: {report_path}")
    print(report_content)

# 함수 실행
if __name__ == "__main__":
    generate_report()