from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/v1/menus", response_model=list[schemas.MenuOut])
def read_menus(db: Session = Depends(get_db)):
    menus = crud.get_all_menus(db)
    for menu in menus:
        menu.id = str(menu.id)
    return menus


@app.post("/api/v1/menus", response_model=schemas.MenuOut, status_code=status.HTTP_201_CREATED)
def create_menu(menu: schemas.MenuBase, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_title(db, title=menu.title)
    if db_menu:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="menu already exist")
    db_output = crud.create_menu(db=db, menu=menu)
    db_output.id = str(db_output.id)
    return db_output


@app.get("/api/v1/menus/{menu_id}", response_model=schemas.MenuOut)
def read_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    db_menu.id = str(db_menu.id)
    return db_menu


@app.delete("/api/v1/menus/{menu_id}")
def delete_menu(menu_id: str, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    return crud.delete_menu(db=db, menu_id=menu_id)


@app.patch("/api/v1/menus/{menu_id}", response_model=schemas.MenuUpdate)
def update_menu(menu: schemas.MenuUpdate, menu_id: str, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    return crud.update_menu(db=db, menu=menu, menu_id=menu_id)


@app.get("/api/v1/menus/{menu_id}/submenus", response_model=list[schemas.SubmenuOut])
def read_submenus(menu_id: int, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=menu_id)
    submenus = crud.get_all_submenus(db, db_menu)
    # for submenu in submenus:
    #     submenu.id = str(submenu.id)
    result = [schemas.SubmenuOut(**submenu.__dict__) for submenu in submenus]
    return result


# @app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=schemas.SubmenuOut)
# def read_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
#     db_submenu = crud.get_submenu(db, menu_id=menu_id, submenu_id=submenu_id)
#     if db_submenu is None:
#         raise HTTPException(status_code=404, detail="menu not found")
#     db_submenu.id = str(db_submenu.id)
#     return db_submenu


# @app.post("/api/v1/menus/{menu_id}/submenus", response_model=schemas.SubmenuCreate, status_code=201)
# def create_submenu(menu_id: int, submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)):
#     db_submenu = crud.get_submenu_by_title(db, menu_id=menu_id, title=submenu.title)
#     if db_submenu:
#         raise HTTPException(status_code=400, detail="menu already exist")
#     db_submenu_output = crud.create_submenu(db, submenu=submenu)
#     db_submenu_output.id = str(db_submenu_output.id)
#     return db_submenu_output


# @app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
# def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
#     db_submenu = crud.get_submenu(db, menu_id=menu_id, submenu_id=submenu_id)
#     if db_submenu is None:
#         raise HTTPException(status_code=404, detail="menu not found")
#     return crud.delete_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)

    



