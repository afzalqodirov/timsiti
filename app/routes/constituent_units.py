from fastapi import APIRouter, Depends, HTTPException, UploadFile,File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import uuid
import os

from app.config import get_db
from app.schemas import UnitsCreate, UnitsResponse
from app.models import Units

units_router = APIRouter(prefix='/units', tags=["Units"])

@units_router.get('/list', response_model=UnitsResponse)
def get_list_units(db:Session = Depends(get_db)):
    try:
        return {'result':db.query(Units).all()}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@units_router.post('/add')
def add_unit_member(units:UnitsCreate, db:Session = Depends(get_db)):
    try:
        new_unit = Units(full_name=units.full_name, job_title=units.job_title, email=units.email, phone_number=units.phone_number)
        db.add(new_unit)
        db.commit()
        return units
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@units_router.delete('/delete/{id}')
def delete_unit_member(id:int, db:Session = Depends(get_db)):
    try:
        unit = db.query(Units).filter_by(id=id).first()
        if unit:
            if str(unit.image)[-11:] != 'default.jpg':
                os.remove('app/' + str(unit.image))
            db.delete(unit)
            db.commit()
            return {"msg":"Successfully deleted"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    raise HTTPException(status_code=404, detail="The unit doesn't exist")

@units_router.patch('/update/image/{id}')
async def add_or_update_image_by_id(id:int, image:UploadFile = File(...), db:Session = Depends(get_db)):
    try:
        unit = db.query(Units).filter_by(id=id).first()
        if not unit:
            raise HTTPException(status_code=404, detail="The unit not found")
        if image.filename and image.filename[-4:] not in (".jpg", "jpeg", '.png'):
            raise HTTPException(status_code=422, detail="Send the Photo!")
        image.filename = f'{uuid.uuid4()}.jpg'
        content = await image.read()
        with open('app/images/' + image.filename, 'wb') as file:
            file.write(content)
        os.remove("app/" + str(unit.image))
        setattr(unit, 'image', '/images/' + image.filename)
        db.commit()
        db.refresh(unit)
        return {"msg":"Successfully updated"}
    except HTTPException:raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@units_router.get('/image/{id}')
def get_photo_by_id(id:int, db:Session = Depends(get_db)):
    try:
        unit = db.query(Units.image).filter_by(id=id).first()
        if unit:
            return FileResponse("app/" + unit[0])
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    raise HTTPException(status_code=404, detail="The unit not found")