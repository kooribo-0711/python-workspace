'''
pip install beautifulsoup4
'''
import requests
from bs4 import BeautifulSoup
# 네이버에 접속 우 네이버에 있는 글자데이터 가져오기
# 네이버는 외부 개발자가 접속해서 데이터 가져오기 차단한 상태
url="https://search.naver.com/search.naver?query=오늘의명언"
soup = BeautifulSoup(requests.get(url).text, 'html.parser')
print(soup.find('p', calss_="ingkr").text)