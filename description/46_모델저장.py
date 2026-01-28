'''
머신러닝 모델
데이터로부터 패턴을 학습한 수학적 함수

scilkit-learn
- 전통적인 ML(회귀, 분류, 군집)

tensorflow / keras
- 딥러닝

pyTorch
- 딥러닝(연구 서비스 많이 사용)

XGBoost / LightGBM / CatBoost
- 트리 기반 고성능 모델

.joblib
.pkl 
.pb
.h5
.json
'''

import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

# 1. 데이터 준비 (100개의 샘플, 각 샘플은 10일치 주가 데이터)
X, y = np.random.random((100, 10)), np.random.random(100)

# 2. 모델 생성(랜덤 포레스트: 주가 예측에서 자주 사용되는 알고리즘)
model = RandomForestRegressor(n_estimators=100)

# 3. 학습시키기 (fit)
model.fit(X, y)

# 4. 파일로 저장 (.pkl 파일 생성)
joblib.dump(model, "나의모델.pkl")
print(f"학습시킨 모델 저장 완료")