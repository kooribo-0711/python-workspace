# 1. 데이터 불러오기
# 2. 학습 / 테스트 데이터 분리
# 3. 정규화 (성능 향상)
# 4. 모델 분류
# 5. 예측
# 6. 정확도 평가

from sklearn.datasets import load_wine
from sklearn.linear_model import LogisticRegression
'''
LogisticRegression = 분류를 위한 머신러닝 모델
결과를 확률로 계산해서 어느 클래스인지 결정
Regression이 있지만 회귀가 아니라 분류에서 사용

클래스 0 일 확률 0.1
클래스 1 일 확률 0.8
클래스 2 일 확률 0.1
'''
x, y = load_wine(return_X_y=True)
model = LogisticRegression(max=1000).fit(x,y)
print(model.score(x,y))