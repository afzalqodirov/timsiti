from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import uuid
import os

from app.config import get_db
from app.models import Leaderships
from app.schemas import LeadershipsBase

leaderships_router = APIRouter(prefix="/leaderships", tags=["Leaderships"])

@leaderships_router.patch("/update/image")
async def update_image(id:int, image:UploadFile = File(...), db:Session = Depends(get_db)):
    try:
        image.filename = f'{uuid.uuid4()}.jpg'
        contents = await image.read()
        image_name = f'app/images/{image.filename}'
        with open(image_name, 'wb') as file:
            file.write(contents)
        leader = db.query(Leaderships).filter_by(id=id).first()
        if not leader:
            raise HTTPException(status_code=404, detail="The leader not found")
        if str(leader.image)[-11:] != 'default.jpg':
            # to not store all the images!
            os.remove(str(leader.image))
        setattr(leader, "image", image_name)
        db.commit()
        db.refresh(leader)
        return {"msg":"Success!"}
    except HTTPException:raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error!")
    
@leaderships_router.post('/add/member')
def add_member(leader:LeadershipsBase, db:Session = Depends(get_db)):
    try:
        new_leader = Leaderships(
            full_name=leader.full_name,
            job_title=leader.job_title,
            reception_days=leader.reception_days,
            phone_number=leader.phone_number,
            email=leader.email,
            bachelor_speciality=leader.bachelor_speciality,
        )
        db.add(new_leader)
        db.commit()
        return leader
    except Exception as e:
        print(e)
        raise HTTPException(status_code=422, detail="The leader already exist")
    
@leaderships_router.get("/members")
def list_members(db:Session = Depends(get_db)):
    return db.query(Leaderships).all()

@leaderships_router.get("/member/image")
def get_image_by_id(id:int, db:Session = Depends(get_db)):
    try:
        leader = db.query(Leaderships.image).filter_by(id=id).first()
        if not leader:
            raise HTTPException(status_code=404, detail="The leader not found")
        return FileResponse(leader[0])
    except HTTPException:raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@leaderships_router.delete("/member/delete")
def delete_member_by_id(id:int, db:Session = Depends(get_db)):
    try:
        leader = db.query(Leaderships).filter_by(id=id).first()
        if leader:
            # extra trash removing
            os.remove(str(leader.image))
            db.delete(leader)
            db.commit()
            return {"msg":"Successfully deleted"}
        raise HTTPException(detail="The leader not found", status_code=404)
    except HTTPException:raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")