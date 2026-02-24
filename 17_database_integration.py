import pandas as pd
import sqlite3

# 1. DB 연결
conn = sqlite3.connect('./data/ecommerce_analytics.db')

try:
    # 2. 데이터 로드 (캡처해주신 파일 경로 기준)
    rfm_df = pd.read_csv('./data/rfm_result.csv')
    churn_df = pd.read_csv('./data/12_churn_prediction_result.csv')
    
    # 3. DB 테이블로 이관 (일단 데이터를 안전하게 넣습니다)
    rfm_df.to_sql('rfm_analysis', conn, if_exists='replace', index=False)
    churn_df.to_sql('churn_prediction', conn, if_exists='replace', index=False)
    print("✅ [단계 1] CSV 데이터를 DB로 안전하게 이관했습니다.")

    # 4. 동적 컬럼 확인 (에러 방지의 핵심)
    # churn_df의 컬럼 중 'churn'이 포함된 컬럼을 찾거나, 없으면 마지막 컬럼을 선택
    cols = churn_df.columns.tolist()
    target_col = next((c for c in cols if 'churn' in c.lower()), cols[-1])
    
    print(f"🔍 [단계 2] 분석에 사용할 컬럼을 찾았습니다: '{target_col}'")

    # 5. 동적 SQL 쿼리 실행
    # 컬럼명에 공백이나 특수문자가 있을 수 있으므로 큰따옴표("")로 감쌉니다.
    query = f"""
    SELECT r.customer_unique_id, r.Segment, c."{target_col}" as prediction
    FROM rfm_analysis r
    JOIN churn_prediction c ON r.customer_unique_id = c.customer_unique_id
    WHERE r.Segment = 'VIP (최상위)'
    LIMIT 5
    """
    
    insight_df = pd.read_sql(query, conn)
    print("\n✅ [단계 3] DB 조회 테스트 결과:")
    print(insight_df)

except Exception as e:
    print(f"❌ 최종 오류 발생: {e}")
    print("💡 팁: 12_churn_prediction_result.csv 파일의 내용을 확인해 보세요.")

finally:
    conn.close()