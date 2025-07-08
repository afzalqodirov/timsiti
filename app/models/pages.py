from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.config import Base

class Menus(Base):
    id = Column(Integer)
    submenus = relationship("Submenus", back_populates="smth")

class Submenus(Base):pass

class Pages(Base):
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    menu = Column()