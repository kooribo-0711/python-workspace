import os
import time
import json
import requests
from playwright.sync_api import sync_playwright
from tqdm import tqdm
from urllib.parse import quote

# =========================
# 기본 설정
# =========================
SEARCH_KEYWORD = "강아지"  # 검색할 키워드
SAVE_DIR = f"google_images_{SEARCH_KEYWORD}"
JSON_FILE = f"google_{SEARCH_KEYWORD}.json"
MAX_IMAGES = 50  # 다운로드할 최대 이미지 수
MAX_PAGES = 5  # 클릭할 최대 "다음" 버튼 횟수

os.makedirs(SAVE_DIR, exist_ok=True)

# =========================
# 이미지 다운로드 함수
# =========================
def download_image(url, filename):
    """이미지를 다운로드하여 파일로 저장"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.google.com/"
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        
        # 이미지가 너무 작으면 제외 (1KB 이하)
        if len(r.content) < 1024:
            return False
            
        with open(filename, "wb") as f:
            f.write(r.content)
        return True
    except Exception as e:
        return False

# =========================
# Playwright 크롤링
# =========================
images_data = []

print("=" * 60)
print(f"구글 이미지 검색 크롤러 시작 - 검색어: '{SEARCH_KEYWORD}'")
print("=" * 60)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        locale="ko-KR",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        viewport={"width": 1920, "height": 1080}
    )
    page = context.new_page()

    # 구글 이미지 검색 URL
    search_url = f"https://www.google.com/search?q={quote(SEARCH_KEYWORD)}&tbm=isch"
    
    print(f"\n페이지 접속 중: {search_url}")
    page.goto(search_url, timeout=60000)
    
    # 페이지 로딩 대기
    print("페이지 로딩 대기 중...")
    page.wait_for_timeout(3000)

    collected_urls = set()  # 중복 제거용
    
    print(f"\n이미지 수집 시작 (목표: {MAX_IMAGES}개)...")
    
    page_num = 1
    
    while len(collected_urls) < MAX_IMAGES and page_num <= MAX_PAGES:
        print(f"\n=== 페이지 {page_num} 수집 중 ===")
        
        # 현재 페이지의 모든 이미지 요소 찾기
        # 구글 이미지 검색의 썸네일 컨테이너
        img_containers = page.locator("div.isv-r")
        container_count = img_containers.count()
        
        print(f"발견된 이미지 컨테이너: {container_count}개")
        
        for i in range(container_count):
            if len(collected_urls) >= MAX_IMAGES:
                break
                
            try:
                container = img_containers.nth(i)
                
                # 컨테이너 내의 링크 찾기
                link = container.locator("a.wXeWr")
                
                if link.count() > 0:
                    # 링크 클릭하여 이미지 상세 보기
                    link.first.scroll_into_view_if_needed()
                    page.wait_for_timeout(300)
                    link.first.click()
                    page.wait_for_timeout(1000)
                    
                    # 큰 이미지가 로드될 때까지 대기
                    try:
                        page.wait_for_selector("img.sFlh5c.pT0Scc, img.n3VNCb", timeout=3000)
                    except:
                        continue
                    
                    # 원본 이미지 URL 추출
                    image_url = None
                    
                    # 방법 1: 큰 이미지 직접 찾기
                    large_img_selectors = [
                        "img.sFlh5c.pT0Scc.iPVvYb",
                        "img.sFlh5c.pT0Scc",
                        "img.n3VNCb",
                        "img.r48jcc.pT0Scc"
                    ]
                    
                    for selector in large_img_selectors:
                        try:
                            large_img = page.locator(selector).first
                            if large_img.is_visible(timeout=1000):
                                src = large_img.get_attribute("src")
                                if src and src.startswith("http") and "encrypted" not in src:
                                    image_url = src
                                    break
                        except:
                            continue
                    
                    # 방법 2: data-src 속성 확인
                    if not image_url:
                        try:
                            img_with_data = page.locator("img[data-src^='http']").first
                            if img_with_data.count() > 0:
                                image_url = img_with_data.get_attribute("data-src")
                        except:
                            pass
                    
                    # 유효한 이미지 URL이고 중복이 아닌 경우만 저장
                    if (image_url and 
                        image_url.startswith("http") and 
                        image_url not in collected_urls and
                        "gstatic" not in image_url and
                        "encrypted" not in image_url):
                        
                        collected_urls.add(image_url)
                        print(f"  이미지 수집 {len(collected_urls)}/{MAX_IMAGES}")
                        
            except Exception as e:
                continue
        
        # 다음 페이지로 이동
        if len(collected_urls) < MAX_IMAGES and page_num < MAX_PAGES:
            print(f"\n'다음' 버튼 찾는 중...")
            
            # 다음 버튼 선택자들
            next_button_selectors = [
                "a#pnnext",  # 일반적인 다음 버튼
                "a[aria-label='다음 페이지']",
                "a[aria-label='Next page']",
                "td.d6cvqb a"
            ]
            
            next_clicked = False
            
            for selector in next_button_selectors:
                try:
                    next_button = page.locator(selector)
                    if next_button.count() > 0 and next_button.first.is_visible():
                        print(f"  '다음' 버튼 클릭...")
                        next_button.first.click()
                        page.wait_for_timeout(3000)
                        next_clicked = True
                        page_num += 1
                        break
                except Exception as e:
                    continue
            
            if not next_clicked:
                print("  '다음' 버튼을 찾을 수 없습니다. 수집 종료.")
                break
        else:
            break
    
    browser.close()

# 수집된 URL을 리스트로 변환
images_data = [{"index": i+1, "image_url": url} for i, url in enumerate(collected_urls)]

print(f"\n총 수집된 고유 이미지 URL: {len(images_data)}개")

if len(images_data) == 0:
    print("수집된 이미지가 없습니다.")
    print("브라우저가 닫히기 전에 페이지를 확인해주세요.")
    exit()

# =========================
# 이미지 다운로드
# =========================
print("\n이미지 다운로드 시작...")
success_count = 0
failed_urls = []

for idx, img_data in enumerate(tqdm(images_data, desc="이미지 다운로드")):
    try:
        img_url = img_data["image_url"]
        
        # 파일 확장자 추출
        ext = "jpg"
        url_path = img_url.split("?")[0]
        if "." in url_path:
            file_ext = url_path.split(".")[-1].lower()
            if file_ext in ["jpg", "jpeg", "png", "webp", "gif"]:
                ext = file_ext
        
        # 파일명 생성
        filename = f"{SAVE_DIR}/{SEARCH_KEYWORD}_{idx+1:04d}.{ext}"
        
        # 다운로드
        if download_image(img_url, filename):
            img_data["local_image"] = filename
            img_data["download_status"] = "success"
            success_count += 1
        else:
            img_data["local_image"] = None
            img_data["download_status"] = "failed"
            failed_urls.append(img_url)
            
    except Exception as e:
        img_data["local_image"] = None
        img_data["download_status"] = "error"
        failed_urls.append(img_url)

# =========================
# JSON 저장
# =========================
with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(images_data, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 60)
print("크롤링 완료!")
print("=" * 60)
print(f"검색어: {SEARCH_KEYWORD}")
print(f"수집된 URL: {len(images_data)}개")
print(f"다운로드 성공: {success_count}개")
print(f"다운로드 실패: {len(images_data) - success_count}개")
print(f"이미지 저장 폴더: {SAVE_DIR}/")
print(f"정보 JSON 파일: {JSON_FILE}")
print("=" * 60)

if failed_urls:
    print(f"\n실패한 URL 샘플 (최대 5개):")
    for url in failed_urls[:5]:
        print(f"  - {url[:80]}...")