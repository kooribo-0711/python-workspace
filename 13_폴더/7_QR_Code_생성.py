'''
파이썬에는 pip 명령어가 존재

pip = 파이썬에서 다른 개발자나 회사에서 만든 기능을 다운받아 나의 개발에 활용할 때 사용하는 도구
pip = 앱스토어와 비슷한개념. 파이썬에서 필요한 기능을 다운

prcode
- QR코드를 만들어주는 라이브러리
- 글자나 링크 등을 QR코드 이미지로 바꿔줌

[pil]
- 이미지를 저장하기 위한 기능
- QR코드를 png, jpg 이미지로 저장하기 위해 필요

앱스토어처럼 필요한 도구를 설치하는 방법
pip install 도구이름

설치한 도구를 삭제하는 방법
pip uninstall 도구이름

설치
pip install qrcode[pil]

삭제
pip uninstall qrcode[pil]
'''
# pip install로 설치한 qrcode라는 기능을 현재 코드를 작성하는 페이지에서 기능을 잠시 호출하여 사용하겠다.
'''
가져오다  가져올기능이름
import      qrcode

'''
import qrcode 

url = "https://www.naver.com"
큐알생성이미지 = qrcode.make(url)
큐알생성이미지.save('naver_QR.png')
print("큐알 생성 이미지 만들기를 완료했습니다.")

'''
필요한 파이썬 기능을 검색하여 설치 명령어를 확인할 수 있는 주소 
https://pypi.org/project/qrcode/
특정 기능에 관련되어 다른 개발자나 회사가 만든 기능을 활용하고자 하나
단어나 키워드에 대한 시작점을 찾지 못하겠다면
AI 검색을 활용하여 우리가 원하는 개발에 도달할 수 있도록 검색해보는 것 또한 좋은 방법
'''