from os import environ  # 환경변수를 가져오기 위한 모듈

from playwright.sync_api import sync_playwright

# 환경변수에서 아이디와 비밀번호를 가져옴
USER_ID = environ.get('NAVER_USER_ID', None)
USER_PW = environ.get('NAVER_USER_PW', None)

if USER_ID is None or USER_PW is None:
    raise ValueError('NAVER_USER_ID, NAVER_USER_PW 환경변수를 설정해주세요.')

# with문을 이용하여 playwright를 사용할 수 있도록 함
with sync_playwright() as p:
    # 브라우저 실행 시 채널을 chrome로 설정하여 별도의 실행환경을 설치하지 않아도 됨
    # headless=False로 설정하여 브라우저를 실행하고, slow_mo=100으로 설정
    browser = p.chromium.launch(headless=False, channel="chrome", slow_mo=100)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://www.naver.com')

    # 로그인 과정
    page.click('#account > a')
    page.fill('input[name=id]', USER_ID)
    page.fill('input[name=pw]', USER_PW)
    page.click('button.btn_login')

    # 메일 페이지로 이동
    page.goto('https://mail.naver.com')

    # 메일 목록을 가져오기 위해 페이지 로딩이 완료될 때까지 대기
    page.wait_for_load_state('networkidle')

    # css selector를 이용하여 메일 목록을 가져옴
    mail_list = page.locator('li.mail_item')

    # 메일 목록의 개수를 가져옴
    mail_cnt = mail_list.count()

    # 메일 목록을 순회하며 메일 제목과 보낸 사람을 출력
    for i in range(mail_cnt):
        mail = mail_list.nth(i)  # 메일 목록 중 i번째 메일을 가져옴
        mail.highlight()

        # 데이터가 아래와 같이 구성되어있어 TEXT NODE에 접근해야 값을 가져올 수 있음
        # <button type="button" class="button_sender" ><span class="blind">보낸 사람</span>네이버</button>
        # 이를 위해 XPath를 이용하여 TEXT NODE에 접근
        # 데이터를 감싸는 태그를 찾아서 해당 태그를 기준으로 TEXT NODE에 접근
        sender = mail.locator('//*[@class="mail_sender"]/button')
        # evaluate 함수를 이용하여 js 코드를 실행할 수 있으며, 호출 시 데이터를 전달할 수 있음
        sender_text = sender.evaluate('(sender, x) => document.evaluate(x, sender, null, XPathResult.STRING_TYPE).stringValue', 'text()')

        title = mail.locator('a.mail_title_link')

        # 메일 제목과 보낸 사람을 출력
        #sender_text는 자체가 문자열, title은 locator이기 때문에 text_content()를 이용하여 문자열을 가져옴
        print(f'{sender_text}: {title.text_content()}')
    
    # 브라우저 종료
    browser.close()