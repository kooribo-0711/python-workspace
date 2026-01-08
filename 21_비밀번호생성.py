'''
import random : 무작위 랜덤 값을 생성하는 모듈을 불러옴

import string : 문자열 관련 상수들을 제공하는 모듈을 불러옴

모듈(Module)
- 파이썬에서 파일 하나(.py)를 의미
- 함수, 클래스, 변수 등을 담고 있는 단일 파일
- 파일이름.py 로 만들어진 코드 모음을 모듈이라고 함
- import random은 random.py 형태로 만들어진 파일 하나
- 책 한 권
- 건축/공학 관련 용어 modules = 작은 단위
- 건축에서 조립식 모듈 같은 독립적인 부품 의미
- 독립적으로 작동하는 코드 덩어리


라이브러리
- 여러 모듈을 모아둔 패키지(폴더)
- 더 큰 개념으로 여러 모듈들의 집합
- 현재 우리의 파일 기준으로는 python_workspace가 라이브러리 명칭
- 여러 책을 모아둔 도서관
- 마치 도서관에서 필요한 책을 꺼내 주요 분야의 정보를 얻고 활용하는 것 처럼 필요한 코드를 꺼내쓴다는 의미

변수 : variavle
- 수학용어에서 유래
- x, y같은 변하는 수를 variable 변수라 한다
- 초기 프로그래머들은 수학자가 많아서 수학용어를 그대로 사용하는 경우 많음.

상수 : constant
- 수학에서 pi나 e 같이 고정된 값을 constant라고 부름. 프로그램에서도 그래도 사용

string = 처음부터 컴퓨터를 만들 때 존재하던 개념이 아님
char = 문자 한글자 한글자 씩 메모리 저장
컴퓨터 메모리 용량이 좋아지며 단어, 문장 단위로 보관
charcharchar.... 문자를 나열한다 -> string 명칭 사용

String 다양한 종류의 상수 존재

String.py
    - ascii-letters  = 영문자 대소문자 모음 (a-z, A-Z 총 52개) 정규식을 모아놓은 상수
                     = String을 만든 파이썬 개발자가 String에서 ascii letters를 사용할 때 영문 대소문자 모음으로 사용하겠다 작성
                       다른 사람들이 String.ascii-letters를 인위적으로 변경할 수 없도록 선언하여 만듦

    - digits = 숫자를 나열해놓은 데이터 공간의 명칭.
             = 마찬가지로 다른 개발자는 string.digits 사용가능하나 공간 내부의 데이터는 변경 불가

    - .join() = "".join(...) : 특정 문자열로 내부 데이터를 이어붙임   


'''

# import는 각 모듈이나 라이브러리 최초 1회만 가져오기하면 여러번 사용 가능
'''
import random, string은

import random
import string

으로 작성한 것과 같은 효과를 가짐

import random.py string.py
기본적으로 있어야 하지만 메모리 크기가 상대적으로 크며, 모든 개발자들이 모두 사용하지 않을 모듈이기 때문에
필요한 개발자는 import = 불러오기 형태로 사용
'''

import random, string
문자들 = string.ascii_letters

def 문자_랜덤_생성기() : # 보통 개발자들은 의미없는 띄어쓰기 또한 메모리라 여겨 (): 붙여서 사용하는 개발자 존재
    # 문자들이라는 데이터 변경 가능한 공간 명칭에는 문자열.영문자대소문자(=영어문자나열) 이 들어있다
    문자들 = string.ascii_letters
    print(f"문자들 : {문자들}") # 문자들 : abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    # "".join("문자들이나 숫자들 문자 + 숫자 등 1개 이상의 데이터들")
    #    모두 한 줄로 문자열로 모아놓겠다
    #    각 다르게 존재하는 문자들을 "" 문자열 형태로 구분하겠다
    # "" or '' = 아무것도 구분하지 않고 이어서 작성한다는 의미
    '''
    random = 랜덤으로
    .choice(문자들) = 문자들 중에서 하나를 선택하는 기능(=random 내부에 만들어진 기능 = method)
    '''
    비밀번호 = "".join(random.choice(문자들)) # 여기서는 "".join()이 사실 필요가 없음 왜냐하면 문자 하나..이고 이을 문자가 없기 때문
    print(f"랜덤 비밀번호 : {비밀번호}")

# 문자_랜덤_생성기()

def 문자_이어붙이기() : 
    문자들 = string.ascii_letters
    print(f"문자들 : {문자들}")
    '''
    랜덤문자1번 = random.choice(문자들)
    랜덤문자2번 = random.choice(문자들)
    랜덤문자3번 = random.choice(문자들)
    랜덤문자4번 = random.choice(문자들)
    랜덤으로만들어진문자들 = 랜덤문자1번 + 랜덤문자2번 + 랜덤문자3번 + 랜덤문자4번
    문자들을 반복해서 출력하고, 알아서 이어붙어 작성되도록 할 수 있는 방법 없을까?
    '''
    # 랜덤으로만들어진문자를 담을 데이턱밧이 변경해도 되는 공간 생성
    랜덤으로만들어진문자들 = []
    # 반복문인 for 문의 규칙
    # for 데이터_하나_담을_공간의명칭 in 반복방법 :
    # 아래와 같이 변수공간이라는 명칭이 의미 없을 경우 규칙만 맞게 처리하는 방법
    # for 변수공간 in range(4): 
    # _ = 규칙에 맞게 만들어놓은 변수이름일 뿐 의미 없다.

    for _ in range(4): # '_'는 코드 기능에 특정 규칙은 존재하여 규칙에 맞도록 작성만 하는 형태
        #  랜덤문자 = random.choice([abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ])
        랜덤문자 = random.choice(문자들)
        랜덤으로만들어진문자들 += 랜덤문자  # += 계속 이어서 추가하기   

    print(f"랜덤으로만들어진문자들 : {랜덤으로만들어진문자들}") # 랜덤으로만들어진문자들 : ['w', 'S', 'n', 'c']

# 문자_이어붙이기()


def 조인_1번():
    a="안녕"
    b="하세요"
    결과="".join((a,b))
    print(f"결과:{결과}")

# 조인_1번()

def 조인_2번():
    a="안녕"
    b="하세요"
    결과="===".join((a,b))
    print(f"결과:{결과}")

# 조인_2번()

def 조인_3번():
    a="안녕"
    b="하세요"
    c="환영합니다"
    결과="===".join((a,b,c))
    print(f"결과:{결과}")

# 조인_3번()

def 조인_4번():
    a=random.choice(문자들)
    b=random.choice(문자들)
    c=random.choice(문자들)
    결과="===".join((a,b,c))
    print(f"결과:{결과}")

# 조인_4번()

# 조인 5번 생성 후 for문을 이용해서 조인을 사용하지 않고 결과 = [] 공간에 for 문으로 출력된 랜덤 영문을 5글자 담은 후 출력하여 결과 확인
def 조인_5번():
    결과 = []
    for _ in range(5) : 
        a=random.choice(문자들)
        결과 += a
    print(f"결과:{결과}")

# 조인_5번()

def 조인_6번():
    #               구분없이 이어붙이겟다       문자들에서랜덤으로선택된문자를            총 0~4 5글자 출력하여  - 해석순은 뒤에서부터
    #                                                                                 for _ in range(5)  - 반복하겠다 0에서 4까지 
    #                                          random.choice(문자들)                   for _ in range(5)  - 랜덤으로 문자 한 글자 뽑기를
    #                                         (random.choice(문자들)                   for _ in range(5)) - () 내부 문자 안에서만
    #                "".join                  (random.choice(문자들)                   for _ in range(5)) - 0~4번 총 5글자를  이어붙이겠다
    # 영희_비밀번호 = "".join                  (random.choice(문자들)                   for _ in range(5)) - 영희_비밀번호에 저장
    영희_비밀번호 = "".join(random.choice(문자들) for _ in range(5))
    print(f"결과 : {영희_비밀번호}")

# 조인_6번()
#                  대소영문자              숫자
문자들2탄 = string.ascii_letters + string.digits
# print(f"문자들 2탄 : {문자들2탄}") # 문자들 2탄 : abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789

소문자들 = string.ascii_lowercase # 소문자들 : abcdefghijklmnopqrstuvwxyz
# print(f"소문자들 : {소문자들}")

대문자들 = string.ascii_uppercase # 대문자들 : ABCDEFGHIJKLMNOPQRSTUVWXYZ
# print(f"대문자들 : {대문자들}")

def 문자숫자_암호생성기():
    문자들 = string.ascii_letters + string.digits + "!@#$%^&*()"
    비밀번호 = "".join(random.choice(문자들) for _ in range(7))
    print(f"랜덤 비밀번호 : {비밀번호}")
# 랜덤이라 한들 선택이 먼저되는 문자들이 존재 알고리즘 상에서 우선 선택적이 되는 문자들이 존재 

문자숫자_암호생성기()

#압축