from .cache import CacheSubmenu
from ..schemas import SubmenuIn
from uuid import UUID
from fastapi import Depends
from ..repositories.submenu_repository import SubmenuRepository


class SubmenuService:

    def __init__(self, database_repository: SubmenuRepository = Depends()):
        self.database_repository = database_repository
        self.cache = CacheSubmenu()

    def get_all(self, menu_id: UUID):
        return self.database_repository.get_submenus(menu_id=menu_id)

    def get_one(self, menu_id: UUID, submenu_id: UUID):
        if self.cache.check_cache(menu_id=menu_id, submenu_id=submenu_id):
            return self.cache.load_cache(
                menu_id=menu_id, submenu_id=submenu_id)
        result = self.database_repository.get_submenu(
            submenu_id=submenu_id)
        self.cache.save_cache(
            subject=result, menu_id=menu_id, submenu_id=result.id)
        return result

    def create(self, submenu: SubmenuIn, menu_id: UUID):
        result = self.database_repository.create_submenu(
            submenu=submenu, menu_id=menu_id)
        self.cache.save_cache(
            subject=result, menu_id=menu_id, submenu_id=result.id)
        return result

    def update(self, menu_id: UUID, submenu_id: UUID, submenu: SubmenuIn):
        result = self.database_repository.update_submenu(
            menu_id=menu_id, submenu_id=submenu_id, submenu=submenu)
        self.cache.save_cache(
            subject=result, menu_id=menu_id, submenu_id=result.id)
        return result

    def delete(self, menu_id: UUID, submenu_id: UUID):
        self.cache.delete_cache(menu_id=menu_id, submenu_id=submenu_id)
        return self.database_repository.delete_submenu(submenu_id=submenu_id)
