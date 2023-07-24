from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas


def get_all_menus(db: Session):
    return db.query(models.Menu).all()


def get_menu(db: Session, menu_id: int):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()


def get_menu_by_title(db: Session, title: str):
    return db.query(models.Menu).filter(models.Menu.title == title).first()


def create_menu(db: Session, menu: schemas.Menu):
    db_menu = models.Menu(title=menu.title, description=menu.description)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def delete_menu(db: Session, menu_id: int):
    db.query(models.Menu).filter(models.Menu.id == menu_id).delete()
    db.commit()
    return 


def update_menu(db: Session, menu: schemas.Menu, menu_id: int):
    updated_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    updated_menu.title = menu.title
    updated_menu.description = menu.description
    db.add(updated_menu)
    db.commit()
    return updated_menu


def get_all_submenus(db: Session, menu_id: int):
    return db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).all()


def get_submenu(db: Session, menu_id: int, submenu_id: int):
    return db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id, \
    models.Submenu.submenu_id == submenu_id).first()


def create_submenu(db: Session, submenu: schemas.Submenu):
    db_submenu = models.Submenu(title=submenu.title, description=submenu.description, menu_id=submenu.menu_id)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def delete_submenu(db: Session, menu_id: int, submenu_id: int):
    db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id, \
    models.Submenu.submenu_id == submenu_id).delete()
    db.commit()
    return


def update_submenu(db: Session, submenu: schemas.Submenu, menu_id: int, submenu_id: int):
    updated_submenu = db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id, \
    models.Submenu.submenu_id == submenu_id).first()
    updated_submenu.title = submenu.title
    updated_submenu.description = submenu.description
    db.add(updated_submenu)
    db.commit()
    return updated_submenu


def get_all_dishes(db: Session, menu_id: int, submenu_id: int):
    return db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id, \
    models.Dish.menu_id == menu_id).all()


def get_dish(db: Session, menu_id: int, submenu_id: int, dish_id: int):
    pass


def create_dish(db: Session, dish: schemas.Dish):
    pass


def delete_dish(db: Session, menu_id: int, submenu_id: int, dish_id: int):
    pass


def update_dish(db: Session, dish: schemas.Dish, menu_id: int, submenu_id: int, dish_id: int):
    pass




