from sqlalchemy import Column, String, Integer

from app.config import Base

class Leaderships(Base):
    __tablename__ = 'leaderships'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    full_name = Column(String, unique=True)
    job_title = Column(String)
    reception_days = Column(String)
    phone_number = Column(String)
    email = Column(String)
    bachelor_speciality = Column(String)
    image = Column(String, default='app/images/default.jpg')