from uuid import UUID, uuid4

from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Dish, Submenu
from ..schemas import SubmenuIn, SubmenuOut
from .errors import already_exist, not_found, success_delete

SAMPLE = 'submenu'


class SubmenuRepository:
    def __init__(self, session: Session = Depends(get_db)) -> None:
        self.session = session
        self.model = Submenu

    def get_submenus(self, menu_id: UUID) -> list[SubmenuOut]:
        submenus = self.session.query(Submenu).filter(
            Submenu.parent_menu_id == menu_id).all()
        for submenu in submenus:
            submenu.dishes_count = self.dish_for_submenu_count(
                submenu_id=submenu.id)
        return submenus

    def create_submenu(self,
                       submenu: SubmenuIn,
                       menu_id: UUID) -> SubmenuOut:
        self.check_submenu_by_title(submenu_title=submenu.title)
        db_submenu = Submenu(id=uuid4(),
                             title=submenu.title,
                             description=submenu.description,
                             parent_menu_id=menu_id)
        self.session.add(db_submenu)
        self.session.commit()
        self.session.refresh(db_submenu)
        db_submenu.dishes_count = self.dish_for_submenu_count(
            submenu_id=db_submenu.id)
        return db_submenu

    def get_submenu(self, submenu_id: UUID) -> SubmenuOut:
        current_submenu = self.session.query(Submenu).filter(
            Submenu.id == submenu_id).first()
        if current_submenu is None:
            not_found(SAMPLE)
        current_submenu.dishes_count = self.dish_for_submenu_count(
            submenu_id=current_submenu.id)
        return current_submenu

    def check_submenu_by_title(self, submenu_title: str) -> None:
        db_menu = self.session.query(Submenu).filter(
            Submenu.title == submenu_title).first()
        if db_menu:
            already_exist(SAMPLE)
        return

    def delete_submenu(self, submenu_id: UUID) -> JSONResponse:
        submenu_for_delete = self.session.query(Submenu).filter(
            Submenu.id == submenu_id).first()
        if submenu_for_delete is None:
            not_found(SAMPLE)
        self.session.delete(submenu_for_delete)
        self.session.commit()
        return success_delete(SAMPLE)

    def update_submenu(self, menu_id: UUID,
                       submenu_id: UUID,
                       submenu: SubmenuIn) -> SubmenuOut:
        db_submenu = self.get_submenu(submenu_id=submenu_id)
        if db_submenu is None:
            not_found(SAMPLE)
        upd_submenu = self.session.query(Submenu).filter(
            Submenu.id == submenu_id,
            Submenu.parent_menu_id == menu_id).first()
        upd_submenu.title = submenu.title
        upd_submenu.description = submenu.description
        self.session.add(upd_submenu)
        self.session.commit()
        upd_submenu.dishes_count = self.dish_for_submenu_count(
            submenu_id=upd_submenu.id)
        return upd_submenu

    def dish_for_submenu_count(self, submenu_id: UUID) -> int:
        dishes = self.session.query(func.count()).select_from(
            Submenu).join(Dish, Submenu.id == Dish.parent_submenu_id).filter(
            Submenu.id == submenu_id).scalar()
        return dishes
