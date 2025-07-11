from pydantic import BaseModel, HttpUrl
from typing import List

class VacancySchema(BaseModel):
    title:str
    link:HttpUrl

class VacancyFull(VacancySchema):
    id:int

class VacancyResponse(BaseModel):
    result:List[VacancyFull]