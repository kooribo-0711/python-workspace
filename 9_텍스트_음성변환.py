'''
qTTS
-google Text To Speech
-글자를 사람 음성(mp3)로 바꿔주는 도구

playsound
- mp3 파일을 바로 재생해주는 도구

설치방법

pip install gTTS
pip install playsound

한 번에 설치하는 방법!
install 다음에 띄어쓰기를 작성하면 다수의 기능을 한번에 설치
pip install 기능1번 기능2번 기능3번 ..... 개수 제한 없음
pip install gTTS playsound3
'''
# pip install 기능을 설치할 때 아래와 같이 버전이 맞지 않아요! 오류가 발생할 수 있다.
# 특정 도구를 실행할 때 파이썬 버전과 설치하고자 하는 도구의 버전이 맞지 않을 경우 아래와 같은 에러가 발생
# pip install gTTS playsound==1.3.0
# 현재 파이썬과 사용하고자 하는 도구의 버전을 맞추어 사용할 수 있도록 설정
# 나의 컴퓨터에 존재하는 언어와 도구가 일치하지 않아서 발생
# 2025년 유행어를 조선시대 가서 하는 격
# 참고로 playsound는 playsound3로 새롭게 출시된 상황
# ai나 gpt에게 물어보며 해결 가능

from gtts import gTTS
from playsound3 import playsound
'''
gtts 내부에 다양한 기능들이 존재하는데, 그 중에서 하나만 가져올 때 사용하는 방법
playsound3 내부에 다양한 기능들이 존재하는데 , 중에서 하나만 가져와서 사용할 때 작성하는 방법
불필요한 기능까지 불러오면 프로그램이 무거워지기 대문에 하나의 기능만 호출하는 방법
'''

text = "25년 마지막 월요일"
'''
gTTS(text="음성으로 변환할 텍스트", lang="작성한 언어의 국가").save("오디오 파일로 저장하기")

playsound("소리로 들을 오디오 파일 작성하기")
'''


tts = gTTS(text="안녕하세요.", lang='ko')
tts.save("hi.mp3")
playsound("hi.mp3")

# 주의할 점
# \ 역슬래시는 특정 명령어를 작성할 때 사용
# \n = 줄바꿈의 약자
# 윈도우 컴퓨터의 경우 폴더를 나누는 경로가 \ 역슬래시 형태로 존재하므로
# 대부분의 코드에서는 window에 작성된 경로를 넣으면 존재하지 않는 명령어를 실행했다는 에러 발생
# 파이썬으로 출력된 구문을 코드 내에 기술 할 때는
# 경로를 제외하고 기술