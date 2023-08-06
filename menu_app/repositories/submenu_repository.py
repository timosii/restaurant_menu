from ..schemas import SubmenuIn
from ..models import Submenu, Dish
from .errors import not_found, success_delete
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from fastapi import Depends
from ..database import get_db
from sqlalchemy import func


SAMPLE = 'submenu'


class SubmenuRepository:
    def __init__(self, session: Session = Depends(get_db)) -> None:
        self.session = session
        self.model = Submenu

    def get_submenus(self, menu_id: UUID):
        submenus = self.session.query(Submenu).filter(
            Submenu.parent_menu_id == menu_id).all()
        for submenu in submenus:
            submenu.dishes_count = self.dish_for_submenu_count(
                submenu_id=submenu.id)
        return submenus

    def get_submenu(self, submenu_id: UUID):
        current_submenu = self.session.query(Submenu).filter(
            Submenu.id == submenu_id).first()
        if current_submenu is None:
            not_found(SAMPLE)
        current_submenu.dishes_count = self.dish_for_submenu_count(
                submenu_id=current_submenu.id)
        return current_submenu

    def create_submenu(self,
                       submenu: SubmenuIn,
                       menu_id: UUID):
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

    def delete_submenu(self, menu_id: UUID,
                       submenu_id: UUID):
        submenu_for_delete = self.session.query(Submenu).filter(
            Submenu.id == submenu_id).first()
        if submenu_for_delete is None:
            not_found(SAMPLE)
        self.session.delete(submenu_for_delete)
        self.session.commit()
        return success_delete(SAMPLE)

    def update_submenu(self, menu_id: UUID,
                       submenu_id: UUID,
                       submenu: SubmenuIn):
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

    def dish_for_submenu_count(self, submenu_id: UUID):
        dishes = self.session.query(func.count()).select_from(
            Submenu).join(Dish, Submenu.id == Dish.parent_submenu_id).filter(
            Submenu.id == submenu_id).scalar()
        return dishes
