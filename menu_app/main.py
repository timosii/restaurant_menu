from fastapi import Depends, FastAPI, HTTPException
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


@app.get("/api/v1/menus", response_model=list[schemas.Menu])
def read_menus(db: Session = Depends(get_db)):
    menus = crud.get_all_menus(db)
    return menus


@app.post("/api/v1/menus", response_model=schemas.Menu, status_code=201)
def create_menu(menu: schemas.Menu, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_title(db, title=menu.title)
    if db_menu:
        raise HTTPException(status_code=400, detail="menu already exist")
    db_output = crud.create_menu(db=db, menu=menu)
    db_output.id = str(db_output.id)
    return db_output


@app.get("/api/v1/menus/{menu_id}", response_model=schemas.Menu)
def read_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    db_menu.id = str(db_menu.id)
    return db_menu


@app.delete("/api/v1/menus/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return crud.delete_menu(db=db, menu_id=menu_id)


@app.patch("/api/v1/menus/{menu_id}", response_model=schemas.Menu)
def update_menu(menu: schemas.Menu, menu_id: int, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")

    return crud.update_menu(db=db, menu=menu, menu_id=menu_id)

