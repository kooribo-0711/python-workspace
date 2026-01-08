'''
.set~~ 생성기능

.get~~ 생성되어진 무언가의 데이터를 가져오는 기능

'''
import zipfile, os, random, string

def 비밀번호압축고전():
    문자들 = string.digits
    비밀번호 = "".join(random.choice(문자들) for _ in range(4))
    print(f"생성된 비밀번호 : {비밀번호}")

    with zipfile.ZipFile('password1.zip', 'w') as my_zip:
        # my_zip.setpassword(비밀번호.encode())
        for file in os.listdir():
            if file.endswith('.txt'):
                my_zip.write(file, compress_type=zipfile.ZIP_DEFLATED)
                my_zip.setpassword(비밀번호.encode())
                print(f"{file} 압축완료")

# zipfile -> 압축하기 할 때 굉장히 예전에 사용 많이 하던 파이썬 인기 모듈이었지만
# 시대가 변하며 파이썬이 성장했지만 zipfile 모듈이 따라오지 못하여 현재는 주로 압축 풀기용으로 사용됨
# 업그레이드 버전으로 pyminizip 이라는 압축 모듈이 흥행

'''
현재 사용중인 컴퓨터에는 C++ 언어가 없음
pyminizip -> C++ + python 조합으로 이루어진 모듈
컴퓨터에 C관련 언어를 설치 후 사용 가능
pip install pyminizip

pip install pyzipper

    # 비밀번호 생성
    # 현재 폴더에서 png 확장자를 찾은 후 
    # zip 파일에 넣고 비밀번호를 강력히 설정
'''
import pyzipper
'''
AES = 비밀번호로 자물쇠 거는 잠금 방식
현재 표준으로 사용되는 암호화 방식
일반 zipfile의 경우, 허술한 다이얼 자물쇠라면
    AESzipfile은 은행 고급 자물쇠
비밀번호는 같아보여도 자물쇠 내부 구조 다름
AES = 은행 앱, 카카오톡, WIFI 정부 기업 보안 믿고 사용하는 표준 암호
AES-128 -192 -256 중에서 AES-256은 거의 철벽급 수비

pyzipper.AESZipFile = pyzipper.py 내부에 .AESZipFile() 메서드 기능이 작성되어있다.
.AESZipFile() = AES-256암호화해서 압축한 파일
compression=pyzipper.ZIP_DEFLATED,
compression = 파일을 ZIP에 넣을 때 압축방식 지정
.ZIP_DEFLATEd = 가장 널리 쓰이는 표준 압축 알고리즘 ; 속도 균형 좋음
7zip. WinRAR, windows 기본 압축 모두 지원
encryption = ZIP파일의 암호화 방식 지정
.WZ_AES = WinZip AES 암호화 규격. 현재 zip에서 가장 안전한 방식. 대부분의 압축프로그램 지원
encryption=pyzipper.WZ_AES
'''
def 비밀번호압축최신():
    with pyzipper.AESZipFile(
        'pyZipperPassword1.zip', # 압축_파일_이름.압축파일형식                                  # 압축상자 이름, 종류
        'w', # write                                                                          # 압축상자에 물건을 담겠다
        compression=pyzipper.ZIP_DEFLATED, # 파일을 ZIP에 넣을 때 압축방식 지정                 # 압축할 때 입축 잘 되는가?        
        encryption=pyzipper.WZ_AES  # ZIP파일의 암호화 방식을 지정                              # 단단한 자물쇠로 잠그자      
    ) as zf: # 이렇게 설정한 형식을 zf라는 변수 이름으로 사용하겠다                               
        zf.setpassword(b'hipassword') # 비밀번호 설정. 반드시 b = byte 타입으로 비밀번호 생성
        # zf.write('test.txt')
        zf.write('내정보_단일큐알.png') # 현재 폴더에 존재하는 내정보.png 파일을 zip 추가
        
'''
AES 잠금이 가능한 상자                           상자에 쓰이는 자물쇠 종류
pyzipper.AESZipFile()              vs              pyzipper.WZ_AES
  ZIP 파일을 만들고                          이 ZIP 상자를 AES 방식으로 잠그자
        열고                                이 가방에 은행 금고 자물쇠를 달아라
파일을 넣고 빼는 그릇 상자               만약에 이 속성을 설정하지 않으면? -> 비밀번호 없는 ZIP이 되거나 약한 옛날 암호화가 됨

b= byte : 사람이 작성한 비밀번호를 컴퓨터가 이해하는 글자조각으로 변환하여 비밀번호를 작성

사람이 작성한 비밀번호 : myPassword
컴퓨터가 입력하는 비밀번호 : 109 131 415 351 251 122 412 이런 식으로 숫자처리되어 비밀번호 생성

AES암호화가 숫자만 계산
'''
# 비밀번호압축최신()

# 랜덤 비밀번호를 생성해서 압축
# 압축 비밀번호 풀기

import random, string

def 비밀번호압축최신_랜덤():
    문자열 = string.ascii_letters + string.digits
    비밀번호 = "".join(random.choice(문자열) for _ in range(7))
    print(f"생성된 비밀번호 : {비밀번호}")
    with pyzipper.AESZipFile(
        '랜덤비밀번호파일.zip', 
        'w', 
        compression=pyzipper.ZIP_DEFLATED,     
        encryption=pyzipper.WZ_AES    
    ) as zf:                       
        zf.setpassword(비밀번호.encode()) 
        # zf.setpassword(b'hipassword') 
        zf.write('내정보_단일큐알.png') 
        # 생성된 비밀번호 : jZxpR38

# 비밀번호압축최신_랜덤()

# 특수문자를 포함하여 압축파일 비밀번호를 랜덤으로 생성 #"!@#$%^&*()"

def 비밀번호압축최신_랜덤_특수문자():
    문자열 = string.ascii_letters + string.digits + "!@#$%^&*()_+~"
    비밀번호 = "".join(random.choice(문자열) for _ in range(7))
    print(f"생성된 비밀번호 : {비밀번호}")
    with pyzipper.AESZipFile(
        '랜덤특수비밀번호파일1.zip', 
        'w', 
        compression=pyzipper.ZIP_DEFLATED,     
        encryption=pyzipper.WZ_AES    
    ) as zf:                       
        zf.setpassword(비밀번호.encode()) 
        # zf.setpassword(b'hipassword') 
        zf.write('내정보_단일큐알.png') 
        # 생성된 비밀번호 : jZxpR38

비밀번호압축최신_랜덤_특수문자()