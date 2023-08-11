from uuid import UUID

from fastapi import Depends
from fastapi.responses import JSONResponse

from menu_app.cache.cache_subjects import CacheMenu
from menu_app.repositories.menu_repository import MenuRepository
from menu_app.schemas import MenuIn, MenuOut


class MenuService:
    def __init__(self,
                 database_repository: MenuRepository = Depends()) -> None:
        self.database_repository = database_repository
        self.cache = CacheMenu()

    async def get_all(self) -> list[MenuOut]:
        if await self.cache.check_list(prefix='Menus'):
            return await self.cache.load_list(prefix='Menus')
        result = await self.database_repository.get_menus()
        await self.cache.save_list(subject=result, prefix='Menus')
        return result

    async def get_one(self, menu_id: UUID) -> MenuOut | None:
        if await self.cache.check_cache(menu_id=menu_id):
            return await self.cache.load_cache(menu_id=menu_id)
        result = await self.database_repository.get_menu(menu_id=menu_id)
        await self.cache.save_cache(subject=result, menu_id=menu_id)
        return result

    async def create(self, menu: MenuIn) -> MenuOut:
        result = await self.database_repository.create_menu(menu=menu)
        await self.cache.del_list(prefix='Menus')
        await self.cache.save_cache(subject=result, menu_id=result.id)
        return result

    async def update(self, menu: MenuIn, menu_id: UUID) -> MenuOut:
        result = await self.database_repository.update_menu(
            menu=menu, menu_id=menu_id)
        await self.cache.del_list(prefix='Menus')
        await self.cache.save_cache(subject=result, menu_id=result.id)
        return result

    async def delete(self, menu_id: UUID) -> JSONResponse:
        await self.cache.delete_cache(menu_id=menu_id)
        return await self.database_repository.delete_menu(menu_id=menu_id)
