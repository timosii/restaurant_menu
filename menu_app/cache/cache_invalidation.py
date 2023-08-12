from uuid import UUID

from menu_app.cache.cache_base import CacheUtils


class CacheInvalidation(CacheUtils):
    async def del_list(self, prefix: str) -> None:
        async with await self.get_redis_conn() as conn:
            await conn.delete(prefix)

    async def del_all_lists(self, **kwargs) -> None:
        menu_id = kwargs.get('menu_id', None)
        submenu_id = kwargs.get('submenu_id', None)
        async with await self.get_redis_conn() as conn:
            await conn.delete('Menus', f'Submenus:{menu_id}', f'Dishes:{submenu_id}:{menu_id}')

    async def del_child(self, parent_id: UUID) -> None:
        async with await self.get_redis_conn() as conn:
            all_keys = await conn.keys('*')
            for key in all_keys:
                if str(parent_id) in str(key):
                    await conn.delete(key)

    async def delete(self, **kwargs) -> None:
        form_key = await self.key_generation(**kwargs)
        async with await self.get_redis_conn() as conn:
            await conn.delete(form_key)


class CacheMenuInvalidation(CacheInvalidation):
    async def create_invalidation(self):
        await self.del_list(prefix='Menus')

    async def update_invalidation(self):
        await self.del_list(prefix='Menus')

    async def delete_invalidation(self, menu_id: UUID):
        await self.del_all_lists(menu_id=menu_id)
        await self.delete(menu_id=menu_id)
        await self.del_child(parent_id=menu_id)


class CacheSubmenuInvalidation(CacheInvalidation):
    async def create_invalidation(self, menu_id: UUID):
        await self.del_all_lists(menu_id=menu_id)
        await self.delete(menu_id=menu_id)

    async def update_invalidation(self, menu_id: UUID):
        await self.del_list(prefix=f'Submenus:{menu_id}')

    async def delete_invalidation(self, menu_id: UUID, submenu_id: UUID):
        await self.del_all_lists(menu_id=menu_id, submenu_id=submenu_id)
        await self.delete(menu_id=menu_id)
        await self.delete(menu_id=menu_id, submenu_id=submenu_id)
        await self.del_child(parent_id=submenu_id)


class CacheDishInvalidation(CacheInvalidation):
    async def create_invalidation(self, menu_id: UUID, submenu_id: UUID):
        await self.del_all_lists(menu_id=menu_id, submenu_id=submenu_id)
        await self.delete(menu_id=menu_id)
        await self.delete(menu_id=menu_id, submenu_id=submenu_id)

    async def update_invalidation(self, menu_id: UUID, submenu_id: UUID):
        await self.del_list(prefix=f'Dishes:{submenu_id}:{menu_id}')

    async def delete_invalidation(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
        await self.del_all_lists(menu_id=menu_id, submenu_id=submenu_id)
        await self.delete(menu_id=menu_id)
        await self.delete(menu_id=menu_id, submenu_id=submenu_id)
        await self.delete(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
