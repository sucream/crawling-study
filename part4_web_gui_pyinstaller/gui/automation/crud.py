from typing import Literal, Optional, List, Dict

from automation.models import Category, News, Comment
from automation.schemas import *
from automation.database import Session, init
from sqlalchemy import select, or_, and_


init()

# Category
def get_all_category_list() -> List[CategoryRead]:
    """
    ### 모든 카테고리 목록을 가져옵니다.
    """

    with Session() as session:
        stmt = select(Category)
        print(stmt)
        
        category_list: List[Category] = session.execute(stmt).scalars().all()

        if not category_list:
            return []

        return list(map(CategoryRead.from_orm, category_list))

def get_category_list_by_main_section(main_section: str) -> List[CategoryRead]:
    """
    메인 섹션에 해당하는 카테고리 목록을 가져옵니다.
    """
    
    with Session() as session:
        stmt = select(Category).where(Category.main_section == main_section)
        print(stmt)

        category_list = session.execute(stmt).scalars().all()
        if not category_list:
            return []

        return list(map(CategoryRead.from_orm, category_list))

def get_category_by_id(category_id: int) -> Optional[CategoryRead]:
    """
    ### 카테고리 ID에 해당하는 카테고리를 가져옵니다.
    """
    
    with Session() as session:
        stmt = select(Category).where(Category.id == category_id)
        return CategoryRead.from_orm(session.execute(stmt).scalars().first())

def create_new_category(category: CategoryCreate) -> CategoryRead:
    """
    ### 새로운 카테고리를 생성합니다.
    """
    
    with Session() as session:
        new_category = Category(**category.dict())
        session.add(new_category)
        session.commit()
        session.refresh(new_category)
        return CategoryRead.from_orm(new_category)

def update_category(category_id: int, update_category: CategoryUpdate) -> CategoryRead:
    selected_category = get_category_by_id(category_id)

    if selected_category is None:
        raise ValueError("Category not found")

    # 데이터 업데이트
    update_category_data = update_category.dict(exclude_unset=True)
    for key, value in update_category_data.items():
        setattr(selected_category, key, value)

    with Session() as session:
        session.add(selected_category)
        session.commit()
        session.refresh(selected_category)
        return CategoryRead.from_orm(selected_category)

def delete_category_by_id(category_id: int) -> bool:
    """
    ### 카테고리 ID에 해당하는 카테고리를 삭제합니다.
    """

    with Session() as session:
        selected_category = get_category_by_id(category_id)

        if selected_category is None:
            raise ValueError("Category not found")

        stmt = select(Category).where(Category.id == category_id)
        category = session.execute(stmt).scalars().first()

        session.delete(category)
        session.commit()

    return True


# News
def get_all_news_list() -> List[NewsRead]:
    """
    ### 모든 뉴스 목록을 가져옵니다.
    """

    with Session() as session:
        stmt = select(News)
        print(stmt)
        return list(map(NewsRead.from_orm, session.execute(stmt).scalars().all()))

def get_all_news_list_by_category_id(category_id: int) -> List[NewsRead]:
    """
    ### 카테고리 ID에 해당하는 뉴스 목록을 가져옵니다.
    """

    with Session() as db:
        stmt = select(News).where(News.category_id == category_id)
        print(stmt)
        return list(map(NewsRead.from_orm, db.execute(stmt).scalars().all()))

def get_news_by_id(news_id: int) -> Optional[NewsRead]:
    """
    ### 뉴스 ID에 해당하는 뉴스를 가져옵니다.
    """
    
    with Session() as session:
        stmt = select(News).where(News.id == news_id)
        return NewsRead.from_orm(session.execute(stmt).scalars().first())

def create_new_news(news: NewsCreate) -> NewsRead:
    """
    ### 새로운 뉴스를 생성합니다.
    """

    with Session() as db:
        new_news = News(**news.dict())
        db.add(new_news)
        db.commit()
        db.refresh(new_news)
        return NewsRead.from_orm(new_news)

def update_news(news_id: int, update_news: NewsUpdate) -> NewsRead:
    """
    ### 뉴스 ID에 해당하는 뉴스를 업데이트합니다.
    """
    selected_news = get_news_by_id(news_id)

    if selected_news is None:
        raise ValueError("News not found")

    # 데이터 업데이트
    update_news_data = update_news.dict(exclude_unset=True)
    for key, value in update_news_data.items():
        setattr(selected_news, key, value)

    with Session() as db:
        db.add(selected_news)
        db.commit()
        db.refresh(selected_news)
        return NewsRead.from_orm(selected_news)

def delete_news_by_id(news_id: int) -> bool:
    """
    ### 뉴스 ID에 해당하는 뉴스를 삭제합니다.
    """

    with Session() as db:
        stmt = select(News).where(News.id == news_id)
        news = db.execute(stmt).scalars().first()
        db.delete(news)
        db.commit()
        return True

def delete_all_news_by_category_id(category_id: int) -> bool:
    """
    ### 카테고리 ID에 해당하는 뉴스를 삭제합니다.
    """

    with Session() as db:
        stmt = select(News).where(News.category_id == category_id)
        news_list = db.execute(stmt).scalars().all()
        for news in news_list:
            db.delete(news)
        db.commit()
    
    return True

# Comment
