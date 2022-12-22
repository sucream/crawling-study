from .database import Base

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Keyword(Base):
    """
    키워드 저장 테이블

    id: 키워드 고유 ID
    keyword: 키워드, 중복 불가
    images: 키워드에 해당하는 이미지 목록
    """

    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    keyword = Column(String, unique=True, index=True)

    images = relationship("Image", back_populates="keyword")

    def __repr__(self):
        return f"Keyword(id={self.id}, keyword={self.keyword})"


class Image(Base):
    """
    이미지 저장 테이블

    id: 이미지 고유 ID
    url: 이미지 URL, 중복 불가
    keyword_id: 키워드 ID
    keyword: 키워드
    """

    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    url = Column(String, unique=True)
    keyword_id = Column(Integer, ForeignKey("keywords.id"))

    keyword = relationship("Keyword", back_populates="images")

    def __repr__(self):
        return f"Image(id={self.id}, url={self.url}, keyword_id={self.keyword_id})"