import logging

from .database import DBSession, engine
from . import models, schemas


logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# models.Base.metadata.create_all(bind=engine)


def create_keyword(keyword: schemas.KeywordCreate):
    with DBSession() as db:
        new_keyword = models.Keyword(**keyword.dict())
        db.add(new_keyword)
        db.commit()
        db.refresh(new_keyword)
        return new_keyword

def get_keyword_list():
    with DBSession() as db:
        return list(map(schemas.KeywordRead.from_orm, db.query(models.Keyword).all()))

def get_keyword_by_keyword(keyword: str):
    with DBSession() as db:
        return schemas.KeywordRead.from_orm(db.query(models.Keyword).filter(models.Keyword.keyword == keyword).first())


def create_image(image: schemas.ImageCreate):
    with DBSession() as db:
        new_image = models.Image(**image.dict())
        db.add(new_image)
        db.commit()
        db.refresh(new_image)
        return schemas.ImageRead.from_orm(new_image)

def get_image_list():
    with DBSession() as db:
        return list(map(schemas.ImageRead.from_orm, db.query(models.Image).all()))

def get_image_by_url(url: str):
    with DBSession() as db:
        return schemas.ImageRead.from_orm(db.query(models.Image).filter(models.Image.url == url).first())