from playwright.sync_api import sync_playwright
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time

KEYWORD = "이재명"   # 검색할 키워드


def get_top10_comments(keyword):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 디버깅용
        context = browser.new_context()
        page = context.new_page()

        # 1. 네이버 뉴스 검색
        search_url = f"https://news.naver.com/"
        page.goto(search_url)
        page.wait_for_timeout(2000)

        # 2. 첫 번째 뉴스 클릭
        first_news = page.locator("a.news_tit").first
        first_news.click()
        page.wait_for_timeout(2000)

        # 새 탭 전환
        page = context.pages[-1]

        # 3. 댓글 iframe 접근
        page.wait_for_selector("iframe#commentFrame", timeout=10000)
        frame = page.frame(name="commentFrame")

        # 4. 공감순 정렬 클릭
        frame.wait_for_selector("a.u_cbox_sort_option", timeout=10000)
        frame.locator("a.u_cbox_sort_option").nth(1).click()  # 공감순
        frame.wait_for_timeout(2000)

        # 5. 댓글 수집
        comments = frame.locator("span.u_cbox_contents")
        count = min(comments.count(), 10)

        top_comments = []
        for i in range(count):
            text = comments.nth(i).inner_text().strip()
            top_comments.append(text)

        browser.close()
        return top_comments


def make_wordcloud(comments):
    text = " ".join(comments)

    wc = WordCloud(
        font_path="malgun.ttf",
        width=600,
        height=400,
        background_color="white"
    ).generate(text)

    plt.figure(figsize=(10,5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    comments = get_top10_comments(KEYWORD)

    print("\n=== 네이버 뉴스 댓글 TOP 10 (공감순) ===")
    for i, c in enumerate(comments, 1):
        print(f"\n{i}. {c}")

    make_wordcloud(comments)
