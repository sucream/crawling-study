import logging

from .database import Session, engine
from . import models


# CREATE
def create_keyword(new_keyword: str):
    with Session() as db:
        new_keyword = models.Keyword(keyword=new_keyword)
        db.add(new_keyword)
        db.commit()
        db.refresh(new_keyword)
        return new_keyword

# READ
def get_keyword_list():
    with Session() as db:
        return db.query(models.Keyword).all()

def get_keyword_by_keyword(keyword: str):
    with Session() as db:
        return db.query(models.Keyword).filter(models.Keyword.keyword == keyword).first()

def create_image(url: str, keyword_id: int):
    with Session() as db:
        new_image = models.Image(url=url, keyword_id=keyword_id)
        db.add(new_image)
        db.commit()
        db.refresh(new_image)
        return new_image

def get_image_list():
    with Session() as db:
        return db.query(models.Image).all()

def get_images_by_keyword_id(keyword_id: int):
    with Session() as db:
        return db.query(models.Image).filter(models.Image.keyword_id == keyword_id).all()

# UPDATE

# DELETE
def delete_keyword(keyword: str):
    with Session() as db:
        keyword_item = 
        db.delete(keyword_item)
        db.commit()
        return True