from typing import Literal, Optional, List, Dict

from automation.models import Category, News, Comment
from automation.database import Session, init
from sqlalchemy import select, or_, and_


init()

# Category
def get_all_category_list():
    """
    ### 모든 카테고리 목록을 가져옵니다.
    """

    with Session() as session:
        stmt = select(Category)
        print(stmt)
        return session.execute(stmt).scalars().all()

def get_category_list_by_main_section(main_section: str):
    """
    메인 섹션에 해당하는 카테고리 목록을 가져옵니다.
    """
    
    with Session() as db:
        stmt = select(Category).where(Category.main_section == main_section)
        print(stmt)
        return db.execute(stmt).scalars.all()

def get_category_by_id(category_id: int) -> Optional[Category]:
    """
    ### 카테고리 ID에 해당하는 카테고리를 가져옵니다.
    """
    
    with Session() as db:
        stmt = select(Category).where(Category.id == category_id)
        return db.execute(stmt).scalars().first()

def create_new_category(main_section: str, sub_section: str, category_name: str):
    """
    ### 새로운 카테고리를 생성합니다.
    """
    
    with Session() as db:
        new_category = Category(main_section=main_section, sub_section=sub_section, category_name=category_name)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category


# News
def get_all_news_list():
    """
    ### 모든 뉴스 목록을 가져옵니다.
    """

    with Session() as session:
        stmt = select(News)
        print(stmt)
        return session.execute(stmt).scalars().all()

def get_all_news_list_by_category_id(category_id: int):
    """
    ### 카테고리 ID에 해당하는 뉴스 목록을 가져옵니다.
    """

    with Session() as db:
        stmt = select(News).where(News.category_id == category_id)
        print(stmt)
        return db.execute(stmt).scalars().all()

def create_new_news(category_id: int, title: str, content: str, url: str, date: str):
    """
    ### 새로운 뉴스를 생성합니다.
    """

    with Session() as db:
        new_news = News(category_id=category_id, title=title, content=content, url=url, date=date)
        db.add(new_news)
        db.commit()
        db.refresh(new_news)
        return new_news

def delete_news_by_id(news_id: int):
    """
    ### 뉴스 ID에 해당하는 뉴스를 삭제합니다.
    """

    with Session() as db:
        stmt = select(News).where(News.id == news_id)
        news = db.execute(stmt).scalars().first()
        db.delete(news)
        db.commit()
        return True

def delete_news_by_category_id(category_id: int):
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
def get_all_comment_list():
    """
    ### 모든 댓글 목록을 가져옵니다.
    """

    with Session() as session:
        stmt = select(Comment)
        print(stmt)
        return session.execute(stmt).scalars().all()

def get_all_comment_list_by_news_id(news_id: int):
    """
    ### 뉴스 ID에 해당하는 댓글 목록을 가져옵니다.
    """

    with Session() as db:
        stmt = select(Comment).where(Comment.news_id == news_id)
        print(stmt)
        return db.execute(stmt).scalars().all()

