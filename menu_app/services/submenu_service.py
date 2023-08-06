from ..schemas import SubmenuIn
from uuid import UUID
from fastapi import Depends
from ..repositories.submenu_repository import SubmenuRepository


class SubmenuService:

    def __init__(self, database_repository: SubmenuRepository = Depends()):
        self.database_repository = database_repository

    def get_all(self, menu_id: UUID):
        return self.database_repository.get_submenus(menu_id)

    def get_one(self, submenu_id: UUID):
        return self.database_repository.get_submenu(submenu_id=submenu_id)

    def create(self, submenu: SubmenuIn, menu_id: UUID):
        return self.database_repository.create_submenu(
            submenu=submenu, menu_id=menu_id)

    def update(self, menu_id: UUID, submenu_id: UUID, submenu: SubmenuIn):
        return self.database_repository.update_submenu(
            menu_id=menu_id, submenu_id=submenu_id, submenu=submenu)

    def delete(self, submenu_id: UUID):
        return self.database_repository.delete_submenu(submenu_id=submenu_id)
