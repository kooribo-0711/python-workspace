'''

pip install pandas numpy scikit-learn matplotlib finance-datareader
시각화/머신/딥러닝 데이터를 다룰 때 많이 사용하는 모듈들

주가 예측을 진행할 때 Yahoo finance에서 csv 파일을 로드하거나 다운하여 예측함.

pandas
- 데이터 엑셀화
- 파이썬에서 표 형식의 데이터를 다루는데 최적화 도구
- 주가 데이터처럼 날짜, 종가, 거래량 등이 나열된 데이터를 정렬하고 계산할 때 사용

numpy
- 고속 수치 계산
- python의 기본 목록 리스트보다 빠르고 효율적으로 복잡한 수학 연산 처리
- 머신러닝 모델이 내부적으로 계산을 수행할 때 기반이 되는 엔진 역할

matplotlib
- 계산된 결과가 예측된 주가 흐름을 선 그래프, 막대 그래프 등으로 그려줌
- 그래프 화 하여 추세를 확인 

scikit-learn
- 머신러닝 종합세트
- 선형회귀, 랜덤 포레스트 등 수많은 머신러닝 알고리즘 구현
- 사람이 직접 복잡한 수학공식을 코딩할 필요 없이 함수 호출만으로 모델을 만들고 학습시킬 수 있다

finance-datareader
- 금융 데이터 수집기
- 한국 거래소의 삼성전자 주가 뿐만 아니라 미국시장(나스닥, 엔비디아 등), 환율, 비트코인 시세까지 코드 한 줄로 불러올 수 있게 해주는 모듈

'''
import FinanceDataReader as fdr
import pandas as pd

# 삼성전자 데이터 (최근 2년치) 삼성전자 종목코드 = 005930
df = fdr.DataReader('005930', '2024-01-01')

# CPU에서 가볍게 돌리기 위해 복잡한 지표 대신 평균 이동선과 전일 대비 등락률 정도 사용
# target : 내일의 종가(close)를 예측
# df = data frame. 파이썬 내부에서 사용하는 엑셀 표
# df = 세가지 요소로 구성
#    1. 열 (Columns)    : 세로 줄. 주가데이터에서는 종가(close), 시가(Open), 거래량(Volume) 같은 항목들이 열
#    2. 행 (Rows/Index) : 가로 줄. 보통 주가 데이터에서는 날짜(Date)가 각 행을 구분하는 기준.
#    3. 값 (Values)     : 표 안에 들어있는 실제 숫자 데이터

# .rolling(window=5) = rolling : 굴러간다 window=5 : 최근 5일치 데이터
# .rolling(window=5) = rolling : 최근 5일치 데이터를 하나의 묶음으로 보겠다
# .mean() = 묶은 데이터들의 수학적 평균 구하기 메서드 기능
# df['MA5'] = 우리가 만든 변수 공간의 명칭
# df['MA5'] = 5일치 묶은 종가 데이터의 평균을 구하여 담아놓은 공간의 명칭
# MA5 = Moving Averages 5
df['MA5']=df['Close'].rolling(window=5).mean()
# MA20 = 평균 20일치를 묶어 담아놓은 공간의 명칭
df['MA20']=df['Close'].rolling(window=20).mean()

# 다음날의 종가를 목표로 설정
# shift(-1) 보통 데이터 한 줄 오늘의 기록
# 내일의 종가 데이터를 오늘 날짜 옆으로 끌어올려 나란히 두는 것
# 모델이 오늘은 이랬으니 내일은 저렇구나 학습할 수 있게 오늘의 종가 / 내일의 종가 이런 형태로 배치
df['Target']=df['Close'].shift(-1)
# .dropna() = 데이터가 들어있지 않은 엑셀 칸은 버리기 drop = 버리다
# na() nan = 엑셀표가 비어있을 때 작성하는 데이터 형태
# 참고로 머신러닝 모델은 비어있는 값이 있으면 학습을 못하고 에러냄. 숫자들과 빈 칸을 더하기 시키거나 나누기와 같은 산술을 진행할 수 없기 때문.
# inplace=True .dropna() 빈 값 지우기 결과를 실시간으로 장부 업데이트해서 사용할 수 있게 허용
# 만약 inplace=Flase라면  업데이트 된 결과를 새로운 변수 이름에 담기와 같은 추가변수 생성 작업 필요
# inplace=True로 해주는 것은 df 공간에 바로바로 실시간 저장 업데이트 처리
df.dropna(inplace=True)

# x = 개발자간의 관습적으로 사용하는 변수이름 문제 혹은 입력 데이터
# df[] = 하나의 열을 가져와서 사용할 때 표기하는 방법
# df[[]] = 여러개의 열을 묶어서 표 형태로 가져올 때 사용
# [] = 하나의 목록데이터 가져올게
# [[]] = 여러개의 목록 데이터 가져올게
X = df[['Close', 'MA5', 'MA20']]
y = df['Target']

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# X는 왜 대문자로 쓰는가?
# 대문자 X는 여러개의 행과 열을 가진 2차원 데이터 표를 의미
# 우리가 문제로 만든 X에는 종가, MA5, MA20 등 여러개의 데이터 열이 들어있음
# 이렇게 덩어리가 큰 데이터는 대문자로 표기

# y는 왜 소문자로 쓰는다?
# 한 줄 짜리 데이터기 때문 (내일의 종가)

# [[]] = 대문자 X로 여러 리스트를 가지고 있는 데이터다.
# [  ] = 소문자 y로 하나의 리스트를 가지고 있는 데이터다.
# train_test_split = 데이터 분류하기 : 시험을 보기 전에 공부할 문제와 실전 테스트를 나누는 과정
# X_train, y_train : 공부용 ; 모델이 정답과 함께 공부할 교과서
# X_test, y_test : 시험용 ; 모델이 제대로 공부했는지 확인하기 위한 기말고사
# 모델에게 X_test 문제만 주고 y_test 실제 정답과 얼마나 일치하는지 확인

# test_size=02 : 전체 데이터 중에서 20%는 시험 문제로 떼어놓고 나머지 80% 공부하겠다
# shuffle=False  주가 데이터는 시간 순서가 매우 중요
#                데이타를 무작위로 섞으면 미래 데이터를 보고 과거를 맞추는 이상한 경과가 발생하므로
#                순서대로 데이터를 자르며 학습시키기 위해 섞지 않겠다
# train_test_split() 변수 순서 중요!
# X_train, X_test로 되어있는 변수 공간에 80% 데이터를 전달하여
# X_train 에서는 학습 X_test 정답에 대한 데이터를 각각 구분하여 데이터 분류
# y_train, y_test로 되어있는 변수 공간에 20% 데이터를 전달하여
# y_train 에서는 문제를 내고 y_test 문제에 대한 정답 맞추기를 하며 얼마나 정답을 맞추는지 확률 처리를 진행
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# 선형 회귀 모델
# 데이터들이 이루는 어떤 선형적인 흐름을 찾는 아주 가벼운 모델
model = LinearRegression()

# .fit() : 실제로 모델이 데이터를 학습시키는 명령어
# X_train 오늘의 상황과 y_train 내일의 결과 사이의 관계를 모델이 스스로 깨닫게 함.
# 로봇에게 교과서와 정답지를 던져주고 둘의 상관관계를 파악하시오 하는 과정
# fot : 딱 맞추다. 데이터에 모델을 맞추어 학습시킨다  
model.fit(X_train, y_train)

# 학습을 마친 모델에게 새로운 문제를 주고 결과를 예측하게 한다.
# 모델은 한번도 본 적 없는 시험지를 보고 규칙대로 내일 주가는 이럴 것이다 답안 제출
predictions = model.predict(X_test)
# 공부 다 했으면 이 문제(X-test) 맞추고 맞춘 결과를 predictions 변수 공간에 담아두기

# 모델이 훈련한 점수의 정확도 확인
# 프린트 출력으로 확인하기
score = model.score(X_test, y_test)
print(f"모델 정확도 : {score:.4f}")