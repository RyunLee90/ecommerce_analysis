import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 마스터 파일 불러오기 및 날짜 변환
df = pd.read_csv('./data/master_ecommerce_data.csv')
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# 2. 요일(이름)과 시간 추출
df['weekday'] = df['order_purchase_timestamp'].dt.day_name()
df['hour'] = df['order_purchase_timestamp'].dt.hour

# 3. 히트맵을 위한 '피벗 테이블' 만들기 (요일/시간별 주문 건수 합산)
# 행(index)은 요일, 열(columns)은 시간으로 설정합니다.
heatmap_data = df.pivot_table(index='weekday', columns='hour', values='order_id', aggfunc='count')

# 4. 요일 순서 정렬 (월요일부터 일요일까지 보기 좋게 배치)
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
heatmap_data = heatmap_data.reindex(days)

# 5. 히트맵 시각화
plt.figure(figsize=(15, 8))
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=False) 
plt.title('Order Density by Day and Hour', fontsize=16)
plt.xlabel('Hour of Day', fontsize=12)
plt.ylabel('Day of Week', fontsize=12)
plt.show()
