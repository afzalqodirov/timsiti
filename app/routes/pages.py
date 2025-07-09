from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import ResultSchema, MenusCreate, MenuBase, SubmenuCreate
from app.models import Pages, Menus, Submenus
from app.config import get_db

menus_router = APIRouter(prefix="/menus", tags=['menu'])

# ---------- MENUS ----------
@menus_router.get('/list', response_model=ResultSchema)
def get_menus_and_submenus(db:Session = Depends(get_db)):
    try:
        menus =  db.query(Menus).all()
        if menus:
            return {"result":menus}
        return {"result":[]}
    except Exception as e:
        print(e)
        return {"msg":"Internal Server Error"}

@menus_router.post('/add', response_model=MenuBase)
def add_menu( menus:MenusCreate,db:Session = Depends(get_db)):
    try:
        if db.query(Menus).filter(Menus.menu==menus.menu).first():
            raise HTTPException(status_code=422, detail="The menu already exist")
        menu = Menus(menu = menus.menu)
        db.add(menu)
        db.commit()
        db.refresh(menu)
        return menu
    except HTTPException:raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@menus_router.delete('/delete')
def delete_menu(id:int, db:Session = Depends(get_db)):
    menu = db.query(Menus).filter_by(id=id).delete()
    if menu:
        db.commit()
        return {"msg":"Successfully deleted"}
    raise HTTPException(status_code=404, detail=f"The menu is not found with id {id}")
# --------- END MENUS ----------


# --------- SUBMENUS -----------
submenu_router = APIRouter(prefix='/submenus', tags=['menu'])
@submenu_router.post('/add', response_model=SubmenuCreate)
def add_submenu(submenus:SubmenuCreate, db:Session = Depends(get_db)):
    try:
        menu = db.query(Menus).filter_by(id=submenus.menu_id).one_or_none()
        if not menu:
            raise HTTPException(status_code=422, detail=f"The menu doesn't exist with id {submenus.menu_id}")
        new_submenu = Submenus(submenu=submenus.submenu, menu=submenus.menu_id)
        db.add(new_submenu)
        db.commit()
        return {"submenu":submenus.submenu, "menu_id":submenus.menu_id}
    except HTTPException:raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@submenu_router.get('/list') # to check if the submenu added successfully
def get_submenus(db:Session = Depends(get_db)):
    return db.query(Submenus).all()

@submenu_router.delete('/delete')
def delete_submenu(id:int, db:Session = Depends(get_db)):
    try:
        submenu = db.query(Submenus).filter_by(id=id).delete()
        if submenu:
            db.commit()
            return {"msg":"Successfully deleted"}
        raise HTTPException(status_code=404, detail=f"The submenu is not found with id {id}")
    except HTTPException:raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
# ---------- END SUBMENUS ----------

# ---------- PAGES -------------
pages = APIRouter(prefix='/pages', tags=['Pages'])
pass