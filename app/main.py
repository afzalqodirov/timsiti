from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from .config import engine, SECRET_KEY, ALGORITHM, Base, get_db
from .routes import (
    user_router, 
    news_router, 
    menus_router, 
    submenu_router, 
    pages_router
    )
from .models import User

app = FastAPI(
    description="""
## Docs
The github repository is available on this <a href="https://github.com/afzalqodirov/timsiti">**_link_**</a>

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
    """,
    title="The TMSITI api", 
    version="v0.9", 
    docs_url='/', 
    redoc_url=None, 
    contact={"name":"Afzal","url":"https://t.me/Afzal006", "email":"htpafzal@gmail.com"},
    swagger_ui_parameters={"syntaxHighlight":{"theme":"github"}, "useUnsafeMarkdown": True},
    openapi_tags=[
        {"name":"Menus", "description":"The menus and submenus routers"},
        {"name":"Pages", "description":"The routes for static pages"},
        {"name":"News", "description":"The newest news"},
        {"name":"default", "description":"The default routes to handle authorization"},
    ]
    )
Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# routers
app.include_router(user_router)
app.include_router(pages_router)
app.include_router(news_router)
app.include_router(menus_router)
app.include_router(submenu_router)

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
