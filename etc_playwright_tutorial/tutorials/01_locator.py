from playwright.sync_api import sync_playwright, Browser, Page, expect


def run():
    """
    ### `locator`를 사용하는 방법에 대해 알아봅니다.
    - `locator`는 `selector`와 유사한 역할을 합니다.
    - 기본적으로 `css selector`, `xpath`를 모두 지원합니다.
    - 그 외에도 다양한 속성을 이용하여 `locator`를 찾을 수 있습니다.
    - `locator`는 chainable 하게 사용할 수 있습니다.
    - 자세한 내용은 [링크](https://playwright.dev/python/docs/locators)를 참조하세요.
    """

    # with문을 사용하여 안전하게 playwright를 사용할 수 있습니다.
    # with문을 이용하기 때문에 playwright를 사용한 후에는 자동으로 종료됩니다.
    with sync_playwright() as p:
        # playwright를 이용해 사용할 브라우저를 지정할 수 있습니다.
        # 특별한 경우를 제외하고 일반적으로 chromium을 사용합니다.
        # 기본적으로 headless 모드로 동작합니다.
        # channel을 'chrome'으로 지정하면 PC에 설치된 chrome을 사용할 수 있습니다.
        browser: Browser = p.chromium.launch(headless=False, slow_mo=500, channel="chrome")

        url = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=105&sid2=226'

        # browser.new_page()를 통해 새로운 탭을 열 수 있습니다.
        page: Page = browser.new_page()

        page.goto(url)

        page.wait_for_load_state('networkidle')


        # 기본적으로 css selector를 사용합니다.
        # 해당 locator에 해당되는 요소가 여러개일 경우, locator의 count()를 통해 개수를 확인할 수 있습니다.
        # 또한 locator.nth()를 통해 해당 인덱스의 locator를 가져올 수 있습니다.
        news_list = page.locator('div.list_body > ul[class^=type] > li')

        news_cnt = news_list.count()

        for i in range(news_cnt):
            news = news_list.nth(i)
            news.highlight()  # 해당 로케이터를 강조

            # playwright는 기본적으로 비동기로 동작하기 때문에 time.sleep()을 사용하면 기다리지 않습니다.
            # 대신 wait_for_timeout()을 사용합니다.
            page.wait_for_timeout(500)

            # text_content()를 통해 해당 locator의 text를 가져올 수 있습니다.
            title = news.locator('dl > dt:nth-child(2) > a').text_content().strip()
            print(title)

        browser.close()  # 사용 후에는 브라우저를 종료해 줍니다.


if __name__ == '__main__':
    run()