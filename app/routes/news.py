from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.models import News, Languages
from app.schemas import NewsRetrieve
from app.config import get_db

news_router = APIRouter(prefix="/news", tags=["News"])

@news_router.post('/add')
def add_news(news:NewsRetrieve,  db: Session = Depends(get_db)):
    try:
        new_news = News(
            title_uz=news.title_uz,
            title_ru=news.title_ru,
            title_en=news.title_en,
            body_uz=news.body_uz,
            body_en=news.body_en,
            body_ru=news.body_ru,
            image=str(news.image),
            )
        db.add(new_news)
        db.commit()
        return {"msg":"Successfully added!"}
    except Exception as e:
        print(e)
        return {"msg":"The given news already exist!"}
    
@news_router.get('/list')
def news_list(lang:Languages = Query("uz"), db:Session = Depends(get_db)):
    try:
        to_return = {"uz":News.title_uz, "ru":News.title_ru, "en":News.title_en}
        return [{"id":i[0], "title":i[1]} for i in db.query(News.id, to_return[lang]).order_by(News.created_at).all()]
    except Exception as e:
        print(e)
        return {"msg":"Internal Server Error!"}
    
@news_router.get('/retrieve')
def news_detail(id:int, lang:Languages = Query("uz"), db:Session = Depends(get_db)):
    title = {"uz":News.title_uz, "ru":News.title_ru, "en":News.title_en}
    body = {"uz":News.body_uz, "ru":News.body_ru, "en":News.body_en}
    news = db.query(News.id, title[lang], body[lang], News.image, News.created_at).filter(News.id==id).one_or_none()
    if news:
        return {"id":news[0], "title":news[1], "content":news[2], "image":news[3], "created_at":news[4]}
    raise HTTPException(404, "Nothing has found")

@news_router.delete('/delete')
def news_delete(id:int, db:Session = Depends(get_db)):
    try:
        news = db.query(News).filter_by(id=id).delete()
        if news:
            db.commit()
            return {"msg":"Successfully deleted!"}
        return {"msg":f"Couldn't find the news with id {id}"}
    except Exception as e:
        print(e)
        return {"msg":"Internal Server Error!"}
