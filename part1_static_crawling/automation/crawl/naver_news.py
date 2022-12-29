from typing import List, Dict
from datetime import datetime

import requests
from bs4 import BeautifulSoup


HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

def get_news_list(date: str, page: int = 1) -> List[Dict[str, str]]:
    """
    네이버 뉴스 목록을 크롤링하는 함수

    Parameters
    ----------
    date : str
        뉴스 목록을 가져올 날짜
        `20220101` 형식의 문자열
    page : int
        뉴스 목록을 가져올 페이지

    Returns
    -------
    List[Dict[str, str]]
        뉴스 목록
        [
            {
                'title': '제목',
                'writing': '신문사',
                'url': '링크'
            },
            ...
        ]
        
    """
    if date is None:
        date = datetime.today().strftime('%Y%m%d')

    sid1 = 101
    sid2 = 259
    mid = 'shm'
    mode = 'LS2D'

    URL = f'https://news.naver.com/main/list.naver?mode={mode}&mid={mid}&sid2={sid2}&sid1={sid1}&date={date}&page={page}'


    response = requests.get(URL, headers=HEADER, timeout=10)  # requests는 기본적으로 타임아웃이 없어서 계속 기다림

    soup = BeautifulSoup(response.text, 'html.parser')

    # select를 이용하여 다수의 항목을 가져올 수 있음
    news_list = soup.select('div.list_body > ul li')

    result: List[Dict[str, str]] = []

    for news in news_list:
        title = news.select_one('dl > dt:not(.photo) > a')
        writing = news.select_one('dl > dd > span.writing')

        result.append({
            'title': title.text.strip(),
            'writing': writing.text.strip(),
            'url': title['href']
        })

    return result


def get_news(url: str) -> Dict[str, str]:
    """
    네이버 뉴스를 크롤링하는 함수

    Parameters
    ----------
    url : str
        뉴스 url

    Returns
    -------
    Dict[str, str]
        뉴스
        {
            'title': '제목',
            'writing': '신문사',
            'content': '내용'
        }
    """
   
    response = requests.get(url, headers=HEADER, timeout=10)

    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.select_one('h2#title_area > span').text.strip()

    contents = soup.select_one('div#dic_area').text.strip()

    return {
        'title': title,
        'content': contents
    }