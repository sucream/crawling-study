from typing import List, Dict
from datetime import datetime

import requests
from bs4 import BeautifulSoup


HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

def get_store_list(sido: str='02', gubun: str='') -> List[Dict[str, str]]:
    """
    굽네치킨 점포 목록을 크롤링하는 함수

    Parameters
    ----------
    sido : str
        시도 코드
        기본값은 서울(02)
    gubun : str
        구군 코드
        기본값은 빈 문자열로, 전체를 의미

    Returns
    -------
    List[Dict[str, str]]
        굽네치킨 점포 목록
        [
            {
                'br_name': '브랜드명',
                'address': '주소',
                'tel1': '전화번호',
                'xloc': '경도',
                'yloc': '위도',
            },
            ...
        ]
    """

    URL = 'https://www.goobne.co.kr/store/srch_storeInfo'

    data = {
        "paging_yn": "N",
        "sido": sido,
        "gugun": gubun
    }

    # 특정 데이터를 같이 전달하기 위해 post를 이용하였음
    # 해당 요청은 json 형태로 전달되어야 하므로 json=data를 추가
    res = requests.post(URL, json=data, headers=HEADER).json()

    result: List[Dict[str, str]] = []

    for store in res['body']['store_list']['store_list']:
        br_name = store['br_name']
        address = store['address']
        tel1 = store['tel1']
        xloc = store['xloc']
        yloc = store['yloc']

        result.append({
            'br_name': br_name,
            'address': address,
            'tel1': tel1,
            'xloc': xloc,
            'yloc': yloc,
        })

    return result