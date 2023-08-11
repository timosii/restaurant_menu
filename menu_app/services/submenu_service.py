from uuid import UUID

from fastapi import Depends
from fastapi.responses import JSONResponse

from menu_app.cache.cache_subjects import CacheSubmenu
from menu_app.repositories.submenu_repository import SubmenuRepository
from menu_app.schemas import SubmenuIn, SubmenuOut


class SubmenuService:

    def __init__(self,
                 database_repository: SubmenuRepository = Depends()) -> None:
        self.database_repository = database_repository
        self.cache = CacheSubmenu()

    async def get_all(self, menu_id: UUID) -> list[SubmenuOut]:
        if await self.cache.check_list(prefix=f'Submenus:{menu_id}'):
            return await self.cache.load_list(prefix=f'Submenus:{menu_id}')
        result = await self.database_repository.get_submenus(menu_id=menu_id)
        await self.cache.save_list(subject=result, prefix=f'Submenus:{menu_id}')
        return result

    async def get_one(self,
                      menu_id: UUID,
                      submenu_id: UUID) -> SubmenuOut | None:
        if await self.cache.check_cache(menu_id=menu_id, submenu_id=submenu_id):
            return await self.cache.load_cache(
                menu_id=menu_id, submenu_id=submenu_id)
        result = await self.database_repository.get_submenu(
            submenu_id=submenu_id)
        await self.cache.save_cache(
            subject=result, menu_id=menu_id, submenu_id=submenu_id)
        return result

    async def create(self,
                     submenu: SubmenuIn,
                     menu_id: UUID) -> SubmenuOut:
        result = await self.database_repository.create_submenu(
            submenu=submenu, menu_id=menu_id)
        await self.cache.del_all_lists(menu_id=menu_id)
        await self.cache.delete(menu_id=menu_id)
        await self.cache.save_cache(
            subject=result, menu_id=menu_id, submenu_id=result.id)
        return result

    async def update(self,
                     menu_id: UUID,
                     submenu_id: UUID,
                     submenu: SubmenuIn) -> SubmenuOut:
        result = await self.database_repository.update_submenu(
            menu_id=menu_id, submenu_id=submenu_id, submenu=submenu)
        await self.cache.del_list(prefix=f'Submenus:{menu_id}')
        await self.cache.save_cache(
            subject=result, menu_id=menu_id, submenu_id=result.id)
        return result

    async def delete(self, menu_id: UUID, submenu_id: UUID) -> JSONResponse:
        await self.cache.delete_cache(menu_id=menu_id, submenu_id=submenu_id)
        return await self.database_repository.delete_submenu(submenu_id=submenu_id)
