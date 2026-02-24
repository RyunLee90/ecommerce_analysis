import pandas as pd

# 1. 모든 분석 결과 로드
rfm = pd.read_csv('./data/rfm_result.csv')
association = pd.read_csv('./data/09_association_rules_result.csv')
churn = pd.read_csv('./data/12_churn_prediction_result.csv')
forecast = pd.read_csv('./data/13_sales_forecast.csv')

# 2. 핵심 지표 요약 (Executive Summary)
total_customers = len(rfm)
vip_count = len(rfm[rfm['Segment'] == 'VIP (최상위)'])
predicted_churn_rate = (churn['is_churned'].sum() / len(churn)) * 100
next_month_revenue = forecast.iloc[:, 1].sum()

# 3. 최종 브리핑 출력
print("==========================================")
print("     BRAZIL E-COMMERCE FINAL REPORT       ")
print("==========================================")
print(f"1. 전체 관리 고객 수: {total_customers:,}명")
print(f"2. VIP 고객 비중: {(vip_count/total_customers)*100:.2f}% ({vip_count:,}명)")
print(f"3. 예상 이탈 위험률: {predicted_churn_rate:.2f}%")
print(f"4. 차월 예상 매출액: {next_month_revenue:,.2f} BRL")
print("------------------------------------------")
print("5. 핵심 추천 상품 조합 (Lift 기준 TOP 1)")
print(f"   [{association.iloc[0]['antecedents']}] 구매 시")
print(f"   -> [{association.iloc[0]['consequents']}] 추천 (Lift: {association.iloc[0]['lift']:.2f})")
print("==========================================")
print("✅ 모든 분석 파이프라인이 성공적으로 완료되었습니다.")