from .models import Menu, Submenu, Dish
from uuid import UUID
from fastapi import Depends
from sqlalchemy import func
from repositories.submenu_repository import SubmenuRepository
from repositories.menu_repository import MenuRepository


class CountService:
    def submenu_count(self, menu_id: UUID):
        submenus = self.session.query(func.count()).select_from(Menu).join(
            Submenu, Menu.id == Submenu.parent_menu_id).filter(
            Menu.id == menu_id).scalar()
        return submenus

    def dish_count(self, menu_id: UUID):
        dishes = self.session.query(func.count()).select_from(Menu).join(
            Submenu, Menu.id == Submenu.parent_menu_id).outerjoin(
            Dish, Submenu.id == Dish.parent_submenu_id).filter(
            Menu.id == menu_id).scalar()
        return dishes

    def dish_for_submenu_count(self, submenu_id: UUID):
        dishes = self.session.query(func.count()).select_from(
            Submenu).join(Dish, Submenu.id == Dish.parent_submenu_id).filter(
            Submenu.id == submenu_id).scalar()
        return dishes


class MenuService:

    def __init__(self, database_repository: MenuRepository = Depends()):
        self.database_repository = database_repository
        self.count = CountService()

    def get_submenu_count(self):
        return self.count.submenu_count()

    def get_dish_count(self):
        return self.count.dish_count()


class SubmenuService:

    def __init__(self, database_repository: SubmenuRepository = Depends()):
        self.database_repository = database_repository
        self.count = CountService()

    def get_dish_count(self):
        return self.count.dish_for_submenu_count()
