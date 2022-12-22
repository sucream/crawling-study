from os import environ

from playwright.sync_api import sync_playwright

USER_ID = environ.get('NAVER_USER_ID', None)
USER_PW = environ.get('NAVER_USER_PW', None)

if USER_ID is None or USER_PW is None:
    raise ValueError('NAVER_USER_ID, NAVER_USER_PW 환경변수를 설정해주세요.')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, channel="chrome", slow_mo=100)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://www.naver.com')
    page.click('#account > a')
    page.fill('input[name=id]', USER_ID)
    page.fill('input[name=pw]', USER_PW)
    page.click('button.btn_login')

    page.goto('https://mail.naver.com')

    page.wait_for_load_state('networkidle')

    mail_list = page.locator('li.mail_item')

    mail_cnt = mail_list.count()

    for i in range(mail_cnt):
        mail = mail_list.nth(i)
        sender = mail.locator('//*[@class="mail_sender"]/button')
        sender_text = sender.evaluate('(sender, x) => document.evaluate(x, sender, null, XPathResult.STRING_TYPE).stringValue', 'text()')
        # sender = page.evaluate('''(e) => document.evaluate('//*[@class="mail_sender"]/button/text()', e, null, XPathResult.STRING_TYPE).stringValue''', mail.element_handle)
        print(sender_text)
    browser.close()