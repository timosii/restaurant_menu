from ..schemas import MenuIn
from uuid import UUID
from fastapi import Depends
from ..repositories.menu_repository import MenuRepository


class MenuService:

    def __init__(self, database_repository: MenuRepository = Depends()):
        self.database_repository = database_repository

    def get_all(self):
        return self.database_repository.get_menus()

    def get_one(self, menu_id: UUID):
        return self.database_repository.get_menu(menu_id=menu_id)

    def create(self, menu: MenuIn):
        return self.database_repository.create_menu(menu=menu)

    def update(self, menu: MenuIn, menu_id: UUID):
        return self.database_repository.update_menu(menu=menu, menu_id=menu_id)

    def delete(self, menu_id: UUID):
        return self.database_repository.delete_menu(menu_id=menu_id)
