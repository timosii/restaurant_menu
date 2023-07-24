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


