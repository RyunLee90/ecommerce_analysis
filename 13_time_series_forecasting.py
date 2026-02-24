import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import warnings

warnings.filterwarnings('ignore')

# 1. 데이터 로드
df = pd.read_csv('./data/master_ecommerce_data.csv')
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# 2. 데이터 필터링 (가장 중요한 공정)
daily_revenue = df.resample('D', on='order_purchase_timestamp')['price'].sum().fillna(0)
# 데이터가 정상적인 2018년 8월 15일까지만 자릅니다. (절벽 구간 제거)
daily_revenue = daily_revenue[daily_revenue.index <= '2018-08-15']

# 3. 로그 변환 (0 이하로 떨어지는 현상을 원천 봉쇄)
# log(0) 방지를 위해 1을 더해줍니다.
daily_revenue_log = np.log1p(daily_revenue)

# 4. 모델링 (추세와 계절성을 반영하되, 로그 데이터를 학습)
model = ExponentialSmoothing(daily_revenue_log, trend='add', seasonal='add', seasonal_periods=7)
model_fit = model.fit()

# 5. 향후 30일 예측 및 지수 변환(Exp)으로 복원
forecast_log = model_fit.forecast(30)
forecast = np.expm1(forecast_log)

# 6. 시각화 (최근 90일치 흐름과 연결)
plt.figure(figsize=(12, 6))
plt.plot(daily_revenue.tail(90), label='Actual Sales (Cleaned)')
plt.plot(forecast, label='Forecast (Next 30 days)', linestyle='--', color='red')
plt.axhline(0, color='black', linewidth=1) # 0원 기준선 표시
plt.title("Refined Sales Revenue Forecasting (Log-Transformed)")
plt.legend()

# 7. 결과 저장
forecast.to_csv('./data/13_sales_forecast.csv')
plt.savefig('./data/reports/13_sales_forecast_refined.png')

print("--- [시뮬레이션 기반 보정 완료] ---")
print(f"향후 30일 예상 총 매출: {forecast.sum():.2f} BRL")
plt.show()