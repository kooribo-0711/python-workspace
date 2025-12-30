'''
pip에 접속하지 않고 특정 파일을 호출하여 사용

파이썬 언어를 만든 개발자 측에서 파이썬 언어를 사용하는 개발 유저들이
가장 많이 사용하고 선호하는 기술의 경우 버전을 업그레이드하며
특정 도구나 기술은 pip에서 다운로드를 하지 않고 사용할 수 있도록
언어를 설치하며 도구와 기술도 함께 설치

ex) import zipfile : 압축 파일을 만들고 다루는 도구
    import os : 운영체제 기능(컴퓨터에 존재하는 파일이나, 폴더)을 다루는 도구
'''

import zipfile
import os

def 파일확인():
    for 파일 in os.listdir():
        print("현재 폴더에 존재하는 모든 파일 리스트 : ", 파일)

# 파일확인()

def 폴더제외후확인():
    for f in os.listdir():
        if os.path.isfile(f):
            print("폴더 제외하고 모든 파일리스트를 확인 : ", f)

# ctrl + space = 이름과 유사한 기능, 변수 이름 추천
# 폴더제외후확인()

def 특정확장자만확인():
    for t in os.listdir():
        if t.endswith(".png"):
            print("png 파일만 확인 : ", t)

# 특정확장자만확인()


def 다수확장자만확인():
    for t in os.listdir():
        if t.endswith((".png", ".mp3")):
            print("png, mp3 파일만 확인 : ", t)

# 다수확장자만확인()

'''
컴퓨터 directory = 폴더
os.listdir() = 현재 폴더의 모든 파일과 모든 폴더 이름을 리스트 반환
               현재 폴더의 모든 파일 조회
               
os.listdir("C:/Users/TJ") = C드라이브에서 Users라는 폴더 내에 TJ폴더 내에 존재하는 모든 파일 목록 조회.
endswith() = 문자열이 특정 확장자로 끝나는지 확인
                만약 존재한다면 true 형태로 결과를 전달
endswith((".png") : 하나의 확장자로만 끝나는 경우에는 ()를 하나만 작성
                현재 내가 순회하는 파일이 .png로 끝나는 파일인가? 맞으면 true 아니면 false로 건너뛴다
endswith((".png", ".mp3")) = 두가지 이상의 확장자를 포함하여 끝나는 경우를 확인하고자 하는 경우에는 (())로 작성
endswith((".png", ".mp3", ".py")) = 세가지 이상의 확장자를 포함해도 괄호는 이중으로 (())
'''

with zipfile.ZipFile("py_files.zip", 'w') as 압축파일:
    for f in os.listdir():
        if f.endswith('.py'):
            압축파일.write(f)
            print(f"{f} 압축 됨")
