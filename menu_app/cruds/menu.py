from ..schemas import MenuIn
from ..models import Menu
from .errors import not_found, message_deleted
from uuid import UUID, uuid4
from sqlalchemy.orm import Session


SAMPLE = 'menu'


def get_menus(db: Session):
    return db.query(Menu).all()


def get_menu(db: Session, menu_id: UUID):
    db_menu = db.query(Menu).filter(
        Menu.id == menu_id).first()
    if db_menu is None:
        not_found(SAMPLE)
    return db_menu


def create_menu(db: Session, menu: MenuIn):
    db_menu = Menu(id=uuid4(),
                   title=menu.title,
                   description=menu.description)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def delete_menu(db: Session, menu_id: UUID):
    menu_for_delete = db.query(Menu).filter(
        Menu.id == menu_id).first()
    if menu_for_delete is None:
        not_found(SAMPLE)
    db.delete(menu_for_delete)
    db.commit()
    return message_deleted(SAMPLE)


def update_menu(db: Session,
                menu: MenuIn,
                menu_id: UUID):
    db_menu = get_menu(db, menu_id=menu_id)
    if db_menu is None:
        not_found(SAMPLE)
    updated_menu = db.query(Menu).filter(
        Menu.id == menu_id).first()
    updated_menu.title = menu.title
    updated_menu.description = menu.description
    db.add(updated_menu)
    db.commit()
    return updated_menu
