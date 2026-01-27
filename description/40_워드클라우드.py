'''

wordcloud : 텍스트 데이터를 시각화해서 단어 구름을 만드는 라이브러리
텍스트에서 자주 등장하는 단어를 크기와 색상으로 표현한 이미지
많이 나온 단어 = 크게 표시
적게 나온 단어 = 작게 표시

pip install wordcloud
'''

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 텍스트 데이터

text = " 파이썬 파이썬 파이썬 데이터 분석 머신러닝 인공지능 파이썬 데이터"

# 워드 클라우드 생성
wc = WordCloud(font_path='malgun.ttf',
               width=400,height=400,background_color='white').generate(text)

# 이미지로 표시
plt.figure(figsize=(10,5))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()


# 특정 키워드에 대한 뉴스를검색하고, 가장 많이 보이는 댓글 데이터 수집해서 1위부터 10위까지 나열해줘

'''
음성비서 = 자연어

AI 인공지능분야 
- 시계열(Time series) 비전(Computer Vision), 자연어(NLP)
- 인공지능이 데이터를 인식하고 처리하는 가장 대표적인 분야 세가지

1. 시계열 AI
- 시간의 흐름에 따라 순서대로 기록된 데이터를 분석하는 기술
- 과거의 데이터 패턴을 학습하여 미래를 예측하거나 이상 징후를 탐지하는데 특화
- 시간 순서가 있는 연속적인 숫자 데이터(주식 가격, 날씨, 서버 로그, 심박수 등)
- 다음달 매출 예측, 금융 시장 문서, 서버 모니터링 시스템, 물류 수요 예측

2. 비전 AI(이미지 JPG, PNG), 비디오 영상(프레임 단위 분석)
- 객체 탐지(Object Detection) : 이미지 내 사람이 있는지, 차가 있는지 위치를 찾음
- 이미지 분류(Classification) : 이 사진이 강아지인지 조양이인지 분류 마스크 착용 유무
- 세그맨테이션 (Segmentation) : 배경과 객체를 픽셀 단위로 정밀하게 분리 (누끼따기)
- 자율주행 자동차의 신호인식, 얼굴 인식 잠금 해제, 의료용 MRI 판독, 공장 불량품 검수

3. 자연어 처리(NLP : Natural Language Processing)
- 인간이 사용하는 언어(텍스트, 음성)를 컴퓨터가 이해하고 생성하도록 하는 기술
- 문맥, 뉘앙스, 문법적 구조를 파악하는 것
- 다루는 데이터 : 텍스트, 음성 데이터(비정형 데이터)
- 핵심 기술 : 트랜스포머, 토큰화, 임베딩 등
- 언어 이해(NLU) : 감정 분석(긍정/부정), 의도 파악, 핵심 키워드 추출
- 언어 생성(NLG) : 작문 요약, 번역, 챗봇 응답 생성
- ChatGPT와 같은 챗봇, 구글 번역기, 스팸 메일 필터링, 음성비서(Siri) 등...


'''



