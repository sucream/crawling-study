from playwright.sync_api import sync_playwright, Browser, Page, expect


def get_paper_list():
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(
            headless=False, slow_mo=500, channel="chrome")

        url = 'https://paperswithcode.com/'

        page: Page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        idx = 0
        while True:
            paper_list = page.locator(f'div.paper-card:nth-child(n+{idx})')
            container = page.locator('div.container')

            paper_cnt = paper_list.count()

            # 최초 실행시에는 인덱스 문제로 1을 더해줌
            if idx == 0:
                idx += 1
            idx += paper_cnt

            for i in range(paper_cnt):
                paper = paper_list.nth(i)
                paper.highlight()
                print(paper.locator('h1 > a').text_content())

            # 비교를 위해 가장 마지막 논문의 제목을 가져옴
            last_paper = paper_list.last
            last_paper_title = last_paper.locator('h1 > a').text_content()

            # 스크롤 맨 아래로 이동
            page.evaluate(
                '() => window.scrollTo(0, document.body.scrollHeight)')
            # 스크롤 이후 데이터를 불러오는 시간을 기다림
            page.wait_for_load_state('networkidle')
            # 데이터를 렌더링하는 시간을 기다려줌
            # 향후 이벤트로 변경해 보기
            page.wait_for_timeout(3000)

            paper_list = page.locator('div.paper-card').last

            if last_paper_title == paper_list.locator('h1 > a').first.text_content():
                break
