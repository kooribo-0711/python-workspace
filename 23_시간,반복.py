'''
1. from datetime import datetime
파이썬에서 날짜 시간을 다루는 도구 / 타 언어에서도 dateTime과 비슷한 명칭으로 시간을 다루는 도구 존재
사람이 읽을 수 있는 연, 월, 일, 시, 분, 초, 마이크로초까지 표현 가능

주요 기능들(=메서드 함수 안에 포함되어있는 개념 .기능명칭()과 같은 형태로 사용 가능)
datetime.now() = 현재 시간
datetime.todㅁy() = 현재 시간+날짜
datetime.strftime("%Y-%m-%d %H:%M:%S")
datetime.strftime("2026-01-12 19:11:39")
컴퓨터가 출력하는 날짜를 개발자나 회사가 보여주기 원하는 형태의 문자열로 변경해서 출력
strftime() =str(String)f(format)time() = 시간을 개발자가 원하는 형식 포맷으로 변환하여 문자열로 출력.


%Y = 연도
%m = 월 (m은 month나 minute과 착각할 수 있어서 하나는 대문자M 하나는 소문자m으로 사용)
   = 타 언어에서는 월을 표현하는 단어로 M을 사용하지만, 파이썬에서는 소문자 m 형태를 사용
%d = 일
%H = 시간 ; 24시간 기준
%M = 분
%S = 초

%H 와 같은 형태로 한 글자만 작성해주면 22시 2시 4시와 같이 원하는 날짜의 시간을 확인할 수 있다.
%HH -> 와 같은 형태 작성 X


주요 속성들
.now().year = 년
.now().month = 월
.now().day = 일
.now().weekday() = 요일(월요일 = 0, 일요일 = 6)
.now()

datetime(년, 월, 일, 시, 분, 초, 마이크로초)

'''
from datetime import datetime
def 현재_시간_확인하기() :
    시작시간 = datetime.now()
    print("시작시간 : ",시작시간) #시작시간 :  2026-01-12 19:18:30.889829

def 시작시간_종료시간_확인하기():
    시작 = datetime.now()

    for i in range(6):
        print("i의 번호 : ", i)

    종료 = datetime.now()

    걸린시간 = (종료 - 시작).total_seconds() # 초 단위로 계산

    print(f"{걸린시간}초 걸렸습니다.")

# 시작시간_종료시간_확인하기()

'''
import itertools

반복(iteration) : 조합/순열/카운트/필터링 과 같은 반복을 깔끔하고 빠르게 처리할 때 자주 사용
 반복을 효율적으로 다루기 위한 표준 라이브러리
 for 문을 여러 겹 대신 한줄 표현 가능
 itertools는 속성은 거의 없고, 함수(function) 기능들이 주로 존재
 
'''
import itertools

def 조합위치():
    a= itertools.product('abc',repeat=2)
    print("a : ", a) # <itertools.product object at 0x000001FBE386A740>
    # 파이썬에서 특정 코드가 모여있는 파일을 실행했을 때,
    # a라는 데이터 저장공간의 위치 출력한 것
    # 파일 실행이 종료되면 a 위치는 사라지고 다음에 다시 실행할 때 컴퓨터에서 랜덤위치로 실행이 된다

def 모든조합생성():
    for 조합 in itertools.product('abc',repeat=2):
        print(''.join(조합)) 
'''
itertools.product() = 모든 조합 생성하는 기능
조합이 될 문장이나 단어, 숫자 등 조합해야 할 모든 문자를 작성                      몇자리 조합으로 구성하는지 설정
itertools.product('조합이 될 문장이나 단어, 숫자 등 조합해야 할 모든 문자를 작성', repeat=2):

aa
ab
ac
ba
bb
bc
ca
cb
cc
'''
# 모든조합생성()

def 모든_세자리_조합_생성():
    for 조합 in itertools.product('abc01',repeat=3):
        print(''.join(조합)) 
'''
aaa
aab
aac
aa0
aa1
aba
abb
abc
ab0
ab1
aca
acb
acc
ac0
ac1
a0a
a0b
a0c
a00
a01
a1a
a1b
a1c
a10
a11
baa
bab
bac
ba0
ba1
bba
bbb
bbc
bb0
bb1
bca
bcb
bcc
bc0
bc1
b0a
b0b
b0c
b00
b01
b1a
b1b
b1c
b10
b11
caa
cab
cac
ca0
ca1
cba
cbb
cbc
cb0
cb1
cca
ccb
ccc
cc0
cc1
c0a
c0b
c0c
c00
c01
c1a
c1b
c1c
c10
c11
0aa
0ab
0ac
0a0
0a1
0ba
0bb
0bc
0b0
0b1
0ca
0cb
0cc
0c0
0c1
00a
00b
00c
000
001
01a
01b
01c
010
011
1aa
1ab
1ac
1a0
1a1
1ba
1bb
1bc
1b0
1b1
1ca
1cb
1cc
1c0
1c1
10a
10b
10c
100
101
11a
11b
11c
110
111
'''
# 모든_세자리_조합_생성()

'''
continue = 특정 단어이거나 상태일 때 아래 코드를 건너뛰고 다음 반복을 이어서 진행하기



'''

def 특정_데이터_건너뛰기():
    for i in range(10):
        if i == 5: # 만약 0~9 반복할 때 i에 들어있는 데이터가 숫자 5 라면 print문을 통하지 않고, 6번부터 진행하기
            continue # 5일 때는 아래 코드를 건너뛰고 다음 번호 진행
        print("i = ",i)

def 특정_길이_데이터확인():
    for i in range(10): #0~9까지 
        # i = 숫자 데이터를
        # str(숫자나 데이터가 들어있는 공간의 명칭 작성)
        # str(i) = 숫자 양 없에 ""나 ''를 붙여주는 것 처럼 문자열로 생성
        print(str(i).zfill(4))
        '''

            .zfill(4) = 문자열 데이터에서 지정한 길이만큼 데이터가 존재하지 않을 때 0 숫자로 앞을 채워 지정한 길이로 만듦
            0000
            0001
            0002
            0003
            0004
            0005
            0006
            0007
            0008
            0009
            
            예를 들어
            "미소".zfill(3) = 0미소 형태로 출력형태가 무조건 3자리가 될 수 있도록 문자열 앞에 부족한 자릿수 만큼 0 채움
            -> 비밀번호 4자리 조합할때 0000~0100 까지 확인하는 용도
            

            int = 숫자에서 사용 불가. 오직 str 문자열 데이터에서만 사용 가능
            print(i.zfill(4))
            ^^^^^^^
            AttributeError: 'int' object has no attribute 'zfill'
        '''

# 특정_길이_데이터확인()

def 특정자리_특정길이_데이터확인():
    시작 = datetime.now()
    for 번호 in range(10000):
        비밀번호 = str(번호).zfill(4)
        print(f"비밀번호 : {비밀번호}")
    종료 = datetime.now()

    걸린시간 = (종료 - 시작).total_seconds()
    print(f"{걸린시간}초 걸렸습니다.")

# 특정자리_특정길이_데이터확인()

