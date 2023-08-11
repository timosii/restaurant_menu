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

    async def save_list(self, subject: list, prefix: str) -> None:
        cache_data = jsonable_encoder(subject)
        async with await self.get_redis_conn() as conn:
            await conn.set(prefix, json.dumps(cache_data))
            await conn.expire(f'{prefix}', EXPIRE)

    async def load_list(self, prefix:
                        str) -> list[MenuOut] | list[SubmenuOut] | list[DishOut]:
        async with await self.get_redis_conn() as conn:
            cached_data = await conn.get(prefix)
            return json.loads(cached_data)

    async def check_list(self, prefix: str) -> int:
        async with await self.get_redis_conn() as conn:
            return await conn.exists(f'{prefix}')

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
