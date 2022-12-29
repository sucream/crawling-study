from datetime import datetime

from .database import Base

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class BaseModel(Base):
    """
    ### 모든 테이블에 공통으로 들어가는 컬럼 정의
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Category(BaseModel):
    """
    ### 카테고리 저장 테이블

    Parameters
    ----------
    main_section : str
        대분류
    sub_section : str
        소분류
    category_name : str
        카테고리 이름

    """

    __tablename__ = "category"

    main_section = Column(String, index=True)
    sub_section = Column(String, unique=True, index=True)
    category_name = Column(String, unique=True, index=True)

    news = relationship("News", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, main_section={self.main_section}, sub_section={self.sub_section}, category_name={self.category_name})>"


class News(BaseModel):
    """
    뉴스 저장 테이블

    id: 뉴스 고유 ID
    title: 키워드, 중복 불가
    images: 키워드에 해당하는 이미지 목록
    """

    __tablename__ = "news"

    title = Column(String, index=True)
    url = Column(String, unique=True)
    publisher = Column(String)
    date = Column(String)
    content = Column(Text)
    note = Column(String)
    category_id = Column(Integer, ForeignKey("category.id"))

    category = relationship("Category", back_populates="news")
    comments = relationship("Comment", back_populates="news")

    def __repr__(self):
        return f"<News (id={self.id}, title={self.title}, url={self.url}, date={self.date}, content={self.content})>"


class Comment(BaseModel):
    """
    ### 댓글 저장 테이블

    Parameters
    ----------
    nickname : str
        댓글 작성자
    content : str
        댓글 내용
    date : str
        댓글 작성일
    like : int
        댓글 좋아요 수
    dislike : int
        댓글 싫어요 수
    """

    __tablename__ = "comment"

    nickname = Column(String)
    content = Column(Text)
    date = Column(String)
    like = Column(Integer)
    dislike = Column(Integer)
    news_id = Column(Integer, ForeignKey("news.id"))

    news = relationship("News", back_populates="comments")


    def __repr__(self):
        return f"<Comment (id={self.id}, nickname={self.nickname}, content={self.content}, date={self.date}, like={self.like}, dislike={self.dislike})>"