import os
import time
import json
import requests
from playwright.sync_api import sync_playwright
from tqdm import tqdm

# =========================
# 기본 설정
# =========================
SAVE_DIR = "zara_perfume_images"
JSON_FILE = "zara_products.json"
URL = "https://www.zara.com/kr/ko/woman-perfumes-floral-l6572.html?v1=2419839"

os.makedirs(SAVE_DIR, exist_ok=True)

# =========================
# 이미지 다운로드 함수
# =========================
def download_image(url, filename):
    """이미지를 다운로드하여 파일로 저장"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.zara.com/"
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
        print(f"\n다운로드 실패 ({url}): {e}")
        return False

# =========================
# Playwright 크롤링
# =========================
products = []

print("=" * 50)
print("Zara 향수 상품 크롤러 시작")
print("=" * 50)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
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
    for i in range(8):
        page.mouse.wheel(0, 3000)
        page.wait_for_timeout(2000)
        print(f"  스크롤 {i+1}/8 완료")

    print("\n상품 데이터 수집 중...")

    # Zara 상품 카드 선택자
    selector = "li.product-grid-product[data-productid]"
    
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
            # data-productid로 상품 ID 가져오기
            product_id = item.get_attribute("data-productid")
            
            # 상품명
            title = None
            try:
                title_elem = item.locator("a.product-grid-product-info__name h3")
                if title_elem.count() > 0:
                    title = title_elem.first.text_content().strip()
            except:
                pass

            # 이미지 URL
            image_url = None
            try:
                img_elem = item.locator("img.media-image__image")
                if img_elem.count() > 0:
                    image_url = img_elem.first.get_attribute("src")
            except:
                pass

            # 가격 정보
            current_price = None
            original_price = None
            discount_rate = None
            
            try:
                # 현재 가격 (할인가 또는 정상가)
                current_price_elem = item.locator("span.price-current__amount .money-amount__main")
                if current_price_elem.count() > 0:
                    current_price = current_price_elem.first.text_content().strip()
                
                # 원가 (할인 전 가격) - 있을 경우에만
                original_price_elem = item.locator("span.price-old__amount .money-amount__main")
                if original_price_elem.count() > 0:
                    original_price = original_price_elem.first.text_content().strip()
                
                # 할인율 계산 (원가와 할인가가 모두 있을 경우)
                if original_price and current_price:
                    try:
                        # 가격에서 숫자만 추출
                        original_num = int(''.join(filter(str.isdigit, original_price)))
                        current_num = int(''.join(filter(str.isdigit, current_price)))
                        
                        if original_num > 0:
                            discount = ((original_num - current_num) / original_num) * 100
                            discount_rate = f"{discount:.0f}%"
                    except:
                        pass
                        
            except Exception as e:
                print(f"\n  상품 {i+1} 가격 처리 중 오류: {e}")

            # 상품 URL
            product_url = None
            try:
                url_elem = item.locator("a.product-link[href]")
                if url_elem.count() > 0:
                    product_url = url_elem.first.get_attribute("href")
                    if product_url and not product_url.startswith("http"):
                        product_url = "https://www.zara.com" + product_url
            except:
                pass

            # 데이터 저장
            if image_url:
                product_data = {
                    "index": i + 1,
                    "product_id": product_id,
                    "title": title or "제목 없음",
                    "current_price": current_price or "가격 정보 없음",
                    "original_price": original_price,
                    "discount_rate": discount_rate,
                    "product_url": product_url,
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
        
        # Zara 이미지 URL에서 고해상도 버전 가져오기
        # w=168을 w=1024로 변경하여 고해상도 이미지 다운로드
        if "w=168" in img_url:
            img_url = img_url.replace("w=168", "w=1024")
        
        # 파일 확장자 추출
        ext = "jpg"
        if "." in img_url.split("?")[0]:
            ext = img_url.split("?")[0].split(".")[-1]
        
        # 파일명 생성
        filename = f"{SAVE_DIR}/product_{idx+1:04d}.{ext}"
        
        # 다운로드
        if download_image(img_url, filename):
            product["local_image"] = filename
            product["downloaded_image_url"] = img_url  # 실제 다운로드한 URL 저장
            success_count += 1
        else:
            product["local_image"] = None
            
    except Exception as e:
        print(f"\n  상품 {idx+1} 이미지 다운로드 실패: {e}")
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

# 할인 중인 상품만 필터링하여 출력
discounted_products = [p for p in products if p.get("discount_rate")]
if discounted_products:
    print(f"\n할인 중인 상품: {len(discounted_products)}개")
    for p in discounted_products:
        print(f"  - {p['title']}: {p['original_price']} → {p['current_price']} ({p['discount_rate']} 할인)")