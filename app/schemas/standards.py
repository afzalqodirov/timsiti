from pydantic import BaseModel
from typing import List, Optional

class StandardCreate(BaseModel):
    title:str
    content_title:str

class StandardBase(StandardCreate):
    id:int
    pdf:str = 'default.pdf'

class StandardResponse(BaseModel):
    result:List[StandardBase]