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
            print(f"걸린시간 : {걸린시간:.2f}ch") # f"" = 문자열 형식 / :.2f = float = 소수점 몇번째

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
import zlib
def 숫자4자리찾기시도하기():
    zip파일이름 = '1_variable.zip'

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
                return # 비밀번호를 찾고 나면 이후 비밀번호로 압축파일 비밀번호 찾기 종료
        except (RuntimeError) : # 다수의 에러를 한번에 한 줄에서 처리할 때 ()를 이용해서 Error들을 , 로 구분하여 작성
            pass
        except Exception as e: # 단일 에러의 경우 () 생략 가능
            print("e: ",e)
            pass 

    print("비밀번호를 찾지 못했습니다.")

# 숫자4자리찾기시도하기()

'''

에러 메세지들은 틀린 비밀번호를 시도할 때 발생하는 정상적인 에러

1. ZIP파일의 비밀번호를 확인하는 과정
-> 코드에서 0000 비밀번호부터 입력
-> 입력 후 압축 해제 시도
-> 압축 해제를 시도하던 도중 코드가 너무 빠르게 돌아가서
   압축 해제를 하지 못한 비밀번호사 압축파일을 만지고 있는 상태에서
   압축을 또 해지하려하여 데이터 깨진 발생

e:  Error -3 while decompressing data: invalid block type
 -> 블록 타입이 잘못되었다
e:  Error -3 while decompressing data: invalid stored block lengths
 -> 압축 코드가 잘못되었다
e:  Error -3 while decompressing data: invalid code lengths set
 -> 압축 데이터가 잘못되었다

--> 비밀번호를 틀려서 해석을 하지 못한 결과가 각양각색 표출
    
 '''

'''


'''

def 범위지정찾기():
    최소길이 = 3
    최대길이 = 5
    zip파일 = "랜덤비밀번호파일.zip"
    문자들 = string.ascii_letters + string.digits # A-Z a-z 0-9
    print(f"비밀번호 찾기 시작 ({최소길이}~{최대길이}자리)")
    전체시작 = datetime.now()

    for 길이 in range(3, 6):
        경우의수 = len(문자들)
        print(f"{길이}자리 시도 중 (경우의 수 : {경우의수})")

        시작시간 = datetime.now()

        for 조합 in itertools.product(문자들, repeat=길이):
            비밀번호 = ''.join(조합)

            try:
                with pyzipper.AESZipFile(zip파일, 'r') as zf:
                    zf.setpassword(비밀번호.encode())
                    zf.testzip()
                    종료시간 = datetime.now()
                    전체시간 = (종료시간 - 전체시작).total_seconds()
                    print(f"비밀번호를 찾았습니다 : {비밀번호}")
                    print(f"총 걸린시간 : {전체시간:.2f}초")
                    return 비밀번호
            except:
                pass
        print("비밀번호를 찾을 수 없습니다.")
        return None
# 범위지정찾기()

def 범위지정찾기2탄():
    최소길이 = 3
    최대길이 = 9
    zip파일 = "랜덤비밀번호파일.zip"
    문자들 = string.ascii_letters + string.digits # A-Z a-z 0-9 조합하고자 하는 특수문자를 포함해서 작성 가능
    print(f"비밀번호 찾기 시작 ({최소길이}~{최대길이}자리)")
    전체시작 = datetime.now()
    for 길이 in range(최소길이, 최대길이): # 직접적으로 숫자를 작성하기보다는 변수 이름을 활용해서 개발자가 어떤 숫자인지 인지
        경우의수 = len(문자들)
        print(f"{길이}자리 시도 중 (경우의 수 : {경우의수})")
        시작시간 = datetime.now()
        시도횟수 = 0
        for 조합 in itertools.product(문자들, repeat=길이):
            비밀번호 = ''.join(조합)
            시도횟수 += 1
            try:
                with pyzipper.AESZipFile(zip파일, 'r') as zf:
                    zf.setpassword(비밀번호.encode())
                    zf.testzip()
                    종료시간 = datetime.now()
                    전체시간 = (종료시간 - 전체시작).total_seconds()
                    print(f"비밀번호를 찾았습니다 : {비밀번호}")
                    print(f"총 걸린시간 : {전체시간:.2f}초")
                    return 비밀번호
            except:
                print("시도횟수 : ", 시도횟수 ," === 경과시간 : ", (datetime.now() - 시작시간).total_seconds())
                pass # pass는 반드시 구문 내에서 맨 아래 위치해야한다. pass 이후 작성하는 코드는 사용되지 않음
                # print("A") pass 아래 같은 구문 내 코드 사용 불가
        print("비밀번호를 찾을 수 없습니다.")
        return None
# 범위지정찾기2탄()

'''
        문장에서 대문자~소문자 문자열로 가져오기               숫자들을 한글자씩 아니라 문자열로 가져오기
문자들 =       string.ascii_letters                   +            string.digits

itertools.product() = 가능한 모든 조합을 생성하는 기능
repeat = 길이 문자들을 모든 경우의 수를 조합해볼 것인데 몇 글자로 조합할 것인지 결정

for 조합 in itertools.product(문자들, repeat=길이):

with pyzipper.AESZipFile(zip파일, 'r') as zf:
암호화된 ZIP파일을 읽을 것 zf라는 명칭으로 대신 사용하겠다.
zf = pyzipper.AESZipFile(zip파일, 'r') 사용해도 됨

공간 명칭에 어떤 데이터를 넣을 것인지 작성하는 방법
개발자가_지정한_공간이름 = 데이터

with = 파일을 알아서 안전하게 열고 자동으로 닫기 기능이 담겨있는 속성

zf.setpassword(비밀번호.encode())
setpassword() = 암호화된 ZIP파일을 열 때 사용할 비밀번호를 설정하는 기능
비밀번호.encode() = 사람이 작성한 비밀번호를 컴퓨터가 읽을 수있는 비밀번호로 변환


zf.extractall()
-- ZIP 차일 안에 모든 파일을 디스크에 압축 해제
-- 압축에 존재하는 파일을 꺼내서 사용하고싶을 때 사용
--마치 ZIP파일 압축을 풀어 사용하는 척 하며 비밀번호 대입해보는 트릭
-- read나 testZip보다 압축풀기 까지 시도하기 때문에 속도가 느림


zf.read(zf.namelist()[0])
-- ZIP 파일 내부에 존재하는 특정 파일 하나만 읽어서 코드나 어딘가에서 사용하기 위한 용도
-- namelist()[0] = ZIP파일 안에 있는 파일들 중에서 첫번째 파일만 꺼내와서 사용하겠다
-- ZIP 파일 내부 파일을 꺼내서 사용하는 척 하며 비밀번호 해제 시도
-- extractall() 보다는 빠르지만, testZIP() 보다는 느림
-- namelist() ZIP파일 내부에 존재하는 모~든 파일 이름 리스트


zf.testzip()
-- 모든 파일이 손상되었는지 확인하며, 비밀번호가 맞는지도 확인하는 트릭
-- 손상의 유무만 보며, 압축을 풀려 하거나, 파일을 사용하는 척과 같은 행위를 하지 않기 때문에
-- 상대적으로 빠름 (상태가 좋은가 확인 후 다음 다음 다음으로 이동)

-- return 문자열
-- return None
-- return 숫자
   코드 구문을 수행 후, 수행에 대한 결과를 전달할 때 사용
   testZip() -- None 은 모든 파일이 정상임을 나타내는 표기법
   testZip() 파일이름 or 문자열 -- 해당 파일이 손상되었음을 나타내는 표기법

'''

def 범위지정찾기3탄():
    최소길이 = 5
    최대길이 = 9
    zip파일 = "랜덤비밀번호파일.zip"
    문자들 = string.ascii_letters + string.digits
    print(f"비밀번호 찾기 시작 ({최소길이}~{최대길이}자리)")
    전체시작 = datetime.now()
    for 길이 in range(최소길이, 최대길이):
        경우의수 = len(문자들)
        print(f"{길이}자리 시도 중 (경우의 수 : {경우의수})")
        시작시간 = datetime.now()
        시도횟수 = 0
        for 조합 in itertools.product(문자들, repeat=길이):
            비밀번호 = ''.join(조합)
            시도횟수 += 1
            try:
                with pyzipper.AESZipFile(zip파일, 'r') as zf:
                    zf.setpassword(비밀번호.encode())
                    zf.testzip()
                    종료시간 = datetime.now()
                    전체시간 = (종료시간 - 전체시작).total_seconds()
                    print(f"비밀번호를 찾았습니다 : {비밀번호}")
                    print(f"총 걸린시간 : {전체시간:.2f}초")
                    return 비밀번호
            except:
                print("시도횟수 : ", 시도횟수 ," === 경과시간 : ", (datetime.now() - 시작시간).total_seconds())
                pass # 
        print("비밀번호를 찾을 수 없습니다.")
        return None
범위지정찾기3탄()