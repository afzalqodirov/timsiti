from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from dotenv import load_dotenv
from os import getenv
import requests

from .schemas import Message
from .config import engine, SECRET_KEY, ALGORITHM, Base, get_db
from .routes import (
    user_router, 
    news_router, 
    menus_router, 
    submenu_router, 
    pages_router,
    leaderships_router,
    units_router,
    vacancy_router,
    standards_router
    )
from .models import User
load_dotenv()
app = FastAPI(
    description="""
## Docs
The github repository is available on this <a href="https://github.com/afzalqodirov/timsiti">**_link_**</a>

The original site is available by this <a href="https://tmsiti.uz/">**_link_**</a>

The original site-**backend** is available by this <a href="https://backend.tmsiti.uz/api/v1/swagger/">**_link_**</a>

The description usage on <span style='color:green'>**FastAPI**</span> i learnt from this <a href="https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api">**_link_**</a>
    
## Special Thanks to
**Sarvarbek Azimov** my precious teacher from **python**

He taught me:
* Django
* Django rest-framework
* Fastapi
* How to use ai prompts to reach the goals
* Finally how to set up the server and also _Linux_

If you need the teacher from python here's the <a href="https://t.me/SarvarAzim">**_link_**</a> for his telegram

**(the exam task is not finished yet)**
    """,
    title="🏛️ The TMSITI api", 
    version="v1.1", 
    docs_url='/', 
    redoc_url=None, 
    contact={"name":"Afzal","url":"https://t.me/Afzal006", "email":"htpafzal@gmail.com"},
    swagger_ui_parameters={"syntaxHighlight":{"theme":"github"}, "useUnsafeMarkdown": True},
    openapi_tags=[
        {"name":"Menus", "description":"The menus and submenus routers"},
        {"name":"Pages", "description":"The routes for static pages (Statik sahifalar uchun)"},
        {"name":"News", "description":"The newest news"},
        {"name":"Leaderships", "description":"The leaderships router (Rahbariyatlar)"},
        {"name":"Units", "description":"The units router (Bo'linmalar)"},
        {"name":"Vacancies", "description":"The vacancies router (Vakansiyalar)","externalDocs": {"description": "Example url","url": "https://hh.uz"}},
        {"name":"Standards", "description":"The standards router (Standardlar)"},
        {"name":"default", "description":"The default routes to handle authorization"},
    ]
    )
app.mount('/images', StaticFiles(directory='./app/images'), name='static')
Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
# the bot's token which will send the message
bot_token=getenv('Bot_token')
# the reciever's id, by default it is Afzal's id
tg_id=getenv('tg_id', '716756079')

# routers
routers = [units_router, user_router, pages_router, menus_router, news_router, submenu_router, leaderships_router, vacancy_router, standards_router]
for router in routers:
    app.include_router(router=router)

@app.post('/send_message')
def telegram_message(message:Message):
    try:
        text = f"Full name: {message.first_name} {message.last_name}\n"\
        f"Message: {message.message}\n"\
        f"Email: {message.email}\n"\
        f"PhoneNumber: {message.phone_number}"
        response = requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={tg_id}&text={text}')
        if response.status_code == 200:
            return {"msg":"Successfully sent to Afzal"}
        return response.json()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/profile")
def profile(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"username": user.username, "message": "Authenticated!"}
