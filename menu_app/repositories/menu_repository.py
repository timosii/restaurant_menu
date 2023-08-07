from uuid import UUID, uuid4

from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Dish, Menu, Submenu
from ..schemas import MenuIn, MenuOut
from .errors import already_exist, not_found, success_delete

SAMPLE = 'menu'


class MenuRepository:
    def __init__(self, session: Session = Depends(get_db)) -> None:
        self.session = session
        self.model = Menu

    def get_menus(self) -> list[MenuOut]:
        menus = self.session.query(Menu).all()
        for menu in menus:
            menu.submenus_count = self.submenu_count(menu_id=menu.id)
            menu.dishes_count = self.dish_count(menu_id=menu.id)
        return menus

    def create_menu(self, menu: MenuIn) -> MenuOut:
        self.check_menu_by_title(menu_title=menu.title)
        db_menu = Menu(id=uuid4(),
                       title=menu.title,
                       description=menu.description)
        self.session.add(db_menu)
        self.session.commit()
        self.session.refresh(db_menu)
        db_menu.submenus_count = self.submenu_count(menu_id=db_menu.id)
        db_menu.dishes_count = self.dish_count(menu_id=db_menu.id)
        return db_menu

    def get_menu(self, menu_id: UUID) -> MenuOut:
        db_menu = self.session.query(Menu).filter(
            Menu.id == menu_id).first()
        if db_menu is None:
            not_found(SAMPLE)
        db_menu.submenus_count = self.submenu_count(menu_id=db_menu.id)
        db_menu.dishes_count = self.dish_count(menu_id=db_menu.id)
        return db_menu

    def check_menu_by_title(self, menu_title: str) -> None:
        db_menu = self.session.query(Menu).filter(
            Menu.title == menu_title).first()
        if db_menu:
            already_exist(SAMPLE)
        return

    def delete_menu(self, menu_id: UUID) -> JSONResponse:
        menu_for_delete = self.session.query(Menu).filter(
            Menu.id == menu_id).first()
        if menu_for_delete is None:
            not_found(SAMPLE)
        self.session.delete(menu_for_delete)
        self.session.commit()
        return success_delete(SAMPLE)

    def update_menu(self,
                    menu: MenuIn,
                    menu_id: UUID) -> MenuOut:
        db_menu = self.get_menu(menu_id=menu_id)
        if db_menu is None:
            not_found(SAMPLE)
        upd_menu = self.session.query(Menu).filter(
            Menu.id == menu_id).first()
        upd_menu.title = menu.title
        upd_menu.description = menu.description
        self.session.add(upd_menu)
        self.session.commit()
        upd_menu.submenus_count = self.submenu_count(menu_id=upd_menu.id)
        upd_menu.dishes_count = self.dish_count(menu_id=upd_menu.id)
        return upd_menu

    def submenu_count(self, menu_id: UUID) -> int:
        submenus = self.session.query(func.count()).select_from(Menu).join(
            Submenu, Menu.id == Submenu.parent_menu_id).filter(
            Menu.id == menu_id).scalar()
        return submenus

    def dish_count(self, menu_id: UUID) -> int:
        dishes = self.session.query(func.count()).select_from(Menu).join(
            Submenu, Menu.id == Submenu.parent_menu_id).outerjoin(
            Dish, Submenu.id == Dish.parent_submenu_id).filter(
            Menu.id == menu_id).scalar()
        return dishes
