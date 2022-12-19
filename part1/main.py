import time

from automation.crawl.naver_news import get_news_list, get_news
from automation.crawl.goobne_stores import get_store_list
from automation.crawl.coupang import get_product_list

def naver():
    news_list = get_news_list('20200501')

    for news in news_list:
        print(get_news(news['url']))
        time.sleep(0.5)

def goobne():
    goobne_list = get_store_list()

    for store in goobne_list:
        print(store)

def coupang():
    coupang_list = get_product_list('아이폰14')

    for coupang in coupang_list:
        print(coupang)


if __name__ == "__main__":
    naver()
    goobne()
    coupang()