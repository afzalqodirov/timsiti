from sqlalchemy import Column, Integer, String, Date, Text
from app.config.database import Base
from datetime import datetime
from enum import Enum


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    title_uz = Column(String, index=True, unique=True)
    title_ru = Column(String, index=True, unique=True)
    title_en = Column(String, index=True, unique=True)

    # ckeditor or similar can be added, that's why it's text field
    body_uz = Column(Text)
    body_ru = Column(Text)
    body_en = Column(Text)

    # image url only https://...
    image = Column(String)
    created_at = Column(Date, default=datetime.now())

class Languages(str, Enum):
    uz = "uz"
    ru = "ru"
    en = "en"