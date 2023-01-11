from typing import List
import datetime

from automation import crud, schemas
from automation.crawl import naver_news

from fastapi import FastAPI, HTTPException, Path, Query, Body
from sqlalchemy.exc import IntegrityError


app = FastAPI(
    title="네이버 뉴스 크롤러",
)


@app.get(
    "/category",
    response_model=List[schemas.CategoryRead],
    tags=["category"],
    summary="모든 카테고리 목록을 가져옵니다.",
)
def list_all_category():
    """
    ### 모든 카테고리 목록을 가져옵니다.
    """
    return crud.get_all_category_list()

@app.post(
    "/category",
    response_model=schemas.CategoryRead,
    tags=["category"],
    summary="새로운 카테고리를 생성합니다.",
)
def create_new_category(category: schemas.CategoryCreate):
    """
    ### 새로운 카테고리를 생성합니다.
    """

    try:
        new_category = crud.create_new_category(category)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail="이미 존재하는 카테고리입니다.")
    return new_category

@app.get(
    "/category/{category_id}",
    response_model=schemas.CategoryRead,
    tags=["category"],
    summary="카테고리 ID에 해당하는 카테고리를 가져옵니다.",
)
def get_category_by_id(category_id: int):
    """
    ### 카테고리 ID에 해당하는 카테고리를 가져옵니다.
    """
    category = crud.get_category_by_id(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다.")
    return category

@app.get(
    "/category/main-section/{main_section}",
    response_model=List[schemas.CategoryRead],
    tags=["category"],
    summary="메인 섹션에 해당하는 카테고리 목록을 가져옵니다.",
)
def get_category_list_by_main_section(main_section: str):
    """
    ### 메인 섹션에 해당하는 카테고리 목록을 가져옵니다.
    """
    return crud.get_category_list_by_main_section(main_section)

@app.delete(
    "/category/{category_id}",
    response_model=bool,
    tags=["category"],
    summary="카테고리 ID에 해당하는 카테고리를 삭제합니다.",
)
def delete_category_by_id(category_id: int):
    """
    ### 카테고리 ID에 해당하는 카테고리를 삭제합니다.
    """

    try:
        category = crud.get_category_by_id(category_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다.")

    if category is None:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다.")

    if category.news_list:
        raise HTTPException(
            status_code=409, detail="카테고리에 속한 뉴스가 존재합니다."
        )

    return crud.delete_category_by_id(category_id)

@app.get(
    "/category/{category_id}/news",
    response_model=List[schemas.NewsRead],
    tags=["news"],
    summary="카테고리 ID에 해당하는 뉴스 목록을 가져옵니다.",
)
def get_news_list_by_category_id(category_id: int):
    """
    ### 카테고리 ID에 해당하는 뉴스 목록을 가져옵니다.
    """
    return crud.get_all_news_list_by_category_id(category_id)

@app.post(
    "/category/{category_id}/news",
    response_model=schemas.NewsRead,
    tags=["news"],
    summary="카테고리 ID에 해당하는 뉴스를 생성합니다.",
)
def create_new_news(category_id: int, news: schemas.NewsCreate):
    """
    ### 카테고리 ID에 해당하는 뉴스를 생성합니다.
    """
    try:
        new_news = crud.create_new_news(category_id, news)
    except Exception as e:
        raise HTTPException(status_code=409, detail="이미 존재하는 뉴스입니다.")
    return new_news

@app.post(
    "/category/{category_id}/news/fetch",
    response_model=List[schemas.NewsRead],
    tags=["news"],
    summary="카테고리 ID에 해당하는 뉴스를 크롤링하여 생성합니다.",
)
def fetch_news(
    category_id: int,
    fetch_date: str = Query(
        default=datetime.date.today().strftime("%Y%m%d"),
        title="날짜",
        description="크롤링할 날짜를 입력합니다. 기본값은 오늘입니다.",
    )
):
    """
    ### 카테고리 ID에 해당하는 뉴스를 크롤링하여 생성합니다.
    """

    try:
        category = crud.get_category_by_id(category_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다.")

    news_list = naver_news.get_news_list(category.main_section, category.sub_section, fetch_date)

    result = []

    for news in news_list:
        try:
            news_obj = schemas.NewsCreate(title=news["title"], url=news["url"], publisher=news["publisher"], date=news["date"], category_id=category_id)
            result.append(crud.create_new_news(news_obj))
        except IntegrityError as e:
            pass

    return result

@app.get(
    "/category/{category_id}/news/{news_id}",
    response_model=schemas.NewsRead,
    tags=["news"],
    summary="카테고리 ID에 해당하고 뉴스 ID에 해당하는 뉴스를 가져옵니다.",
)
def get_news_by_id(category_id: int, news_id: int):
    """
    ### 카테고리 ID에 해당하고 뉴스 ID에 해당하는 뉴스를 가져옵니다.
    """

    try:
        category = crud.get_category_by_id(category_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다.")

    news = crud.get_news_by_id(news_id)
    if news is None:
        raise HTTPException(status_code=404, detail="뉴스를 찾을 수 없습니다.")
    return news

@app.delete(
    "/category/{category_id}/news",
    response_model=bool,
    tags=["news"],
    summary="카테고리 ID에 해당하는 뉴스를 모두 삭제합니다.",
)
def delete_news_by_category_id(category_id: int):
    """
    ### 카테고리 ID에 해당하는 뉴스를 모두 삭제합니다.
    """

    try:
        category = crud.get_category_by_id(category_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다.")

    try:
        crud.delete_all_news_by_category_id(category_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="뉴스를 삭제하는데 실패했습니다.")

    return True