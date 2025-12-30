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
'''
with zipfile.ZipFile("py_files.zip", 'w') as 압축파일:

with - 만들고자 하는 특정 파일을 열고 닫을 때 사용
       with는 필수는 아니지만 with를 사용하지 않을 경우
       마지막에 압축파일.close() 파일 닫기를 사용하여
       어디서부터 어디까지 파일을 압축해야 하는지 시작과 끝을 관리할 때 사용.

as 변수이름 - 앞에서 작성한 with zipfile.ZipFile("py_files.zip", 'w') 기능을       
             특정 변수 이름으로 사용하여 코드가 시작하고 종료될 때 까지 기능이나 데이터를 잠시 변수 이름으로 활용하겠다.

zipfile
    .ZipFile("파일이름.확장자이름", "파일사용방법") - 압축 파일을 전반적으로 다루는 클래스 (만들기/열기)
    .ZipInfo("파일이름.확장자이름")                - 압축한 파일의 정보를 확인하는 클래스
    .is_zipfile("파일이름.확장자이름")             - 압축 파일인지 확인하는 함수 true false 구분됨

'w' - write :새로 만들기 (기존 파일과 동일한 명칭.확장자 라면 덮어쓰기)
'r' - read : 읽기 모드 (파일이 없으면 에러 발생, 쓰는 기능 없음)
'a' - append : 추가하기 (기존 파일에서 내용 유지하고 뒤에 추가 / 없으면 에러)
'x' - exclusive create : 새로 만들기 (기존 파일과 동일한 명칭.확장가 가 존재한다면 에러 발생 / 무조건 파일.확장자 가 존재하기 않아야 한다)

write('파일이름.확장자') - () 안에 작성되어있는 파일이나 텍스트를 추가
extract('파일이름.확장자','특정폴더') - () 내에 작성되어있는 파일을 특정 폴더에 압축 해제
extractall() - 현재 폴더에 있는 압축파일을 전부 풀기
extractall('특정폴더') - 특정 폴더에 전부 풀기

이외 압축 파일의 파일 목록 보기
압축 내용 출력
파일 내용 읽기(압축 풀지 않고 미리보기)
파일 정보 가져오기
'''

def 압축하기기능():
    with zipfile.ZipFile("py_files.zip", 'w') as 압축파일:
        for f in os.listdir():
            if f.endswith('.py'):
                압축파일.write(f)
                print(f"{f} 압축 됨")

def png압축하기기능():
    # 확장자가 .png인 파일만 png_files.zip으로 압축하기
    with zipfile.ZipFile("png_files.zip", "w") as a: # 어떤 작업을 하고자 인지시키기 위해 반드지 w,r 과 같은 단어 작성해야 함
        for ff in os.listdir():
            
            if ff.endswith('.png'): # png 파일이 맞을 때 실행하는 구문들
                a.write(ff)
                
                print("==== png 파일이 맞습니다. 압축 파일에 추가했습니다. ====") # if문의 조건이 일치할 때 마다 프린트문을 실행하고 싶다면 현재 위치에 작성
            else:                   # png 파일이 아닐 때 실행하는 구문       
                print(ff,"png 파일이 아닙니다.")
            # if else에 관계 없이 ff 파일 하나가 png인지 아닌지 확인 완료됨을 표기하는 구문  
            print(ff,"파일은 png 파일이 아닙니다.")
        print("개발자님 압축 완료되었습니다, 알림 문구와 비슷한 효과를 가짐")           

# png압축하기기능()

# 현재는 close를 사용하지 않는다고 해서 문제가 되지는 않지만
# 파일과 코드가 길어지면 close를 사용해서 압축시작했다 압축 끝났다 에 대한 결과를 작성하지 않을 경우 에러 발생
# close() 명칭을 작성하지 않을 수 있으니
# with ~ as 압축파일 : 과 같은 형식을 사용하는 습관 들일 것!
def 파일확인():
    압축파일 = zipfile.ZipFile("all_file.zip", "w")

    for abc in os.listdir():
        if abc.endswith('.mp3'):
            압축파일.write(abc)
    print("파일 압축이 완료되었습니다.")

        #압축파일.close()

# 파일확인()

# 특정 파일을 선택하지 않고 모~~~든 현재 폴더에 존재하는 파일을 all_file.zip에 압축하기
# os.listdir() 현재 나의 폴더에 있는 모든 파일을 압축할 경우 if를 사용하지 않는다

# 자신의 현재 코딩을 진행하고 있는 python 코드 자체도 압축하려 했기 때문에 발생하는 에러
# 현재 실행중인 파이썬 파일은 제외하고 압축을 진행해야 한다
# 폴더 내에 존재하는 파일이 압축되는 순서는 이름 순
# .py로 되어있는 파일들의 파일 이름이 0부터 시작하는 숫자이기 때문에 다른 파일보다 먼저 압축되고 있는데
# 12번째에 존재하는 현재 파이썬 파일이 코딩중이기에 충돌이 일어나 압축이 되지 않는 상황
#gpt 들어가서 현재 작업하고 잇는 파일을 제외하고 압축할 수 있도록 코드를 수정해줘 요청
def 모두압축():
    with zipfile.ZipFile("all_file.zip", "w") as 파일:
        for fff in os.listdir():
            파일.write(fff)
        print("모든 파일이 압축되었습니다.")

# 모두압축()

'''
 os.path.basename = 현재 컴퓨터에서 내 파일과 fff에서 추가하고자 하는 파일이

 fff != os.path.basename(__file__)
 != 다르다면
 == 같가면 

'''
def 현재파일을_제외한_모든파일압축():
    현재파일 = os.path.basename(__file__)  # 실행 중인 파이썬 파일 이름
    압축파일명 = "all_file.zip"

    with zipfile.ZipFile(압축파일명, "w") as 파일:
        for fff in os.listdir():
            # 현재 실행 중인 파일과 zip 파일은 제외
            if fff in (현재파일, 압축파일명):
                continue # continue= 건너뛰고 다음 for문이나 작업을 실행

            if os.path.isfile(fff):  # 파일만 압축 (폴더 제외)
                파일.write(fff)

    print("모든 파일이 압축되었습니다.")

# 현재파일을_제외한_모든파일압축()

# 현재 실행중인 파일을 파일 내에서 제어하거나 작동하려는 경우 멈추는 문제 발생

# 현재 파일은 건너뛰고를 주로 사용
# != else에 해당하는 구문을 주로 작성
# if 문이 사실상 필요하지 않고, if else를 위해서 if else를 작성해야 할 때는
# if 내부에 != 를 써서 else 구분에 해당하는 결과가 사실이라면 if에 해당하는 기능을 실행하겠다.
def 느낌표표기기능():
    with zipfile.ZipFile("all_file.zip", "w") as 파일:
        for fff in os.listdir():
            if( fff == os.path.basename(__file__) ):
                print("현재 실행중인 파일이므로 압축에서 제외합니다.")
            else:
                # 파일.write(fff)
                파일.write(fff, os.path.basename(__file__))
                print("현재 실행중인 파일이 아니므로 압축에 추가합니다.")
느낌표표기기능()                


# 폴더에서 전체 드래그를 해서 압축하는 방법은
# 폴더에서 실행하는 파일이 존재하지 않을 때
# 주로 외부 폴더에 존재하는 파일들을 압축할 때 많이 사용
# 아무리 실행버튼을 눌러도 실행이 되지 않는 경우 현재 코드에 문제가 생겨 무한루프 발생
# 껐다 키거나 터미널 창에서 ctrl + c를 열심히 누른다
# 터미널창에서 ctrl + c 는 현재 실행중인 작업 취소
            