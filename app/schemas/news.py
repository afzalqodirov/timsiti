from pydantic import BaseModel, HttpUrl
from datetime import datetime

class NewsList(BaseModel):
    image:HttpUrl
    # frontend's side should change the language like (if uz -> title_uz)
    title_uz:str
    title_ru:str
    title_en:str

class NewsRetrieve(NewsList):
    body_uz:str
    body_ru:str
    body_en:str

class NewsBase(NewsRetrieve):
    id:int
    created_at:datetime

    class Config:
        from_orm = True