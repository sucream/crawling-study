from urllib.request import urlretrieve
import os

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

    pic_idx = 0
    all_idx = 0
    while True:
        data_list: Locator = get_image_locators(page, all_idx)
        cnt = data_list.count()

        for i in range(all_idx, cnt):
            all_idx += 1

            loc: Locator = data_list.nth(i)
            img: Locator = loc.locator('a.wXeWr.islib.nfEiy')
            img.click()
            page.wait_for_load_state("networkidle")

            try:
                img_src: Locator = page.locator('a.eHAdSb > img.KAlRDb')
                link = img_src.get_attribute('src', timeout=1000)
            except:
                continue
            else:
                pic_idx += 1

            # 이미지 디렉토리 생성
            os.makedirs(f'./images', exist_ok=True)

            # 이미지 다운로드
            try:
                urlretrieve(link, f'./images/{keyword}_{pic_idx}.jpg', )
            except Exception as e:
                print(e)
                pic_idx -= 1
            else:
                print(pic_idx)
                print(link)

            if pic_idx == max_num:
                break
        
        if pic_idx == max_num:
            break

        try:
            gen_new_images(page)
        except Exception as e:
            print(e)
            break

    browser.close()


def gen_new_images(page: Page) -> None:
    now_page_height = page.evaluate('() => document.body.scrollHeight')
    page.evaluate('() => window.scrollTo(0, document.body.scrollHeight)')
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)
    after_scroll_page_height = page.evaluate('() => document.body.scrollHeight')

    if now_page_height == after_scroll_page_height:
        raise Exception('더 이상 이미지를 불러올 수 없습니다.')


def get_image_locators(page: Page, idx: int) -> Locator:
    return page.locator(f'div.islrc > div.isv-r.PNCib.MSM1fd.BUooTd:nth-child(n+{idx})')


if __name__ == "__main__":
    get_google_images('dog', 10)