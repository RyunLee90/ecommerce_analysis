import pandas as pd
import numpy as np
from scipy import stats

# 1. 시뮬레이션 환경 설정
np.random.seed(42)
n_customers = 5000  # 테스트 대상 고객 수

# 2. 가상의 A/B 테스트 데이터 생성
# A그룹(대조군): 기존 추천 방식 / B그룹(실험군): 연관 분석 기반 추천
group_a = np.random.normal(loc=150, scale=30, size=n_customers) # 평균 150 BRL 구매
group_b = np.random.normal(loc=165, scale=35, size=n_customers) # 평균 165 BRL 구매 (추천 효과로 상승 가정)

# 3. 데이터프레임 구성
df_ab = pd.DataFrame({
    'Group': ['A'] * n_customers + ['B'] * n_customers,
    'Purchase_Amount': np.concatenate([group_a, group_b])
})

# 4. 통계적 유의성 검정 (T-test)
t_stat, p_value = stats.ttest_ind(group_a, group_b)

# 5. 결과 리포트 출력
print("--- [A/B 테스트 시뮬레이션 결과] ---")
print(f"A그룹(기존) 평균 구매액: {group_a.mean():.2f} BRL")
print(f"B그룹(연관 추천) 평균 구매액: {group_b.mean():.2f} BRL")
print(f"매출 상승률: {((group_b.mean() - group_a.mean()) / group_a.mean() * 100):.2f}%")
print(f"T-통계량: {t_stat:.4f}")
print(f"p-value: {p_value:.4e}")

if p_value < 0.05:
    print("\n✅ 결론: 연관 상품 추천 전략은 통계적으로 매우 유의미한 효과가 있습니다! (도입 확정)")
else:
    print("\n❌ 결론: 우연에 의한 차이일 가능성이 높습니다. 전략을 재검토하십시오.")

# 6. 결과 저장
df_ab.to_csv('./data/14_ab_test_result.csv', index=False)