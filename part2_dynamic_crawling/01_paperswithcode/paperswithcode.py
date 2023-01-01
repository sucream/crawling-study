from playwright.sync_api import sync_playwright, Browser, Page, expect


# 네트워크 속도를 위한 세팅
NETWORKCONDITIONS = {
  'Slow 3G': {
    'download': ((500 * 1000) / 8) * 0.8,
    'upload': ((500 * 1000) / 8) * 0.8,
    'latency': 400 * 5,
  },
  'Fast 3G': {
    'download': ((1.6 * 1000 * 1000) / 8) * 0.9,
    'upload': ((750 * 1000) / 8) * 0.9,
    'latency': 150 * 3.75,
  },
}

def get_paper_list():
    with sync_playwright() as p:
        # 새로운 브라우저
        browser: Browser = p.chromium.launch(
            headless=False, slow_mo=500, channel="chrome")
        
        # 컨텍스트 생성
        context = browser.new_context()

        url = 'https://paperswithcode.com/'

        # 새로운 페이지 생성
        page: Page = context.new_page()
        # 테스트를 위한 cdp 세션 생성
        cdp_session = context.new_cdp_session(page)

        # 의도적으로 네트워크 속도를 늦춤
        cdp_session.send("Network.emulateNetworkConditions", {
            'downloadThroughput': NETWORKCONDITIONS['Fast 3G']['download'],
            'uploadThroughput': NETWORKCONDITIONS['Fast 3G']['upload'],
            'latency': NETWORKCONDITIONS['Fast 3G']['latency'],
            'offline': False,
        })

        # 페이지 이동
        # wait_until 옵션을 통해 네트워크 통신이 끝날 때까지 기다림
        page.goto(url, wait_until="networkidle")

        idx = 0
        while True:
            paper_list = page.locator(f'div.paper-card:nth-child(n+{idx})')
            last_element_count = page.locator('div.paper-card').count()

            paper_cnt = paper_list.count()

            # 최초 실행시에는 인덱스 문제로 1을 더해줌
            if idx == 0:
                idx += 1
            idx += paper_cnt

            for i in range(paper_cnt):
                paper = paper_list.nth(i)
                paper.scroll_into_view_if_needed()
                paper.highlight()
                print(paper.locator('h1 > a').text_content())
                page.wait_for_timeout(300)

            # 스크롤을 맨 아래로 내림
            page.evaluate('() => window.scrollTo(0, document.body.scrollHeight)')


            # 데이터가 돔에 렌더링될 때까지 대기
            # 타임아웃을 걸어서 최대 5초만 기다림
            try:
                page.wait_for_function(expression="count => document.querySelectorAll('div.paper-card').length > count", arg=last_element_count, timeout=5000)
            except Exception as e:
                print('데이터를 불러올 수 없습니다.', e)
                break

        browser.close()


if __name__ == "__main__":
    get_paper_list()