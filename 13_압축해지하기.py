import zipfile

def 파이썬압축해제():
    with zipfile.ZipFile("py_files.zip","r") as z:
        z.extractall('13_폴더')
    print("압축 해제 완료되었습니다.")

# 컴퓨터의 기본개념
# 폴더를 삭제할 때 폴더 내의 파일을 어딘가에서 사용중이라면
# 폴더 삭제 중지하는 것 처럼 컴퓨터는 문제를 최소화 하기 위해
# 실행중인 파일은 이중으로 건들지 않는다.

# png_files.zip
# 13_폴더에 png_files.zip 압축 해제 하기.
# 압축 해제의 경우, 파일에 데이터를 추가하는 개념이 아니라
# 파일을 읽는 모드이기 때문에 r(read) 사용

def png압축해제():
    with zipfile.ZipFile("png_files.zip","r") as k:
        k.extractall('13_폴더')
    print("png 압축 해제 되었습니다.")

# png압축해제()

import os

# 폴더가 없는데 압축을 푼다 하면
# 폴더가 존재하지 않는다 에러 발생 하므로
# 반드시 폴더를 생성한 다음에 폴더 내에 압축 해제
def zip파일명칭으로압축풀기(zip파일명, 폴더명):
    if not os.path.exists(폴더명):
        os.makedirs(폴더명)
    with zipfile.ZipFile(zip파일명, "r") as k:
         k.extractall(폴더명)

zip파일명칭으로압축풀기("png_files.zip", "png_files")

def zip파일명칭으로압축풀기_2탄(zip파일명):
    if not os.path.exists(zip파일명):
        os.makedirs(zip파일명)
    with zipfile.ZipFile(zip파일명+".zip","r") as k:
         k.extractall(zip파일명)

zip파일명칭으로압축풀기_2탄("png_files")         