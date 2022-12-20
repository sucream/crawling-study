from playwright.sync_api import sync_playwright, PlaywrightContextManager, Browser, Page, Locator


def get_google_images(keyword: str, max_num: int):
    with sync_playwright() as playwright:
        run(playwright, keyword, max_num)


def run(playwright: PlaywrightContextManager, keyword: str, max_num: int) -> None:
    browser: Browser = playwright.chromium.launch(
        headless=False, channel="chrome")
    page: Page = browser.new_page()

    page.goto(f"https://www.google.com/search?q={keyword}&tbm=isch")
    page.reload()
    page.wait_for_load_state("networkidle")

    idx = 0

    while True:
        data_list: Locator = get_image_locators(page)
        cnt = data_list.count()

        for i in range(idx, cnt):
            idx += 1
            if i == max_num:
                break

            loc: Locator = data_list.nth(i)
            img: Locator = loc.locator('a.wXeWr.islib.nfEiy')
            img.click()
            page.wait_for_load_state("networkidle")

            try:
                img_src: Locator = page.locator('a.eHAdSb > img.KAlRDb')
                link = img_src.get_attribute('src', timeout=1000)
            except:
                continue

            print(i)
            print(link)

        if idx == max_num:
            break

        gen_new_images(page)

    browser.close()


def gen_new_images(page: Page) -> None:
    page.evaluate('() => window.scrollTo(0, document.body.scrollHeight)')
    page.wait_for_load_state("networkidle")


def get_image_locators(page: Page) -> Locator:
    return page.locator('div.islrc > div.isv-r.PNCib.MSM1fd.BUooTd')
