'''
크롤링
웹사이트나 인터넷 상의 데이터를 자동을 ㅗ수집하는 기술
py 프로그램이 웹페이지를 방문해서
HTML 코드를 읽고, 그 안에 있는 텍스트, 링크 이미지 등의 정보를 추출하는 과정
마치 거미가 거미줄을 기어다니듯이 웹페이지들을 돌아다닌다고 해서 크롤링

가격비교 사이트에서 여러 쇼핑몰의 가격 정보를 수정할 때
데이터 분석이나 연구 목적으로 정보를 수집할 때
'''

'''
바탕화면에서 하든 어디에서 하든 상관 없이 파이썬 모듈 설치됨
설치된 모듈은 어디에서든 사용 가능
pip install selenium requests tqdm
# selenium : 가장 오래되고 유명한 도구
# 거의 모든 프로그래밍 언어와 브라우저를 지원하지만 설정이 복잡하고 속도가 다소 느린 편
# ChromeDriver와 함께 사용해야 하지만 ChromeDriver 설치 다소 번거러움

pip install playwright requests tqdm
# 마이크로소프트에서 만든 최신도구
# Selenium보다 훨씬 빠르고 별도의 드라이버 설치 불필요
# .sync_api = 동기방식 = 순서대로 차례차례 데이터를 가져올 때 사용
# requests : 브라우저를 띄우지 않고 서버에 데이터 줘! 직접적인 요청만 보냄
# tqdm : 데이터를 수천개 수집할 때 얼마나 진행됐는지 진행바를 보여주는 UI 도구
다운로드: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 76/76 [00:03<00:00, 20.36it/s]

데이터 수집하고 수집한 데이터를 다룰 때 json(키명칭-데이터값) 형태 많이 사용. csv 엑셀 형태
과제 : GPT를 활용하여 product_images 폴더에 이미지 저장하고 상품명, 가격 데이터를 json형태로 수집
'''

import os
import time
import requests
from playwright.sync_api import sync_playwright
from tqdm import tqdm

# 저장 폴더
SAVE_DIR = "images"
# 이미지 저장 폴더가 존재하지 않을 경우, images라는 폴더 생성
os.makedirs(SAVE_DIR, exist_ok=True)

URL = "도메인주소"

def download_image(url, filename):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    r = requests.get(url, headers=headers, timeout=15)
    with open(filename, "wb") as f:
        f.write(r.content)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        locale="ko-KR",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    )
    page = context.new_page()

    print("페이지 접속 중...")
    page.goto(URL, timeout=60000)
    page.wait_for_timeout(3000)

    # 스크롤로 상품 추가 로딩
    for _ in range(5):
        page.mouse.wheel(0, 3000)
        page.wait_for_timeout(2000)

    print("이미지 수집 중...")

    # Amazon 상품 이미지 selector
    img_elements = page.locator("img.s-image")
    count = img_elements.count()

    image_urls = []
    for i in range(count):
        src = img_elements.nth(i).get_attribute("src")
        if src and src.startswith("http"):
            image_urls.append(src)

    browser.close()

print(f"총 이미지 개수: {len(image_urls)}")

# 이미지 다운로드
# 다운로드라는 명칭으로 데이터 수집이 어디서부터 어디까지 되고 있는 것인지
# for 반복작업 횟수를 파악하여 % 표시
for idx, img_url in enumerate(tqdm(image_urls, desc="다운로드")):
    try:
        # 맨 끝에 작성된 확장자 png jpg를 보관
        ext = img_url.split("?")[0].split(".")[-1]
        #             어느 폴더에 저장할 것이고 / 저장할 때 파일이름 img_숫자1번. 부터 
        filename = f"{SAVE_DIR}/img_{idx+1}.{ext}"
        download_image(img_url, filename)
    except Exception as e:
        print("실패:", e)

print("모든 이미지 저장 완료!")
