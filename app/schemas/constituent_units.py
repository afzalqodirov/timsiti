from pydantic import BaseModel, EmailStr
from typing import List

class UnitsCreate(BaseModel):
    full_name:str
    job_title:str
    phone_number:str
    email:EmailStr

class UnitsBase(UnitsCreate):
    id:int
    image:str

class UnitsResponse(BaseModel):
    result:List[UnitsBase]
