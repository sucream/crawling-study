from typing import List, Union, Optional

from pydantic import BaseModel


class KeywordBase(BaseModel):
    keyword: str

class KeywordCreate(KeywordBase):
    pass

class KeywordRead(KeywordBase):
    id: int

    class Config:
        orm_mode = True


class ImageBase(BaseModel):
    url: str
    keyword_id: int

class ImageCreate(ImageBase):
    pass

class ImageRead(ImageBase):
    id: int

    class Config:
        orm_mode = True

print(__file__)