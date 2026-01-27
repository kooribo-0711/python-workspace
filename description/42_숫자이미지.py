import matplotlib.pyplot as plt
from sklearn.datasets import load_digits # 1797개의 숫자 이미지 들어있음

# 데이터 로드
digits = load_digits() #sklearn 회사가 모아놓은 숫자 데이터를 사용할 준비(0~9)

# 첫번째 숫자 선택
# load_digits() 내부에는 
# images[1] 에는 1 숫자 이미지가 들어있고
# target[1] 에는 1 숫자 문자로 1이라는 라벨 표기가 세트로 들어있다
# 손 이미지 데이터 중구난방 수집하여 load_digits() 기능을 가져오기 전에
# 연구자가 수집한 이미지 데이터 하나가 어떤 숫자인지 분류하는 과정을 러닝
image = digits.images[8] # 8*8 이미지
label = digits.target[8] # 정답 숫자

# 이미지 출력
plt.imshow(image, cmap='gray')
plt.title(f"Label:{label}")
plt.axis('off')
plt.show()


