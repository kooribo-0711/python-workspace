'''
변수(=Variable)
값을 저장해 두는 이름표가 붙은 상자

타 언어는 상자가 어떤 상자인지 맨 앞에 작성
이 상자는 숫자만 들어갈 수 있는 상자입니다.

int   a=1;  a 상자에는 숫자 값만 들어갈 수 있습니다.
String b = "문자들" b 상자에는 문자값만 들어갈 수 있습니다.

파이썬의 경우 상자에 어떤 값만 들어갈 수 있는지 지정하지 않음!
파이썬이 한 줄씩 코드를 해석하며 자동으로 처리해 줌

개발자가 개발하는데 있어 편의 우선
변수 이름 지정할 때 규칙
맨 앞 글자로 숫자가 들어가면 안되고, 변수 이름 사이에 띄어쓰기 존재해선 안 됨.
'''

# 가정 : 회사를 소개하는 주소 작성 

print("https://www.google.com")
print("Search Website : https://www.google.com")
print("My Home Page Website : https://www.google.com")

# 회사에 투자를 받아 검색하는 홈페이지를 변경

print("https://www.naver.com")
print("Search Website : https://www.naver.com")
print("My Home Page Website : https://www.naver.com")

# 동일한 데이터를 여러 번 작성하고, 관리해야 할 때 변수 이름에 데이터를 담아 손쉽게 관리할 수 있다.
website = "https://www.naver.com" # website 라는 공간에는 "https://www.naver.com" 명칭이 담겨져 있는 것.

print(website)
print("Search Website : ", website)
print("My Home Page Website : ", website)

# 우리 회사가 주소 소개를 변경할 때 마다 일일이 하나하나 검색해서 변경하는 것이 아니라
# website 라는 변수 이름에 담겨진 주소만 변경하면 됨