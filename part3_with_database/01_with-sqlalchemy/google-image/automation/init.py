import logging

from .database import engine
from . import models


logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)

def init():
    models.Base.metadata.create_all(bind=engine)