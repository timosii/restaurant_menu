from .. import schemas, models
from ..cruds.menu import (get_menu,
                          get_menus,
                          create_menu,
                          update_menu,
                          delete_menu,
                          submenu_dish_count)
from ..database import engine, get_db
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import Depends, status, APIRouter


models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/api/v1/menus")


@router.get("/", response_model=list[schemas.MenuOut])
def reading_menus(db: Session = Depends(get_db)):
    menus = get_menus(db)
    for menu in menus:
        menu.submenus_count, menu.dishes_count =\
            submenu_dish_count(db=db, menu_id=menu.id)
    return menus


@router.post("/", response_model=schemas.MenuOut,
             status_code=status.HTTP_201_CREATED)
def creating_menu(menu: schemas.MenuIn,
                  db: Session = Depends(get_db)):
    db_output = create_menu(db=db, menu=menu)
    db_output.submenus_count, db_output.dishes_count = submenu_dish_count(
        db=db, menu_id=db_output.id)
    return db_output


@router.get("/{menu_id}",
            response_model=schemas.MenuOut)
def reading_menu(menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = get_menu(db, menu_id=menu_id)
    db_menu.submenus_count, db_menu.dishes_count = submenu_dish_count(
        db=db, menu_id=db_menu.id)
    return db_menu


@router.delete("/{menu_id}",
               response_model=schemas.DeleteMSG,
               status_code=status.HTTP_200_OK)
def deleting_menu(menu_id: UUID,
                  db: Session = Depends(get_db)):
    return delete_menu(db=db, menu_id=menu_id)


@router.patch("/{menu_id}",
              response_model=schemas.MenuOut)
def updating_menu(menu: schemas.MenuIn,
                  menu_id: UUID, db: Session = Depends(get_db)):
    updated_menu = update_menu(db=db, menu=menu, menu_id=menu_id)
    updated_menu.submenus_count,\
        updated_menu.dishes_count = submenu_dish_count(
            db=db, menu_id=updated_menu.id)
    return updated_menu
