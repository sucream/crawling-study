from .database import engine
from . import models

def init():
    models.Base.metadata.create_all(bind=engine)