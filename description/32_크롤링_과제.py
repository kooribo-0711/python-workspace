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
      Tip : 아래 코드로 이미지가 잘 수집되었음을 언급하며 아래 코드 그대로 프롬프트에 넣고,
            원하는 요청을프롬프트에 작성하여 상품명과 가격데이터, 이미지를 json 형태로 저장하는 코드 요청

지마켓 / 무신사 / 자라 등 원하는 웹사이트 이미지 가격 설명을 수집해오는 명령도 진행해보기
'''
import os
import time
import json
import requests
from playwright.sync_api import sync_playwright
from tqdm import tqdm

# =========================
# 기본 설정
# =========================
SAVE_DIR = "images"
JSON_FILE = "products.json"
URL = "도메인주소"

os.makedirs(SAVE_DIR, exist_ok=True)

# =========================
# 이미지 다운로드 함수
# =========================
def download_image(url, filename):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    r = requests.get(url, headers=headers, timeout=15)
    with open(filename, "wb") as f:
        f.write(r.content)

# =========================
# Playwright 크롤링
# =========================
products = []

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

    print("상품 데이터 수집 중...")

    # 상품 카드 selector
    items = page.locator("div.s-result-item[data-component-type='s-search-result']")
    count = items.count()

    for i in range(count):
        item = items.nth(i)

        # ---------- 상품명 ----------
        title = None
        title_locator = item.locator("h2 span")
        if title_locator.count() > 0:
            title = title_locator.first.text_content().strip()

        # ---------- 이미지 ----------
        image_url = None
        image_locator = item.locator("img.s-image")
        if image_locator.count() > 0:
            image_url = image_locator.first.get_attribute("src")

        # ---------- 가격 ----------
        price = None

        # 1순위: a-offscreen (가장 정확)
        offscreen_locator = item.locator("span.a-offscreen")

        if offscreen_locator.count() > 0:
            price = offscreen_locator.first.text_content().strip()

        else:
            # 2순위: whole + fraction
            whole_locator = item.locator("span.a-price-whole")
            fraction_locator = item.locator("span.a-price-fraction")

            if whole_locator.count() > 0:
                whole = whole_locator.first.text_content().strip()

                if fraction_locator.count() > 0:
                    fraction = fraction_locator.first.text_content().strip()
                    price = f"${whole}{fraction}"
                else:
                    # fraction 없는 경우
                    price = f"${whole}"


        # ---------- 저장 ----------
        if title and image_url:
            products.append({
                "title": title,
                "price": price,
                "image_url": image_url
            })

            
    browser.close()

print(f"총 수집된 상품 수: {len(products)}")

# =========================
# 이미지 다운로드
# =========================
for idx, product in enumerate(tqdm(products, desc="이미지 다운로드")):
    try:
        img_url = product["image_url"]
        ext = img_url.split("?")[0].split(".")[-1]
        filename = f"{SAVE_DIR}/img_{idx+1}.{ext}"
        download_image(img_url, filename)

        # JSON에 로컬 이미지 경로 추가
        product["local_image"] = filename
    except Exception as e:
        print("이미지 다운로드 실패:", e)

# =========================
# JSON 저장
# =========================
with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print("모든 데이터 저장 완료!")
