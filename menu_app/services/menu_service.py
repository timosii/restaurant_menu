from uuid import UUID

from fastapi import Depends
from fastapi.responses import JSONResponse

from ..repositories.menu_repository import MenuRepository
from ..schemas import MenuIn, MenuOut
from .cache import CacheMenu


class MenuService:
    def __init__(self,
                 database_repository: MenuRepository = Depends()) -> None:
        self.database_repository = database_repository
        self.cache = CacheMenu()

    def get_all(self) -> list[MenuOut]:
        return self.database_repository.get_menus()

    def get_one(self, menu_id: UUID) -> MenuOut | None:
        if self.cache.check_cache(menu_id=menu_id):
            return self.cache.load_cache(menu_id=menu_id)
        result = self.database_repository.get_menu(menu_id=menu_id)
        self.cache.save_cache(subject=result, menu_id=result.id)
        return result

    def create(self, menu: MenuIn) -> MenuOut:
        result = self.database_repository.create_menu(menu=menu)
        self.cache.save_cache(subject=result, menu_id=result.id)
        return result

    def update(self, menu: MenuIn, menu_id: UUID) -> MenuOut:
        result = self.database_repository.update_menu(
            menu=menu, menu_id=menu_id)
        self.cache.save_cache(subject=result, menu_id=result.id)
        return result

    def delete(self, menu_id: UUID) -> JSONResponse:
        self.cache.delete_cache(menu_id=menu_id)
        return self.database_repository.delete_menu(menu_id=menu_id)
