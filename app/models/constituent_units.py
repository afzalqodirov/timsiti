from app.config import Base
from sqlalchemy import Column, String, Integer

class Units(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_title = Column(String)
    full_name = Column(String)
    phone_number = Column(String)
    email = Column(String)
    image = Column(String, default="/images/default.jpg")