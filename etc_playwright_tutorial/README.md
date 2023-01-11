# Playwright Tutorial

![playwright](../img/playwright.jpg)

- 기본적인 Playwright 사용법을 익히기 위한 튜토리얼입니다.
- 최대한 적은 기능을 사용하려 했습니다.

## 1. Playwright 개요

- Playwright는 브라우저를 제어하기 위한 Node.js 라이브러리입니다.
- playwright는 Python, Java, C# 등 다양한 언어를 지원합니다.
- Chromium, Webkit, Firefox를 지원합니다.
- 비동기를 지원하기 때문에 await, async를 사용할 수 있습니다.
- codegen을 지원하여, 브라우저에서 작업한 내용을 코드로 변환할 수 있습니다.

## 2. Playwright 설치

- `pip install playwright`로 설치가 가능합니다.
- 기본적으로 playwright에서 사용하는 브라우저를 설치해야 합니다.
- `playwright install [chromium|webkit|firefox]`로 설치가 가능합니다.
- 실제 사용할 때 channel을 지정하면 PC에 설치된 브라우저를 그대로 사용할 수 있습니다.(사용자 정보는 별도)

## 3. Playwright 사용법

- playwright는 크게 `PlaywrightContextManager`, `Browser`, `Context`, `Page`, `Locator`의 5가지로 구성되어 있습니다.

### 3.1 PlaywrightContextManager

- PlaywrightContextManager는 `from playwright.sync_api import sync_playwright`를 import하여 사용할 수 있습니다.
- 안전한 실행과 종료를 위해 `with sync_playwright() as p` 형태의 with문을 사용합니다.

### 3.2 Browser

- Browser는 `PlaywrightContextManager`를 통해 생성됩니다.
- 실제 브라우저를 실행 및 관리합니다.
- `p.chromium.launch()` 형태로 브라우저를 실행할 수 있습니다.
- 브라우저를 실행할 때 헤드리스 여부, 채널, 사용자 데이터 디렉토리 등을 지정할 수 있습니다.

### 3.3 Context

- Context는 브라우저 내에서 다수의 컨텍스트를 위한 선택사항이며, `Browser`를 통해 생성됩니다.
- `browser.new_context()` 형태로 생성할 수 있습니다.

### 3.4 Page

- Page는 브라우저에서 실제로 작업을 수행하는 탭이라 불리는 하나의 객체입니다.
- `browser.new_page()`, `context.new_page()` 형태로 생성할 수 있습니다.
- `page.goto(URL)` 형태로 페이지를 이동할 수 있습니다.
- 대부분의 페이지 관련 인터랙션은 `page`를 통해 이루어집니다.

### 3.5 Locator

- Locator는 `Page`, `Locator`를 통해 생성되며, DOM을 탐색하는데 사용됩니다.
- 기존의 css selector, xpath 등을 사용할 수 있습니다.
- 추가로 다양항 형태의 선택자를 지원합니다.
- `page.queryselector` 등도 지원하지만, locator를 통해 엘리먼트에 접근하는 것을 권장합니다.

## 4. Playwright 예제

- 아래 예제는 `playwright`를 사용하여 `https://www.naver.com`에 접속하여 로그인 하고 메일 리스트를 가져오는 예제입니다.

  ```python
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
  ```

## 5. Playwright codegen 기능 이용해 보기([관련 링크](https://playwright.dev/python/docs/codegen-intro))

![codegen](../img/codegen.gif)

- `codegen`은 playwright의 확장 기능이기 때문에 `playwright install`을 해야 사용할 수 있음
- playwright codegen 기능을 이용하면 브라우저에서 수행한 작업을 레코딩하여 파이썬 코드로 변환해줌
- `playwright codegen URL` 형태로 사용하며, 실행시 브라우저가 실행되고, 브라우저에서 수행한 작업을 레코딩됨
- 본 기능은 대략적인 참고용으로만 사용하고, 실제 코드를 작성할 때는 코드를 직접 작성하는 것이 좋음(codegen은 해당 행위에 대한 specipic한 코드만 생성하기 때문에 범용적인 프로그램에는 어울리지 않을 수 있음)

## 6. 자주 사용하는 메소드들

- `page.goto(url)` : 해당 url로 이동
- `page.locator(selector)` : 해당 selector를 찾아 locator 객체를 반환
- `page.click(selector)` : 해당 selector를 클릭
- `page.fill(selector, text)` : 해당 selector에 text를 입력
- `page.screenshot(path="example.png")` : 현재 페이지의 스크린샷을 path에 저장
- `locator.highlight()` : 해당 locator를 화면에 강도하여 표시
- `locator.click()` : 해당 locator를 클릭
- `locator.fill(text)` : 해당 locator에 text를 입력
- `locator.text_content()` : 해당 locator의 text를 반환
- `locator.evaluate(func, *args)` : 해당 locator에 자바스크립트 함수를 실행하고, args를 전달함
- `locator.check()` : 해당 locator를 체크함
- `locator.uncheck()` : 해당 locator를 체크 해제함
- `locator.is_checked()` : 해당 locator가 체크되어 있는지 확인
- `locator.is_disabled()` : 해당 locator가 비활성화 되어 있는지 확인
- `locator.press("Enter")` : 해당 locator에 key를 입력함
- `locator.set_input_files('myfile.pdf')` : 해당 locator에 파일을 업로드함
- `locator.select_option('blue')` : 해당 locator의 value를 기준으로 option을 선택함
- `locator.select_option(label='blue')` : 해당 locator의 label을 기준으로 option을 선택함
- `page.locator("#item-to-be-dragged").drag_to(page.locator("#item-to-drop-at"))` : 해당 locator를 드래그하여 다른 locator에 드랍함

## 7. Playwright 조금 더 알아보기

### 7.1. 우아하게 파일 다운로드 처리하기

- playwright는 파일 다운로드를 기다리는 컨택스트를 제공함
- 내부적으로는 `expect_event`를 이용하여 다운로드가 시작되는 것을 기다리고, 다운로드가 시작되면 `Download` 객체를 반환함

  ```python
  # 다운로드가 시작되는 것을 기다리는 컨택스트
  with page.expect_download() as download_info:
      다운로드 창을 띄우기 위한 작업
      page.get_by_text("Download file").click()
  # 실제 다운로드 정보를 가져옴
  download = download_info.value

  # 원하는 이름으로 파일 저장
  download.save_as("/path/to/save/download/at.txt")

  # 추천하는 이름으로 파일 저장
  download.save_as(download.suggested_filename)
  ```

### 7.2. 다이얼로그 인터랙션 하기

- playwright는 기본적으로 다이얼로그가 나타나면 `dismiss`를 수행함
- 다이얼로그 발생시 적절한 처리를 할 수 있는 핸들러를 등록할 수 있음
- playwright의 모든 핸들러는 `page.on('event_name', handler)` 형태로 등록할 수 있음
- 1회성 핸들러는 `page.once('event_name', handler)` 형태로 등록할 수 있음

  ```python
  # 다이얼로그가 발생하면 accept를 수행하는 핸들러 등록
  page.on("dialog", lambda dialog: dialog.accept())


  # 다이얼로그 발생
  page.evaluate("() => confirm('동의하시겠습니까?')")
  page.evaluate("() => alert('경고창입니다.')")
  ```

### 7.3. playwright 로그 확인하기

- playwright는 `Trace Viewer`라고 하는 로그를 기록하는 기능을 제공함
- playwright를 시작할 때 간단한 설정을 추가하여 로그를 기록할 수 있음
- 로그 내역은 zip 파일로 저장되며, `playwright show-trace trace.zip` 명령어를 통해 확인할 수 있음

  ```python
  browser = chromium.launch()
  context = browser.new_context()

  # 로그를 기록하기 위한 설정
  # 로그를 기록할 때 스크린샷, 소스코드, 스냅샷을 함께 기록하도록 설정할 수 있음
  context.tracing.start(screenshots=True, snapshots=True, sources=True)

  page = context.new_page()
  page.goto("https://playwright.dev")
  page.screenshot(path="example.png")

  # 원하는 순간에 로그 기록을 중단하고 zip 파일로 저장할 수 있음
  context.tracing.stop(path = "trace.zip")
  browser.close()
  ```

  ```bash
  playwright show-trace trace.zip
  ```

### 7.4. 유연하게 대기하기

- playwright는 `page.wait_for_state()`를 통해 특정 상태가 될 때까지 대기할 수 있음
- 크게 3가지 상태를 지원함
  - `load` - load 이벤트가 발생할 때까지 기다림
  - `domcontentloaded` - DOMContentLoaded 이벤트가 발생할 때까지 기다림
  - `networkidle` - 최소 0.5초를 기다리며, 더이상 네트워크 연결이 없을 때까지 기다림(가장 유용한 기능)
- 이러한 기능들은 대부분의 기능(click, goto 등)에서도 `wait_until` 형태로 지원

### 7.5 time.sleep()을 사용하지 말기

- 기본적으로 playwright는 [auto-waiting](https://playwright.dev/python/docs/actionability)을 지원함
- 그럼에도 불구하고 특정 상황에는 의도적으로 기다려야 하는 경우가 생김
- playwright는 비동기 방식으로 동작하기 때문에, `time.sleep()`을 사용하면 의도한 대로 동작하지 않을 수 있음
- `page.wait_for_timeout(ms)`을 사용하여 동일한 기능을 구현할 수 있음

### 7.6. pyinstaller 로 배포하기

- playwright는 pyinstaller로 배포하는 것을 고려하여 만들어져 있음
- bash
  ```console
  PLAYWRIGHT_BROWSERS_PATH=0 playwright install chromium
  pyinstaller -F main.py
  ```
- cmd
  ```cmd
  set PLAYWRIGHT_BROWSERS_PATH=0
  playwright install chromium
  pyinstaller -F main.py
  ```
- powershell
  ```powershell
  $env:PLAYWRIGHT_BROWSERS_PATH="0"
  playwright install chromium
  pyinstaller -F main.py
  ```
