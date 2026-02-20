import pandas as pd
import os

# 1. 필요 데이터 로드
master_path = './data/master_ecommerce_data.csv'
rfm_path = './data/rfm_result.csv'

if not os.path.exists(rfm_path):
    print("⚠️ 오류: rfm_result.csv가 없습니다. 08_rfm_segmentation.py를 먼저 실행해 주세요.")
    exit()

df_master = pd.read_csv(master_path)
df_rfm = pd.read_csv(rfm_path)

# 2. 데이터 병합 (Merge)
# 고객 ID를 기준으로 마스터 데이터에 RFM 세그먼트 정보를 붙입니다.
# [최종 수정] 11번 파일의 merge 부분을 아래와 같이 바꾸세요.
# [수정 후] df_rfm의 모든 컬럼(Recency, Frequency, Monetary 등)을 한 번에 다 가져옵니다.
df_merged = pd.merge(df_master, df_rfm, on='customer_unique_id', how='left')

# 3. [심화] Loyal Customers(충성 고객) 분석
target_segment = 'Loyal Customers'
df_loyal = df_merged[df_merged['Segment'] == target_segment]

print(f"--- [{target_segment}] 분석 결과 ---")
if not df_loyal.empty:
    # 충성 고객이 가장 많이 구매한 카테고리 TOP 5
    top_cats = df_loyal['product_category_name_english'].value_counts().head(5)
    print("\n[인기 카테고리 TOP 5]")
    print(top_cats)
    
    # 충성 고객의 평균 객단가
    avg_price = df_loyal['price'].mean()
    print(f"\n[평균 구매 금액]: {avg_price:.2f} BRL")
else:
    print(f"{target_segment} 데이터가 없습니다. 등급 분류를 확인해 주세요.")

# 4. 전체 세그먼트별 매출 기여도 분석
segment_revenue = df_merged.groupby('Segment')['price'].sum().sort_values(ascending=False)
print("\n--- 세그먼트별 전체 매출 기여도 ---")
print(segment_revenue)

# 5. 결과 저장
df_merged.to_csv('./data/11_customer_behavior_by_segment.csv', index=False)
print("\n✅ 분석 완료: './data/11_customer_behavior_by_segment.csv' 저장됨")