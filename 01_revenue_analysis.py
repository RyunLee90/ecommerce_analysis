import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 세 개의 데이터 불러오기
customers = pd.read_csv('./data/olist_customers_dataset.csv')
orders = pd.read_csv('./data/olist_orders_dataset.csv')
items = pd.read_csv('./data/olist_order_items_dataset.csv') # 새로 추가된 '상품 상세' 파일

# 2. 데이터 순차적으로 합치기 (Merge)
# 먼저 주문과 고객을 합칩니다.
order_customer = pd.merge(orders, customers, on='customer_id')

# 그 결과에 상품 상세(가격 정보가 있는) 데이터를 합칩니다.
# order_id를 기준으로 합칩니다.
total_data = pd.merge(order_customer, items, on='order_id')

# 3. 도시별 매출 합계 계산 (Groupby 활용)
# 도시별로 묶어서(groupby), 가격(price)의 합계(sum)를 구합니다.
city_revenue = total_data.groupby('customer_city')['price'].sum().sort_values(ascending=False).head(10)

print("--- [매출 상위 10개 도시 (단위: 브라질 헤알)] ---")
print(city_revenue)

# 4. 시각화 (매출 그래프)
plt.figure(figsize=(12, 6))
sns.barplot(x=city_revenue.index, y=city_revenue.values, palette="magma")
plt.title('Top 10 Cities by Total Revenue', fontsize=16)
plt.xticks(rotation=45) # 도시 이름이 길면 겹치니까 사선으로 돌려줍니다.
plt.show()

# 5. 결과 저장
total_data.to_csv('./data/total_marketing_data.csv', index=False)
print("\n✅ 매출 데이터까지 포함된 통합 파일이 저장되었습니다!")