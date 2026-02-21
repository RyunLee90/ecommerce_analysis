import pandas as pd
import sqlite3
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import warnings

# 1. 시끄러운 경고 숨기기
warnings.filterwarnings('ignore')

# 2. DB 금고에서 데이터 로드 (Cursor 프로젝트 경로 기준)
def load_data():
    conn = sqlite3.connect('./data/ecommerce_analytics.db')
    query = """
    SELECT r.Recency, r.Frequency, r.Monetary, c.is_churned
    FROM rfm_analysis r
    JOIN churn_prediction c ON r.customer_unique_id = c.customer_unique_id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

print("📡 데이터를 로드 중입니다...")
df = load_data()
X = df[['Recency', 'Frequency', 'Monetary']]
y = df['is_churned']

# 훈련/테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. [핵심] 최적의 조합을 찾기 위한 설정값 지도 (Grid)
param_grid = {
    'n_estimators': [50, 100],      # 나무의 개수
    'max_depth': [10, 20, None],    # 나무의 깊이
    'min_samples_split': [2, 5]     # 가지를 치기 위한 최소 기준
}

# 4. 자동 탐색 엔진 가동 (Grid Search)
print("🚀 최적의 모델 레시피를 탐색 중입니다. Cursor 터미널을 지켜보세요...")
grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=3, scoring='accuracy')
grid_search.fit(X_train, y_train)

# 5. 최종 결과 도출
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

print("\n" + "="*40)
print("🏆 최적의 파라미터 조합:", grid_search.best_params_)
print(f"📊 최적화 후 모델 정확도: {accuracy_score(y_test, y_pred):.4f}")
print("="*40)

# 6. 추가 진단: 과적합/데이터 특성 확인용
print("\n[진단] 데이터 분할 크기")
print(f" - Train size: {len(y_train)}")
print(f" - Test size : {len(y_test)}")

print("\n[진단] CV 결과")
print(f" - Best CV mean accuracy: {grid_search.best_score_:.4f}")

print("\n[진단] Train/Test 정확도")
y_train_pred = best_model.predict(X_train)
print(f" - Train accuracy: {accuracy_score(y_train, y_train_pred):.4f}")
print(f" - Test  accuracy: {accuracy_score(y_test, y_pred):.4f}")

print("\n[진단] 타깃 분포 (전체 데이터 기준)")
print(y.value_counts(normalize=True))

print("\n[진단] 테스트 세트 Confusion Matrix")
print(confusion_matrix(y_test, y_pred))

print("\n[진단] 테스트 세트 상세 리포트")
print(classification_report(y_test, y_pred))

# 7. 최적화된 뇌(모델) 저장
joblib.dump(best_model, './data/optimized_churn_model.pkl')
print("✅ 최적화 모델 저장 완료: ./data/optimized_churn_model.pkl")