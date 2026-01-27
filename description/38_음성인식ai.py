'''
컴퓨터에서 재생되는 소리(유튜브, 음악 등) 실시간 음성 인식
필요한 라이브러리:
pip install SpeechRecognition
pip install pyaudio
pip install pydub
'''

import speech_recognition as sr
import pyaudio
import wave
import threading
import time

# ==================== 방법 1: 마이크로 시스템 오디오 캡처 ====================
def 시스템_오디오_인식_마이크():
    """
    스테레오 믹스(Stereo Mix) 또는 루프백 장치를 마이크로 선택하여 녹음
    Windows: 제어판 > 사운드 > 녹음 탭 > 스테레오 믹스 활성화 필요
    """
    r = sr.Recognizer()
    
    # 사용 가능한 마이크 목록 출력
    print("=== 사용 가능한 오디오 장치 목록 ===")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"{index}: {name}")
    
    print("\n스테레오 믹스 또는 루프백 장치 번호를 입력하세요:")
    device_index = int(input("장치 번호: "))
    
    # 선택한 장치로 마이크 설정
    with sr.Microphone(device_index=device_index) as source:
        print("\n=== 시스템 오디오 인식 시작 ===")
        print("유튜브나 음악을 재생하세요...")
        print("Ctrl+C를 눌러 종료")
        
        r.adjust_for_ambient_noise(source, duration=1)
        
        try:
            while True:
                print("\n[듣는 중...]")
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
                
                try:
                    text = r.recognize_google(audio, language='ko-KR')
                    print(f"인식된 텍스트: {text}")
                except sr.UnknownValueError:
                    print("음성을 인식할 수 없습니다")
                except sr.RequestError as e:
                    print(f"Google API 오류: {e}")
                    
        except KeyboardInterrupt:
            print("\n\n프로그램 종료")


# ==================== 방법 2: PyAudio로 직접 녹음 후 인식 ====================
def 시스템_오디오_녹음_후_인식():
    """
    시스템 오디오를 직접 녹음한 후 음성 인식
    WASAPI 루프백 장치 사용 (Windows)
    """
    # PyAudio 설정
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2  # 스테레오
    RATE = 44100
    RECORD_SECONDS = 10  # 녹음 시간
    WAVE_OUTPUT_FILENAME = "system_audio.wav"
    
    p = pyaudio.PyAudio()
    
    # 사용 가능한 장치 출력
    print("=== 사용 가능한 오디오 장치 ===")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print(f"{i}: {info['name']} (입력채널: {info['maxInputChannels']})")
    
    print("\n녹음할 장치 번호를 입력하세요 (스테레오 믹스/루프백):")
    device_index = int(input("장치 번호: "))
    
    print(f"\n{RECORD_SECONDS}초 동안 녹음을 시작합니다...")
    print("유튜브나 음악을 재생하세요!")
    
    # 스트림 열기
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=device_index,
                    frames_per_buffer=CHUNK)
    
    frames = []
    
    # 녹음
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        
        # 진행 표시
        if i % 50 == 0:
            print(".", end="", flush=True)
    
    print("\n녹음 완료!")
    
    # 스트림 종료
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # WAV 파일로 저장
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    # 음성 인식
    print("\n음성 인식 중...")
    r = sr.Recognizer()
    with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
        audio = r.record(source)
    
    try:
        text = r.recognize_google(audio, language='ko-KR')
        print(f"\n=== 인식 결과 ===")
        print(f"텍스트: {text}")
    except sr.UnknownValueError:
        print("음성을 인식할 수 없습니다")
    except sr.RequestError as e:
        print(f"Google API 오류: {e}")


# ==================== 방법 3: 연속 실시간 인식 ====================
class 실시간_시스템_오디오_인식:
    """백그라운드에서 계속 시스템 오디오를 인식"""
    
    def __init__(self, device_index=None):
        self.recognizer = sr.Recognizer()
        self.device_index = device_index
        self.is_running = False
        self.thread = None
    
    def 장치_선택(self):
        """오디오 장치 선택"""
        print("=== 사용 가능한 오디오 장치 목록 ===")
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"{index}: {name}")
        
        print("\n스테레오 믹스 또는 루프백 장치 번호를 입력하세요:")
        self.device_index = int(input("장치 번호: "))
    
    def 콜백_함수(self, recognizer, audio):
        """음성 인식 콜백"""
        try:
            text = recognizer.recognize_google(audio, language='ko-KR')
            print(f"\n[{time.strftime('%H:%M:%S')}] 인식: {text}")
        except sr.UnknownValueError:
            print(".", end="", flush=True)
        except sr.RequestError as e:
            print(f"\nAPI 오류: {e}")
    
    def 시작(self):
        """백그라운드 인식 시작"""
        if self.device_index is None:
            self.장치_선택()
        
        print("\n=== 실시간 시스템 오디오 인식 시작 ===")
        print("유튜브나 음악을 재생하세요...")
        print("'q' + Enter를 눌러 종료\n")
        
        # 마이크 설정
        mic = sr.Microphone(device_index=self.device_index)
        
        # 백그라운드 리스너 시작
        self.stop_listening = self.recognizer.listen_in_background(
            mic, 
            self.콜백_함수,
            phrase_time_limit=10
        )
        
        self.is_running = True
        
        # 종료 대기
        try:
            while True:
                if input() == 'q':
                    break
        except KeyboardInterrupt:
            pass
        
        self.종료()
    
    def 종료(self):
        """인식 종료"""
        if self.is_running:
            self.stop_listening(wait_for_stop=False)
            self.is_running = False
            print("\n프로그램 종료")


# ==================== 메인 실행 ====================
if __name__ == "__main__":
    print("=" * 50)
    print("시스템 오디오 음성 인식 프로그램")
    print("=" * 50)
    print("\n사용할 방법을 선택하세요:")
    print("1. 실시간 인식 (추천)")
    print("2. 녹음 후 인식 (10초)")
    print("3. 백그라운드 연속 인식")
    
    choice = input("\n선택 (1-3): ")
    
    if choice == "1":
        시스템_오디오_인식_마이크()
    elif choice == "2":
        시스템_오디오_녹음_후_인식()
    elif choice == "3":
        recognizer = 실시간_시스템_오디오_인식()
        recognizer.시작()
    else:
        print("잘못된 선택입니다")