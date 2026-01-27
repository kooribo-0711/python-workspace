'''
SpeechRecognition
- 음성을 텍스트로 변환하는 파이썬 라이브러리.
  다양한 음성인식 API를 지원하고, 마이크나 오디오 파일에서 음성을 인식할 수 있다.
  마이크 입력 또는 오디오 파일에서 음성 인식
  다양한 오디오 포멧 지원 (WAV, FLAC 등)

pyaudio
- 파이썬에서 오디오 입출력을 다루는 라이브러리
- 마이크로부터 오디오 녹음
- 스피커로 오디오 재생
- 실시간 오디오 스트리밍 처리
- 다양한 오디오 포멧과 샘플레이트 지원

* SpeechRecognition가 마이크 입력을 받으려면 pyaudio 모듈의 도움을 받음
* pyaudio는 각 컴퓨터 레벨의 오디오 라이브러리에 의존하므로, 설치방법이 각 컴퓨터마다 다를 수 있음
* 특히 window에서는 별도의 도구가 필요할 수 있다

pip install SpeechRecognition pyaudio --break-system-packages

'''

# 1. 마이크로 음성 인식하기
import speech_recognition as sr

# 인식할 하나의 도구 생성
r = sr.Recognizer() # r 데이터 공간 음성을 인식할 수 있는 도구 하나가 놓여져 있는 상태

# 마이크로 음성 녹음
with sr.Microphone() as source:
    print("말씀하세요...")
    audio = r.listen(source)

#구글 음성 인식
try:
    # recognize_google
    text = r.recognize_google(audio, language="ko-KR")
    print(f"인식된 텍스트 : {text}")
except sr.UnknownValueError: # 음성을 인식하지 못한 예외상황이 발생했다면
    print("음성을 인식할 수 없습니다.")
except sr.RequestError: # 음성 변환을 도와주는 서버와 연결을 실패했을 경우 request = 인터넷에서는 요청하다. 웹사이트/데이터 등
    print(("API 요청 실패!"))

# 오디오 파일에서 인식하기

def 오디오_파일():
    r=sr.Recognizer() # r이라는 공간 안에 음성인식을 위한 기능을 잠시 넣어둔 상태
    # 오디오 파일 열기
    with sr.AudioFile('audio.wav') as source:
        audio = r.record(source)

    text = r.recognize_google(audio, language="ko-KR") 
    print(text)

def 주변소음측정하기():
    with sr.Microphone() as source:
        print("주변 소음 측정 중...")
        r.adjust_for_ambient_noise(source, duration=1) # 1초동안 주변 소음 측정 어디까지가 배경 소음인지 파악
        print("말씀하세요...")
        audio = r.listen(source)

# 주변소음측정하기()

def listen_and_recognize():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("듣고 있습니다...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="ko-KR")
        return text
    except:
        return None
#사용
result = listen_and_recognize()
if result:
    print(f"당신이 말한 것 : {result}")

# listen_and_recognize()
