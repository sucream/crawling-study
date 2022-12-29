from .database import Base

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, unique=True, index=True)

    images = relationship("Image", back_populates="keyword")

    def __repr__(self):
        return f"Keyword(id={self.id}, keyword={self.keyword})"


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True)
    keyword_id = Column(Integer, ForeignKey("keywords.id"))

    keyword = relationship("Keyword", back_populates="images")

    def __repr__(self):
        return f"Image(id={self.id}, url={self.url}, keyword_id={self.keyword_id})"


print(__file__)
