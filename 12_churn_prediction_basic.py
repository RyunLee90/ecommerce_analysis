import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

# 1. 데이터 로드
df = pd.read_csv('./data/11_customer_behavior_by_segment.csv')

# 2. 이탈 라벨 생성 (최근성 기준)
df['is_churned'] = df['Recency'].apply(lambda x: 1 if x > 400 else 0)

# 3. 특성 및 타겟 설정
X = df[['Frequency', 'Monetary']]
y = df['is_churned']

# 4. 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. [핵심] 불균형 해소를 위한 모델 설정
# class_weight='balanced'가 소수의 이탈자 데이터를 더 중요하게 학습하게 합니다.
model = LogisticRegression(class_weight='balanced')
model.fit(X_train, y_train)

# 6. 결과 출력
y_pred = model.predict(X_test)

print("--- [데이터 분포 확인] ---")
print(df['is_churned'].value_counts())

print("\n--- [수정된 이탈 예측 보고서] ---")
# precision(정밀도)과 recall(재현율)을 함께 확인해야 진짜 실력을 알 수 있습니다.
print(classification_report(y_test, y_pred))
print(f"예측된 이탈 위험 고객 수: {sum(y_pred)}명")

# 7. 결과 저장
df.to_csv('./data/12_churn_prediction_result.csv', index=False)