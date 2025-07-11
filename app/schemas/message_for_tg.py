from pydantic import BaseModel, EmailStr

class Message(BaseModel):
    first_name:str = "Afzal"
    last_name:str = "Qodirov"
    message:str = "Woow, You have learnt Telegram messaging by using requests!"
    email:EmailStr
    phone_number:str = "999999999"