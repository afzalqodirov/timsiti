from pydantic import BaseModel, EmailStr

class LeadershipsBase(BaseModel):
    full_name:str
    job_title:str
    reception_days:str
    phone_number:str
    email:EmailStr
    bachelor_speciality:str