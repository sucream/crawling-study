# Playwright Tutorial

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
  from playwright.sync_api import sync_playwright

  with sync_playwright() as p:
      browser = p.chromium.launch(headless=False)
      context = browser.new_context()
      page = context.new_page()
      page.goto("https://www.naver.com")
      page.click("text=로그인")
      page.fill("input[name=id]", "ID")
      page.fill("input[name=pw]", "PW")
      page.click("text=로그인")
      page.click("text=메일")
      page.click("text=받은 메일함")
      mail_list = page.locator("div.mail_list")
      for mail in mail_list:
          print(mail.inner_text())
      browser.close()
  ```
