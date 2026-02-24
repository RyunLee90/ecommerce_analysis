import matplotlib.pyplot as plt

# 한글 깨짐 방지를 위한 폰트 설정 (윈도우 기준)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# 1. 마스터 데이터 불러오기
df = pd.read_csv('./data/master_ecommerce_data.csv')
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# 2. 분석 기준일 설정 (데이터상 마지막 날짜 + 1일)
# 실무에서는 '오늘'을 기준으로 하지만, 과거 데이터이므로 데이터의 끝점을 기준으로 합니다.
snapshot_date = df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

# 3. RFM 지표 계산
# R(Recency): 마지막 구매일로부터 며칠 지났나?
# F(Frequency): 얼마나 자주 샀나? (주문번호 개수)
# M(Monetary): 총 얼마를 썼나? (가격 합계)
rfm = df.groupby('customer_unique_id').agg({
    'order_purchase_timestamp': lambda x: (snapshot_date - x.max()).days,
    'order_id': 'count',
    'price': 'sum'
})

# 4. 컬럼명 알기 쉽게 변경
rfm.columns = ['Recency', 'Frequency', 'Monetary']

# 5. 결과 확인 (상위 5명)
print("--- [RFM 계산 결과 상위 5인] ---")
print(rfm.sort_values('Monetary', ascending=False).head())

# 6. 시각화 (금액별 분포 확인)
plt.figure(figsize=(10, 6))
sns.histplot(rfm['Monetary'], bins=100, kde=True, color='purple')
plt.title('Distribution of Monetary Value', fontsize=15)
plt.xlim(0, 1000) # 대다수 고객을 보기 위해 범위 제한
plt.show()

# 7. RFM 스코어링 (1~5점 부여)
# Recency는 작을수록(최근일수록) 높은 점수, F와 M은 클수록 높은 점수입니다.
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])

# 8. 최종 합계 점수 계산
rfm['RFM_Score'] = rfm['R_Score'].astype(int) + rfm['F_Score'].astype(int) + rfm['M_Score'].astype(int)

# 9. 등급 정의 (간단한 예시)
def get_segment(score):
    if score >= 13: return 'VIP (최상위)'
    elif score >= 9: return 'Loyal (우수)'
    elif score >= 5: return 'Potential (잠재)'
    else: return 'At Risk (이탈위기)'

rfm['Segment'] = rfm['RFM_Score'].apply(get_segment)

# 10. 등급별 고객 수 확인
print("\n--- [고객 등급별 분포] ---")
print(rfm['Segment'].value_counts())

# 11. 시각화 (등급별 비율)
plt.figure(figsize=(10, 6))
rfm['Segment'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['gold', 'silver', 'lightcoral', 'gray'])
plt.title('Customer Segments Share')
plt.ylabel('')
plt.show()

# --- [중요] 분석 결과를 CSV 파일로 저장하는 로직 ---
# 데이터프레임 인덱스(customer_unique_id)를 포함하여 저장합니다.
rfm.to_csv('./data/rfm_result.csv') 

print("\n✅ [파일 생성 완료] ./data/rfm_result.csv 파일이 저장되었습니다.")