from pydantic import BaseModel
from typing import List

class PagesSchema(BaseModel):
    id:int
    title:str
    content:str
    submenu:int

class SubmenusBase(BaseModel):
    id:int
    submenu:str

class MenuBase(BaseModel):
    id:int
    menu:str

class MenusSchema(MenuBase):
    submenus_obj:List[SubmenusBase] = []

    class Config:
        from_orm = True

class ResultSchema(BaseModel):
    result:List[MenusSchema]

class MenusCreate(BaseModel):
    menu:str

    class Config:
        from_orm = True

class SubmenuCreate(BaseModel):
    submenu:str
    menu_id:int
    class Config:
        from_orm = True