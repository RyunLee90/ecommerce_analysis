import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 5개의 데이터 불러오기 (번역 파일 추가)
customers = pd.read_csv('./data/olist_customers_dataset.csv')
orders = pd.read_csv('./data/olist_orders_dataset.csv')
items = pd.read_csv('./data/olist_order_items_dataset.csv')
products = pd.read_csv('./data/olist_products_dataset.csv')
translation = pd.read_csv('./data/product_category_name_translation.csv') # 번역 파일

# 2. 데이터 병합 (Merge Chain)
df = pd.merge(orders, customers, on='customer_id')
df = pd.merge(df, items, on='order_id')
df = pd.merge(df, products, on='product_id')

# 포르투갈어 카테고리명을 영어로 바꾸기 위해 번역 데이터를 합칩니다.
df = pd.merge(df, translation, on='product_category_name')

# 3. 영어 카테고리별 매출 합계 계산
# 이제 'product_category_name_english' 컬럼을 사용합니다.
category_rev_en = df.groupby('product_category_name_english')['price'].sum().sort_values(ascending=False).head(10)

print("--- [매출 상위 10개 카테고리 (영어)] ---")
print(category_rev_en)

# 4. 시각화 (그래프가 더 이해하기 쉬워집니다)
plt.figure(figsize=(12, 8))
sns.barplot(x=category_rev_en.values, y=category_rev_en.index, palette="viridis")
plt.title('Top 10 Categories by Revenue (English)', fontsize=16)
plt.xlabel('Revenue (BRL)', fontsize=12)
plt.show()

# 5. 최종 데이터 저장 (이것이 진짜 '마스터 데이터'입니다)
df.to_csv('./data/master_ecommerce_data.csv', index=False)
print("\n✅ 영어 번역까지 완료된 마스터 파일이 저장되었습니다!")