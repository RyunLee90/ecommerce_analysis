import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 마스터 파일 불러오기
df = pd.read_csv('./data/master_ecommerce_data.csv')

# 2. 날짜 데이터를 파이썬이 이해할 수 있는 '날짜 형식'으로 변환
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# 3. 요일(0=월, 6=일)과 시간(0~23) 정보 추출
df['weekday'] = df['order_purchase_timestamp'].dt.weekday
df['hour'] = df['order_purchase_timestamp'].dt.hour

# 4. 숫자로 된 요일을 글자(Mon, Tue...)로 바꾸기
weekday_map = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
df['weekday_name'] = df['weekday'].map(weekday_map)

# 5. 요일별 주문 건수 시각화
plt.figure(figsize=(10, 5))
weekday_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
sns.countplot(data=df, x='weekday_name', order=weekday_order, palette='viridis')
plt.title('Orders by Day of Week', fontsize=15)
plt.show()

# 6. 시간대별 주문 건수 시각화
plt.figure(figsize=(12, 5))
sns.countplot(data=df, x='hour', color='skyblue')
plt.title('Orders by Hour of Day', fontsize=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

print("✅ 요일 및 시간 분석 그래프 생성이 완료되었습니다!")