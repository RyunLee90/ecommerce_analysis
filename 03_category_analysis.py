import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 필요한 4개의 데이터 불러오기
customers = pd.read_csv('./data/olist_customers_dataset.csv')
orders = pd.read_csv('./data/olist_orders_dataset.csv')
items = pd.read_csv('./data/olist_order_items_dataset.csv')
products = pd.read_csv('./data/olist_products_dataset.csv') # 상품 카테고리 정보가 있는 파일

# 2. 순차적 병합 (Merge Chain)
# 주문 + 고객 + 상품상세 + 상품카테고리 순으로 합칩니다.
df = pd.merge(orders, customers, on='customer_id')
df = pd.merge(df, items, on='order_id')
df = pd.merge(df, products, on='product_id')

# 3. 카테고리별 매출 합계 계산
# product_category_name 기준이며, 매출(price)의 합계를 구합니다.
category_revenue = df.groupby('product_category_name')['price'].sum().sort_values(ascending=False).head(10)

print("--- [매출 상위 10개 카테고리] ---")
print(category_revenue)

# 4. 시각화
plt.figure(figsize=(12, 8))
sns.barplot(x=category_revenue.values, y=category_revenue.index, palette="rocket")
plt.title('Top 10 Product Categories by Revenue', fontsize=16)
plt.xlabel('Total Revenue (BRL)', fontsize=12)
plt.ylabel('Category Name', fontsize=12)
plt.show()

# 5. 결과 저장
df.to_csv('./data/final_category_data.csv', index=False)
print("\n✅ 카테고리 분석이 포함된 최종 파일이 저장되었습니다!")