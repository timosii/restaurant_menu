from ..models import Menu, Submenu, Dish
from sqlalchemy import func
from uuid import UUID
from sqlalchemy.orm import Session


def submenu_count(db: Session, menu_id: UUID):
    submenus = db.query(func.count()).select_from(Menu).join(
        Submenu, Menu.id == Submenu.parent_menu_id).filter(
        Menu.id == menu_id).scalar()
    return submenus


def dish_count(db: Session, menu_id: UUID):
    dishes = db.query(func.count()).select_from(Menu).join(
        Submenu, Menu.id == Submenu.parent_menu_id).outerjoin(
        Dish, Submenu.id == Dish.parent_submenu_id).filter(
        Menu.id == menu_id).scalar()
    return dishes


def dish_for_submenu_count(db: Session, submenu_id: UUID):
    dishes = db.query(func.count()).select_from(
        Submenu).join(Dish, Submenu.id == Dish.parent_submenu_id).filter(
        Submenu.id == submenu_id).scalar()
    return dishes
