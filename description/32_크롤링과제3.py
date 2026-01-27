import os
import time
import json
import requests
from playwright.sync_api import sync_playwright
from tqdm import tqdm

# =========================
# 기본 설정
# =========================
SAVE_DIR = "musinsa_images"
JSON_FILE = "musinsa_products.json"
URL = "https://www.musinsa.com/main/musinsa/ranking?gf=A&storeCode=musinsa&sectionId=200&contentsId=&categoryCode=000&ageBand=AGE_BAND_ALL"

os.makedirs(SAVE_DIR, exist_ok=True)

# =========================
# 이미지 다운로드 함수
# =========================
def download_image(url, filename):
    """이미지를 다운로드하여 파일로 저장"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.musinsa.com/"
    }
    try:
        # https:// 없는 경우 추가
        if url.startswith('//'):
            url = 'https:' + url
        
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        with open(filename, "wb") as f:
            f.write(r.content)
        return True
    except Exception as e:
        print(f"다운로드 실패 ({url}): {e}")
        return False

# =========================
# Playwright 크롤링
# =========================
products = []

print("=" * 50)
print("무신사 상품 이미지 크롤러 시작")
print("=" * 50)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # 디버깅을 위해 headless=False
    context = browser.new_context(
        locale="ko-KR",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    page = context.new_page()

    print(f"\n페이지 접속 중: {URL}")
    page.goto(URL, timeout=60000)
    
    # 페이지 로딩 대기
    print("페이지 로딩 대기 중...")
    page.wait_for_timeout(5000)

    # 스크롤하여 더 많은 상품 로드
    print("스크롤하여 상품 추가 로딩 중...")
    for i in range(10): # 스크롤을 몇번째 까지 진행할 것인지
        page.mouse.wheel(0, 3000)
        page.wait_for_timeout(1500)
        print(f"  스크롤 {i+1}/10 완료")

    print("\n상품 데이터 수집 중...")

    # 무신사 상품 카드 선택자 (data-item-id 속성으로 식별)
    selector = "div.gtm-view-item-list[data-item-id]"
    
    items = page.locator(selector)
    count = items.count()
    
    if count > 0:
        print(f"'{selector}' 선택자로 {count}개 상품 발견!")
    else:
        print("상품을 찾을 수 없습니다.")
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(page.content())
        print("page_source.html 파일에 HTML이 저장되었습니다.")
        browser.close()
        exit()
    
    
    for i in tqdm(range(count), desc="상품 수집"):
        item = items.nth(i)

        try:
            # data-item-id로 상품 ID 가져오기
            item_id = item.get_attribute("data-item-id")
            
            # 브랜드명 (a 태그 내의 p 태그)
            brand = None
            try:
                brand_elem = item.locator("a.gtm-click-brand p")
                if brand_elem.count() > 0:
                    brand = brand_elem.first.text_content().strip()
            except:
                pass

            # 상품명 (브랜드 다음의 a 태그 내 p 태그)
            title = None
            try:
                title_elem = item.locator("a.gtm-select-item p.line-clamp-2")
                if title_elem.count() > 0:
                    title = title_elem.first.text_content().strip()
            except:
                pass

            # 이미지 URL
            image_url = None
            try:
                img_elem = item.locator("img[alt*='상품 이미지']")
                if img_elem.count() > 0:
                    image_url = img_elem.first.get_attribute("src")
            except:
                pass

            # 할인율과 가격
            discount_rate = None
            price = None
            try:
                # 할인율
                discount_elem = item.locator("span.text-red")
                if discount_elem.count() > 0:
                    discount_rate = discount_elem.first.text_content().strip()
                
                # 가격
                price_elem = item.locator("span.text-black")
                if price_elem.count() > 0:
                    # 마지막 span이 가격
                    price_count = price_elem.count()
                    price = price_elem.nth(price_count - 1).text_content().strip()
            except:
                pass

            # 랭킹
            rank = None
            try:
                rank_elem = item.locator("span.text-black.font-pretendard")
                if rank_elem.count() > 0:
                    rank = rank_elem.first.text_content().strip()
            except:
                pass

            # 데이터 저장
            if image_url:
                product_data = {
                    "index": i + 1,
                    "rank": rank or str(i + 1),
                    "item_id": item_id,
                    "brand": brand or "브랜드 정보 없음",
                    "title": title or "제목 없음",
                    "discount_rate": discount_rate,
                    "price": price or "가격 정보 없음",
                    "image_url": image_url
                }
                products.append(product_data)
                
        except Exception as e:
            print(f"\n  상품 {i+1} 처리 중 오류: {e}")
            continue

    browser.close()

print(f"\n총 수집된 상품 수: {len(products)}")

if len(products) == 0:
    print("수집된 상품이 없습니다. 선택자를 확인해주세요.")
    exit()

# =========================
# 이미지 다운로드
# =========================
print("\n이미지 다운로드 시작...")
success_count = 0

for idx, product in enumerate(tqdm(products, desc="이미지 다운로드")):
    try:
        img_url = product["image_url"]
        
        # 파일 확장자 추출
        ext = "jpg"
        if "." in img_url.split("?")[0]:
            ext = img_url.split("?")[0].split(".")[-1]
        
        # 파일명 생성
        filename = f"{SAVE_DIR}/product_{idx+1:04d}.{ext}"
        
        # 다운로드
        if download_image(img_url, filename):
            product["local_image"] = filename
            success_count += 1
        else:
            product["local_image"] = None
            
    except Exception as e:
        print(f"  상품 {idx+1} 이미지 다운로드 실패: {e}")
        product["local_image"] = None

# =========================
# JSON 저장
# =========================
with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 50)
print("크롤링 완료!")
print("=" * 50)
print(f"총 상품 수: {len(products)}")
print(f"다운로드 성공: {success_count}")
print(f"다운로드 실패: {len(products) - success_count}")
print(f"이미지 저장 폴더: {SAVE_DIR}/")
print(f"상품 정보 JSON: {JSON_FILE}")
print("=" * 50)