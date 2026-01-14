from gtts import gTTS
from playsound3 import playsound

# 아랫 코드 tts를 제거하여 한번에 hello 라는 파일로 저장하기 
tts = gTTS(text="안녕하세요.", lang='ko')
tts.save("hi.mp3")
playsound("hi.mp3")

gTTS(text="안녕하세요, 반갑습니다, 잘가세요.", lang='ko').save("hello.mp3")