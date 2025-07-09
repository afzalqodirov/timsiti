from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.config import Base

class Menus(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    menu = Column(String, index=True)

    submenus_obj = relationship("Submenus", back_populates="menus_obj")

class Submenus(Base):
    __tablename__ = "submenus"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    submenu = Column(String, index=True)
    menu = Column(Integer, ForeignKey('menus.id'))

    menus_obj = relationship("Menus", back_populates="submenus_obj")
    pages = relationship("Pages", back_populates="submenu_obj")

class Pages(Base):
    __tablename__ = 'pages'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    submenu = Column(Integer, ForeignKey('submenus.id'))

    submenu_obj = relationship("Submenus", back_populates="pages")