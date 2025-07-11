from sqlalchemy import Column, Integer, String
from app.config import Base

class Vacancies(Base):
    __tablename__ = 'vacancies'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    # the 255 characters will be enough for vacancy links on hh.uz or similar
    link = Column(String)