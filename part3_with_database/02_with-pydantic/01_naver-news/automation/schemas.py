from __future__ import annotations
from typing import List, Optional

from pydantic import BaseModel


# 카테고리 스키마
class CategoryBase(BaseModel):
    """
    카테고리 기본 스키마
    """
    main_section: str
    sub_section: str
    category_name: str

class CategoryCreate(CategoryBase):
    """
    카테고리 생성 스키마
    """
    pass

class CategoryRead(CategoryBase):
    """
    카테고리 조회 스키마
    """
    id: int
    news_list: List[Optional[NewsRead]]

    class Config:
        orm_mode = True

class CategoryUpdate(CategoryBase):
    """
    카테고리 수정 스키마
    """
    main_section: Optional[str] = None
    sub_section: Optional[str] = None
    category_name: Optional[str] = None


# 뉴스 스키마
class NewsBase(BaseModel):
    """
    뉴스 기본 스키마
    """
    title: str
    url: str
    publisher: str
    date: str
    content: str
    note: str
    category_id: int

class NewsCreate(NewsBase):
    """
    뉴스 생성 스키마
    """
    content: Optional[str] = None
    note: Optional[str] = None

class NewsRead(NewsBase):
    """
    뉴스 조회 스키마
    """
    id: int
    title: Optional[str] = None
    url: Optional[str] = None
    publisher: Optional[str] = None
    date: Optional[str] = None
    content: Optional[str] = None
    note: Optional[str] = None
    comments: List[CommentRead]

    class Config:
        orm_mode = True

class NewsUpdate(NewsBase):
    """
    뉴스 수정 스키마
    """
    title: Optional[str] = None
    url: Optional[str] = None
    publisher: Optional[str] = None
    date: Optional[str] = None
    content: Optional[str] = None
    note: Optional[str] = None
    category_id: Optional[int] = None


# 댓글 스키마
class CommentBase(BaseModel):
    """
    댓글 기본 스키마
    """
    nickname: str
    content: str
    date: str
    like: int
    news_id: int

class CommentCreate(CommentBase):
    """
    댓글 생성 스키마
    """
    pass

class CommentRead(CommentBase):
    """
    댓글 조회 스키마
    """
    id: int

    class Config:
        orm_mode = True

class CommentUpdate(CommentBase):
    """
    댓글 수정 스키마
    """
    nickname: Optional[str] = None
    content: Optional[str] = None
    date: Optional[str] = None
    like: Optional[int] = None
    news_id: Optional[int] = None


CategoryRead.update_forward_refs()
NewsRead.update_forward_refs()