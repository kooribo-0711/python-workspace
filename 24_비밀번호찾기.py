import pyzipper, zipfile, string, itertools
from datetime import datetime

def 숫자4자리찾기():
    zip파일이름 = '랜덤비밀번호파일.zip'

    print("숫자 비밀번호 찾기를 시작합니다.")
    시작시간 = datetime.now()

    #0000~9999까지 모두 시도
    for 번호 in range(10000):
        비밀번호 = str(번호).zfill(4)


        # 비밀번호를 찾을 때 
        # with zipfile.ZipFile(zip파일이름,'r') as zf: -> 고전적인 비밀번호 형태 / 오래된 버전 코드 제안
        with pyzipper.AESZipFile(zip파일이름) as zf:
            # zf.extractall(pwd=비밀번호.encode()) = 아래 19,20 문장을 한번에 작성한 것. 컴퓨터가 읽을 수 있는 형태로 변환
            zf.pwd=비밀번호.encode()
            zf.extractall() # zip파일 안에 들어있는 모든 파일을한꺼번에 풀어주는 기능 -> 폴더로 전부 꺼내는 버튼 
            '''
            압축 비밀번호를 풀 때 비밀번호가 틀리면
            Bad Password / compression Error / Bad CRC와 같은 에러 발생
            애러가 발생했을 때는 넘기며 정답을 맞출 때 까지 코드 수행

            try - except 사용
            '''
            종료시간 = datetime.now()
            걸린시간 = (종료시간 - 시작시간).total_seconds()
            print("비밀번호를 찾았습니다. : ", 비밀번호)
            print(f"걸린시간 : {걸린시간:.2f}ch") # f"" = 문자열 형식 / :.2f = float = 수수점 몇번째

    print("비밀번호를 찾기 못했습니다.")

# 숫자4자리찾기()

'''
try : 문제가 발생할 수 있는 모든 코드 실행

except : 개발자가 예상하는 에러 1 # 비밀번호가 틀리는 문제가 발생했을 때
    특정 문제가 발생했을 때 수행할 작동 작성 # 프로그램이 종료되지 않고, 어떻게 대처할 수 있을지 작성

except : 개발자가 예상하는 에러 2
    특정 문제가 발생했을 때 수행할 작동 작성

except : 개발자가 예상 못하는 에러 # 개발자가 예상하지 못하는 문제가 발생했을 때
    특정 문제가 발생했을 때 수행할 작동 작성 # 프로그램을 강제로 종료하거나, 모든 예외에 프로그램을 종료하지 않고 대처하는 방법 작성

try는 하나지만 except는 1개 이상 작성 가능
'''

def 숫자4자리찾기시도하기():
    zip파일이름 = '랜덤비밀번호파일.zip'

    print("숫자 비밀번호 찾기를 시작합니다.")
    시작시간 = datetime.now()
    for 번호 in range(10000):
        비밀번호 = str(번호).zfill(4)
        try:
            with pyzipper.AESZipFile(zip파일이름) as zf:
                zf.pwd=비밀번호.encode()
                # zf.extractall()  
                zf.read(zf.namelist()[0])
                종료시간 = datetime.now()
                걸린시간 = (종료시간 - 시작시간).total_seconds()
                print("비밀번호를 찾았습니다. : ", 비밀번호)
                print(f"걸린시간 : {걸린시간:.2f}초")
        except (RuntimeError, pyzipper.zipfile.BadZipFile, OSError, ValueError) :
            # continue
            pass # 비밀번호를 틀리면 조용히 다음 시도

    print("비밀번호를 찾지 못했습니다.")

숫자4자리찾기시도하기()