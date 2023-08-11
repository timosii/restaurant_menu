import json
from uuid import UUID

import aioredis
from fastapi.encoders import jsonable_encoder

from menu_app.config import settings
from menu_app.schemas import DishOut, MenuOut, SubmenuOut

host = settings.REDIS_HOST
port = settings.REDIS_PORT
db = settings.REDIS_DB
redis_url = f'redis://{host}:{port}'
EXPIRE = 3000


class CacheBase:

    async def get_redis_conn(self):
        return await aioredis.from_url(redis_url, db=db)

    async def key_generation(self, **kwargs) -> str:
        menu_id = kwargs.get('menu_id', None)
        submenu_id = kwargs.get('submenu_id', None)
        dish_id = kwargs.get('dish_id', None)
        form_key = f'{menu_id}:{submenu_id}:{dish_id}'
        return form_key

    async def save_stage(self, subject: list, prefix: str) -> None:
        cache_data = jsonable_encoder(subject)
        async with await self.get_redis_conn() as conn:
            await conn.set(prefix, json.dumps(cache_data))
            await conn.expire(f'{prefix}', EXPIRE)

    async def load_stage(self, prefix:
                         str) -> list[MenuOut] | list[SubmenuOut] | list[DishOut]:
        async with await self.get_redis_conn() as conn:
            cached_data = await conn.get(prefix)
            return json.loads(cached_data)

    async def check_stage(self, prefix: str) -> int:
        async with await self.get_redis_conn() as conn:
            return await conn.exists(f'{prefix}')

    async def del_stage(self, prefix: str) -> None:
        async with await self.get_redis_conn() as conn:
            await conn.delete(prefix)

    async def del_all_stages(self, **kwargs) -> None:
        menu_id = kwargs.get('menu_id', None)
        submenu_id = kwargs.get('submenu_id', None)
        async with await self.get_redis_conn() as conn:
            await conn.delete('Menus', f'Submenus:{menu_id}', f'Dishes:{submenu_id}:{menu_id}')

    async def save(self, subject: MenuOut | SubmenuOut | DishOut, **kwargs) -> None:
        cache_data = jsonable_encoder(subject)
        form_key = await self.key_generation(**kwargs)
        async with await self.get_redis_conn() as conn:
            await conn.set(form_key, json.dumps(cache_data))
            await conn.expire(form_key, EXPIRE)

    async def load(self, subject, **kwargs) -> MenuOut | SubmenuOut | DishOut | None:
        form_key = await self.key_generation(**kwargs)
        async with await self.get_redis_conn() as conn:
            cached_data = await conn.get(form_key)
            if cached_data:
                return subject(**json.loads(cached_data))
            return None

    async def check(self, **kwargs) -> int:
        form_key = await self.key_generation(**kwargs)
        async with await self.get_redis_conn() as conn:
            return await conn.exists(form_key)

    async def delete(self, **kwargs) -> None:
        form_key = await self.key_generation(**kwargs)
        async with await self.get_redis_conn() as conn:
            await conn.delete(form_key)


class CacheMenu(CacheBase):

    async def save_cache(self, subject: MenuOut, menu_id: UUID) -> None:
        await self.save(subject=subject, menu_id=menu_id)

    async def load_cache(self, menu_id: UUID) -> MenuOut | None:
        return await self.load(subject=MenuOut, menu_id=menu_id)

    async def check_cache(self, menu_id: UUID) -> int:
        return await self.check(menu_id=menu_id)

    async def delete_cache(self, menu_id: UUID) -> None:
        await self.del_stage(prefix='Menus')
        await self.delete(menu_id=menu_id)
        async with await self.get_redis_conn() as conn:
            all_keys = await conn.keys('*')
            for key in all_keys:
                if str(menu_id) in str(key):
                    await conn.delete(key)


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
        await self.del_all_stages(menu_id=menu_id, submenu_id=submenu_id)
        await self.delete(menu_id=menu_id)
        await self.delete(menu_id=menu_id, submenu_id=submenu_id)
        async with await self.get_redis_conn() as conn:
            all_keys = await conn.keys('*')
            for key in all_keys:
                if str(submenu_id) in str(key):
                    await conn.delete(key)


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
        await self.del_all_stages(menu_id=menu_id, submenu_id=submenu_id)
        await self.delete(menu_id=menu_id)
        await self.delete(menu_id=menu_id, submenu_id=submenu_id)
        await self.delete(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
