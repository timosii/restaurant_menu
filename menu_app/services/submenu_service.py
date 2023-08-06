from uuid import UUID

from fastapi import Depends
from fastapi.responses import JSONResponse

from ..repositories.submenu_repository import SubmenuRepository
from ..schemas import SubmenuIn, SubmenuOut
from .cache import CacheSubmenu


class SubmenuService:

    def __init__(self,
                 database_repository: SubmenuRepository = Depends()) -> None:
        self.database_repository = database_repository
        self.cache = CacheSubmenu()

    def get_all(self, menu_id: UUID) -> list[SubmenuOut]:
        return self.database_repository.get_submenus(menu_id=menu_id)

    def get_one(self,
                menu_id: UUID,
                submenu_id: UUID) -> SubmenuOut | None:
        if self.cache.check_cache(menu_id=menu_id, submenu_id=submenu_id):
            return self.cache.load_cache(
                menu_id=menu_id, submenu_id=submenu_id)
        result = self.database_repository.get_submenu(
            submenu_id=submenu_id)
        self.cache.save_cache(
            subject=result, menu_id=menu_id, submenu_id=result.id)
        return result

    def create(self,
               submenu: SubmenuIn,
               menu_id: UUID) -> SubmenuOut:
        result = self.database_repository.create_submenu(
            submenu=submenu, menu_id=menu_id)
        self.cache.save_cache(
            subject=result, menu_id=menu_id, submenu_id=result.id)
        return result

    def update(self,
               menu_id: UUID,
               submenu_id: UUID,
               submenu: SubmenuIn) -> SubmenuOut:
        result = self.database_repository.update_submenu(
            menu_id=menu_id, submenu_id=submenu_id, submenu=submenu)
        self.cache.save_cache(
            subject=result, menu_id=menu_id, submenu_id=result.id)
        return result

    def delete(self, menu_id: UUID, submenu_id: UUID) -> JSONResponse:
        self.cache.delete_cache(menu_id=menu_id, submenu_id=submenu_id)
        return self.database_repository.delete_submenu(submenu_id=submenu_id)
