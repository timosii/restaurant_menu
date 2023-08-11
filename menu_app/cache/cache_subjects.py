from uuid import UUID

from menu_app.cache.cache_base import CacheBase
from menu_app.schemas import DishOut, MenuOut, SubmenuOut


class CacheMenu(CacheBase):

    async def save_cache(self, subject: MenuOut, menu_id: UUID) -> None:
        await self.save(subject=subject, menu_id=menu_id)

    async def load_cache(self, menu_id: UUID) -> MenuOut | None:
        return await self.load(subject=MenuOut, menu_id=menu_id)

    async def check_cache(self, menu_id: UUID) -> int:
        return await self.check(menu_id=menu_id)

    async def delete_cache(self, menu_id: UUID) -> None:
        await self.del_list(prefix='Menus')
        await self.del_list(prefix=f'Submenus:{menu_id}')
        await self.delete(menu_id=menu_id)
        await self.del_child(parent_id=menu_id)


class CacheSubmenu(CacheBase):

    async def save_cache(self, subject: SubmenuOut,
                         menu_id: UUID, submenu_id: UUID) -> None:
        await self.save(subject=subject, menu_id=menu_id, submenu_id=submenu_id)

    async def load_cache(self, menu_id: UUID,
                         submenu_id: UUID) -> SubmenuOut | None:
        return await self.load(subject=SubmenuOut,
                               menu_id=menu_id,
                               submenu_id=submenu_id)

    async def check_cache(self, menu_id: UUID, submenu_id: UUID) -> int:
        return await self.check(menu_id=menu_id, submenu_id=submenu_id)

    async def delete_cache(self, menu_id: UUID, submenu_id: UUID) -> None:
        await self.del_all_lists(menu_id=menu_id, submenu_id=submenu_id)
        await self.delete(menu_id=menu_id)
        await self.delete(menu_id=menu_id, submenu_id=submenu_id)
        await self.del_child(parent_id=submenu_id)


class CacheDish(CacheBase):

    async def save_cache(self, subject: DishOut,
                         menu_id: UUID,
                         submenu_id: UUID,
                         dish_id: UUID) -> None:
        await self.save(subject=subject,
                        menu_id=menu_id,
                        submenu_id=submenu_id,
                        dish_id=dish_id)

    async def load_cache(self, menu_id: UUID,
                         submenu_id: UUID,
                         dish_id: UUID) -> DishOut | None:
        return await self.load(subject=DishOut,
                               menu_id=menu_id,
                               submenu_id=submenu_id,
                               dish_id=dish_id)

    async def check_cache(self, menu_id: UUID,
                          submenu_id: UUID, dish_id: UUID) -> int:
        return await self.check(menu_id=menu_id,
                                submenu_id=submenu_id,
                                dish_id=dish_id)

    async def delete_cache(self,
                           menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> None:
        await self.del_all_lists(menu_id=menu_id, submenu_id=submenu_id)
        await self.delete(menu_id=menu_id)
        await self.delete(menu_id=menu_id, submenu_id=submenu_id)
        await self.delete(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
