import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import os

# 1. 데이터 로드 및 경로 확인
file_path = './data/master_ecommerce_data.csv'
if not os.path.exists(file_path):
    print(f"오류: {file_path} 파일이 없습니다. 경로를 확인해주세요.")
    exit()

df = pd.read_csv(file_path)

# 2. 전처리: 카테고리 결측치 제거
df = df.dropna(subset=['product_category_name_english'])

# 3. 장바구니 행렬 생성 (Pivot Table)
# 각 주문(order_id)에 어떤 카테고리가 담겼는지 1(True) / 0(False)로 표시
basket = (df.groupby(['order_id', 'product_category_name_english'])['product_id']
          .count().unstack().reset_index().fillna(0)
          .set_index('order_id'))

# 4. 최신 Pandas/mlxtend 규격 반영 (bool 타입 변환으로 성능 최적화 및 경고 방지)
def encode_units(x):
    return 1 if x >= 1 else 0

basket_sets = basket.map(encode_units).astype(bool)

# 5. 연관 규칙 탐색 (성공했던 지지도 0.0002 적용)
print("🔍 연관 규칙을 분석 중입니다... (지지도: 0.0002)")
frequent_itemsets = apriori(basket_sets, min_support=0.0002, use_colnames=True)

# 6. 향상도(Lift) 기준 규칙 생성
if not frequent_itemsets.empty:
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
    
    if not rules.empty:
        # 결과를 Lift 순으로 정렬하여 상위 10개 출력
        result = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].sort_values('lift', ascending=False)
        print("\n--- [분석 완료: 상품 연관 규칙 결과] ---")
        print(result.head(10))
        
        # 분석 결과 저장 (Phase 6 시각화에서 사용)
        result.to_csv('./data/09_association_rules_result.csv', index=False)
        print("\n✅ 결과가 './data/09_association_rules_result.csv'에 저장되었습니다.")
    else:
        print("결과가 없습니다. 분석 기준을 더 낮춰보세요.")
else:
    print("빈번 항목을 찾지 못했습니다.")