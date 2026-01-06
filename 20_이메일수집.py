'''
pip install requests

already가 나오면 이미 설치가 되어있는 상태

'''

import re
import requests

# 1. 다음 뉴스 주소 하나를 가져온다.
주소 = "https://v.daum.net/v/20260106201833699"
headers = {'User-Agent':'Mozilla/5.0'}

# 웹페이지 접근 요청 측정 주소를 접근해서 데이터를 모두 가져옴
이메일요청 = requests.get(주소, headers=headers)
# [아이디]@[회사도메인].[최상위도메인]
이메일패턴 = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
이메일들 = re.findall(이메일패턴, 이메일요청.text) 
# findall = 정규식에 해당하는 모든 데이터를 찾아보기
# 문자열에서 글자 형식 데이터만 가져오겠다.

print(이메일들)

'''
[a-zA-Z0-9_.+-]+   @이 되기 전까지 대소문자숫자 _.+- 특수기호까지 한글자 이상 포함
@                  @
[a-zA-Z0-9-]+      회사도메인 주소는 대소문자 특수기호는 - 만 허용해서 한글자 이상 포함
\.                 \.   .을 단순 문자 . 로 사용하겠다
[a-zA-Z0-9-.]+     . 이후 국제적으로 사용 가능하도록 허용된 도메인에서 대소문자숫자 특수기호 -. 허용해서 한글자 이상 포함

'''
'''
import re
import requests

주소 = "https://v.daum.net/v/20260106201833699"
headers = {'User-Agent': 'Mozilla/5.0'}

이메일요청 = requests.get(주소, headers=headers)

# 이메일 정규식 패턴
이메일패턴 = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

이메일들 = re.findall(이메일패턴, 이메일요청.text)

print(이메일들)
정규식 설명 (간단)
[a-zA-Z0-9._%+-]+ : 이메일 ID

@ : 구분자

[a-zA-Z0-9.-]+ : 도메인

\.[a-zA-Z]{2,} : 최상위 도메인 (.com, .co.kr 등)
'''