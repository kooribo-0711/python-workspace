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
import json
from playwright.sync_api import sync_playwright

# =========================
# 기본 설정
# =========================
JSON_FILE = "musinsa_products.json"
URL = "https://www.musinsa.com/main/musinsa/sale?gf=A"

products = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # 구조 확인용
    context = browser.new_context(
        locale="ko-KR",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    )
    page = context.new_page()

    print("페이지 접속 중...")
    page.goto(URL, timeout=60000)
    page.wait_for_timeout(5000)

    # 스크롤 (캐러셀 데이터 로딩)
    for _ in range(6):
        page.mouse.wheel(0, 4000)
        page.wait_for_timeout(2000)

    print("상품 데이터 수집 중...")

    # =========================
    # 🔴 여기부터가 핵심 수정 부분
    # =========================
    items = page.locator('div[data-mds="ListInfoItem"]')
    count = items.count()
    print("감지된 상품 수:", count)

    for i in range(count):
        item = items.nth(i)

        # ---------- 브랜드 ----------
        brand = None
        brand_locator = item.locator('p.text-etc_11px_semibold')
        if brand_locator.count() > 0:
            brand = brand_locator.first.text_content().strip()

        # ---------- 상품명 ----------
        title = None
        title_locator = item.locator('p.text-body_13px_reg')
        if title_locator.count() > 0:
            title = title_locator.first.text_content().strip()

        # ---------- 가격 ----------
        price = None
        price_locator = item.locator('span.text-black')
        if price_locator.count() > 0:
            price = price_locator.first.text_content().strip()

        if title:
            products.append({
                "brand": brand,
                "title": title,
                "price": price
            })

    browser.close()

# =========================
# JSON 저장
# =========================
with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print(f"총 저장된 상품 수: {len(products)}")
print("모든 데이터 저장 완료!")
