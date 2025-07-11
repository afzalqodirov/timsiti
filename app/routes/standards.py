from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import uuid
import os

from app.config import get_db
from app.schemas import StandardCreate, StandardResponse
from app.models import Standards

standards_router = APIRouter(prefix='/standards', tags=['Standards'])

@standards_router.get('/list', response_model=StandardResponse)
def get_list_of_standards(db:Session = Depends(get_db)):
    try:
        return {"result":db.query(Standards).all()}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@standards_router.post('/add')
def add_standard(standard:StandardCreate, db:Session = Depends(get_db)):
    try:
        new_standard = Standards(title=standard.title, content_title=standard.content_title)
        db.add(new_standard)
        db.commit()
        return standard
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@standards_router.post('/add/pdf/{id}')
async def add_or_update_pdf(id:int, pdf:UploadFile = File(...), db:Session = Depends(get_db)):
    try:
        standard = db.query(Standards).filter_by(id=id).first()
        if not standard:
            raise HTTPException(status_code=404, detail="The standard not found")
        if pdf.filename and pdf.filename[-4:] != '.pdf':
            raise HTTPException(status_code=422, detail="Send pdf file!")
        contents = await pdf.read()
        pdf_filename = f'{uuid.uuid4()}.pdf'
        with open('app/pdf_files/' + pdf_filename, 'wb') as file:
            file.write(contents)
        if str(standard.pdf)[-11:] != 'default.pdf':
            # trash removing
            os.remove('app/pdf_files/' + str(standard.pdf))
        setattr(standard, 'pdf', pdf_filename)
        db.commit()
        return {"msg":"Successfully uploaded"}
    except HTTPException:raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@standards_router.get('/pdf/{id}',deprecated=True, summary="Don't use it! It may crash the browser", 
                      response_description="<h1>If the pdf is not light, this will crash your browser(on swagger)!</h1>" \
                      "<p>If still curious, check with default.pdf (hehehe)</p>")
def pdf_by_standards_id(id:int, db:Session = Depends(get_db)):
    try:
        pdf = db.query(Standards.pdf).filter_by(id=id).first()
        if not pdf:
            raise HTTPException(status_code=404, detail="The pdf not found")
        return FileResponse('app/pdf_files/'+ pdf[0])
    except HTTPException:raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@standards_router.delete('/delete/{id}')
def delete_standard_by_id(id:int, db:Session = Depends(get_db)):
    try:
        standard_exist = db.query(Standards).filter_by(id=id).first()
        if standard_exist:
            if str(standard_exist.pdf) != 'default.pdf':
                os.remove('app/pdf_files/' + str(standard_exist.pdf))
            db.delete(standard_exist)
            db.commit()
            return {"msg":"Successfully deleted!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    raise HTTPException(status_code=404, detail="The standard not found")