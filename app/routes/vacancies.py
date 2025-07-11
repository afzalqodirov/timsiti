from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import Vacancies
from app.schemas import VacancySchema, VacancyResponse
from app.config import get_db

vacancy_router = APIRouter(prefix='/vacancies', tags=['Vacancies'])

@vacancy_router.get('/list', response_model=VacancyResponse)
def get_list_of_vacancies(db:Session = Depends(get_db)):
    try:
        return {"result":db.query(Vacancies).all()}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@vacancy_router.post('/add', response_model=VacancySchema)
def add_new_vacancy(vacancy:VacancySchema, db:Session = Depends(get_db)):
    try:
        if not db.query(Vacancies).filter_by(title=vacancy.title).first():
            new_vacancy = Vacancies(title=vacancy.title, link=str(vacancy.link))
            db.add(new_vacancy)
            db.commit()
            return vacancy
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    raise HTTPException(status_code=422, detail="The vacancy already exist")

@vacancy_router.delete('/delete/{id}')
def delete_vacancy(id:int, db:Session = Depends(get_db)):
    try:
        vacancy_exist = db.query(Vacancies).filter_by(id=id).delete()
        if vacancy_exist:
            db.commit()
            return {"msg":"Successfully deleted"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    raise HTTPException(status_code=404, detail="The vacancy not found")