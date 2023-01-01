import logging

from . import models

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)

SQLALCHEMY_DATABASE_URL = "sqlite:///./crawl.db"

# DB 연결
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# DB 세션 생성기 세팅
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session: sessionmaker = scoped_session(SessionLocal)

# ORM 모델을 만들기 위한 Base 클래스
Base = declarative_base()


def init():
    """
    데이터베이스 설정 부분
    """
    models.Base.metadata.create_all(bind=engine)