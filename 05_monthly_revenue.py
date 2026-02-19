import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 마스터 파일 불러오기
df = pd.read_csv('./data/master_ecommerce_data.csv')

# 2. 날짜 데이터 형식으로 변환 (중요!)
# 'order_purchase_timestamp' 컬럼을 문자열에서 실제 날짜 형식으로 바꿉니다.
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# 3. '연-월' 정보만 따로 추출하기
# 예: 2017-01-30 -> 2017-01
df['month_year'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)
# 4. 월별 매출 합계 계산
monthly_revenue = df.groupby('month_year')['price'].sum()

# 5. 시각화 (꺾은선 그래프)
plt.figure(figsize=(15, 6))
sns.lineplot(x=monthly_revenue.index, y=monthly_revenue.values, marker='o', color='b')

plt.title('Monthly Revenue Trend', fontsize=16)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Total Revenue (BRL)', fontsize=12)
plt.xticks(rotation=45) # 월 이름이 겹치지 않게 회전
plt.grid(True) # 눈금선 추가
plt.show()

print("--- [월별 매출 요약] ---")
print(monthly_revenue.tail()) # 최근 5개월치 출력