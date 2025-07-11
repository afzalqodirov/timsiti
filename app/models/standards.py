from sqlalchemy import Column, String, Integer
from app.config import Base

class Standards(Base):
    __tablename__ = 'standards'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    # Laws number (Ex:O'zMst 103:2024)
    title = Column(String)
    # the title of it's content (Alyuminiy qotishmalari)
    content_title = Column(String)
    pdf = Column(String, default='default.pdf')