from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from .config import engine, SECRET_KEY, ALGORITHM, Base, get_db
from .routes import user_router, news_router
from .models import User


app = FastAPI()
Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# routers
app.include_router(user_router)
app.include_router(news_router)

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

@app.get("/")
def greeting():return {"msg":"Hellou"}
