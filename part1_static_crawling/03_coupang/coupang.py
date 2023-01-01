from typing import List, Dict
from datetime import datetime
from urllib.parse import urljoin  # urljoin을 이용하여 절대 경로로 변환

import requests
from bs4 import BeautifulSoup


HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

def get_product_list(search_keyword: str=None) -> List[Dict[str, str]]:
    """
    쿠팡 검색 목록을 크롤링하는 함수

    Parameters
    ----------
    search_keyword : str
        검색할 단어

    Returns
    -------
    List[Dict[str, str]]
        뉴스 목록
        [
            {
                'name': '상품명',
                'price': '가격',
                'link': '상품 링크',

            },
            ...
        ]
        
    """
    if not search_keyword:
        raise Exception('검색 키워드는 필수입니다.')

    URL = f'https://www.coupang.com/np/search?component=&q={search_keyword}&channel=user'


    # 세션을 이용하여 쿠키를 유지
    session = requests.session()
    session.get('https://weblog.coupang.com', headers=HEADER, allow_redirects=True)

    response = session.get(URL, headers=HEADER, timeout=10)  # requests는 기본적으로 타임아웃이 없어서 계속 기다림

    soup = BeautifulSoup(response.text, 'html.parser')

    # select를 이용하여 다수의 항목을 가져올 수 있음
    product_list = soup.select('li.search-product:not(.search-product__ad-badge):not(.best-seller-carousel-item)')

    result: List[Dict[str, str]] = []

    for product in product_list:
        name = product.select_one('div.name').text.strip()
        link = urljoin(URL, product.select_one('a')['href'])
        price = product.select_one('strong.price-value').text.strip()
        out_of_stock = product.select_one('div.out-of-stock')
        if out_of_stock:
            arrival_info = out_of_stock.text.strip()
        else:
            arrival_info = product.select_one('span.arrival-info').text.strip()

        result.append({
            'name': name,
            'link': link,
            'price': price,
            'arrival_info': arrival_info,
        })

    return result


if __name__ == '__main__':
    product_list = get_product_list('아이폰14')

    for product in product_list:
        print(product)