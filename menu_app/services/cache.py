import json
from uuid import UUID

import redis
from fastapi.encoders import jsonable_encoder

from ..config import settings
from ..schemas import DishOut, MenuOut, SubmenuOut

host = settings.REDIS_HOST
port = settings.REDIS_PORT
db = settings.REDIS_DB


class CacheBase:
    def __init__(self):
        self.redis_conn = redis.Redis(host=host, port=port, db=db)

    def delete_parent_menu(self, menu_id: UUID) -> None:
        self.redis_conn.delete(f'menu:{menu_id}')
        for key in self.redis_conn.hkeys(str(menu_id)):
            self.redis_conn.hdel(str(menu_id), key)

    def delete_parent_submenu(self, menu_id: UUID, submenu_id: UUID) -> None:
        self.redis_conn.delete(str(menu_id), f'submenu:{submenu_id}')
        for key in self.redis_conn.hkeys(str(submenu_id)):
            self.redis_conn.hdel(str(submenu_id), key)


class CacheMenu(CacheBase):

    def save_cache(self, subject: MenuOut, menu_id: UUID) -> None:
        cache_data = jsonable_encoder(subject)
        self.redis_conn.set(f'menu:{menu_id}', json.dumps(cache_data))

    def load_cache(self, menu_id: UUID) -> MenuOut | None:
        cached_data = self.redis_conn.get(f'menu:{menu_id}')
        if cached_data:
            return MenuOut(**json.loads(cached_data))
        return None

    def check_cache(self, menu_id: UUID) -> int:
        return self.redis_conn.exists(f'menu:{menu_id}')

    def delete_cache(self, menu_id: UUID) -> None:
        self.delete_parent_menu(menu_id=menu_id)


class CacheSubmenu(CacheBase):

    def save_cache(self, subject: SubmenuOut,
                   menu_id: UUID, submenu_id: UUID) -> None:
        self.delete_parent_menu(menu_id=menu_id)
        cache_data = jsonable_encoder(subject)
        self.redis_conn.hset(str(menu_id), f'submenu:{submenu_id}',
                             json.dumps(cache_data))

    def load_cache(self, menu_id: UUID,
                   submenu_id: UUID) -> SubmenuOut | None:
        cached_data = self.redis_conn.hget(str(menu_id),
                                           f'submenu:{submenu_id}')
        if cached_data:
            return SubmenuOut(**json.loads(cached_data))
        return None

    def check_cache(self, menu_id: UUID, submenu_id: UUID) -> int:
        return self.redis_conn.hexists(str(menu_id), f'submenu:{submenu_id}')

    def delete_cache(self, menu_id: UUID, submenu_id: UUID) -> None:
        self.delete_parent_menu(menu_id=menu_id)
        self.delete_parent_submenu(menu_id=menu_id, submenu_id=submenu_id)


class CacheDish(CacheBase):

    def save_cache(self, subject: DishOut,
                   menu_id: UUID,
                   submenu_id: UUID,
                   dish_id: UUID) -> None:
        self.delete_parent_submenu(menu_id=menu_id, submenu_id=submenu_id)
        self.delete_parent_menu(menu_id=menu_id)
        cache_data = jsonable_encoder(subject)
        self.redis_conn.hset(str(submenu_id), f'dish:{dish_id}',
                             json.dumps(cache_data))

    def load_cache(self, submenu_id: UUID, dish_id: UUID) -> DishOut | None:
        cached_data = self.redis_conn.hget(str(submenu_id),
                                           f'dish:{dish_id}')
        if cached_data:
            return DishOut(**json.loads(cached_data))
        return None

    def check_cache(self, submenu_id: UUID, dish_id: UUID) -> bool:
        return self.redis_conn.hexists(str(submenu_id), f'dish:{dish_id}')

    def delete_cache(self,
                     menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> None:
        self.delete_parent_submenu(menu_id=menu_id, submenu_id=submenu_id)
        self.delete_parent_menu(menu_id=menu_id)
        self.redis_conn.hdel(str(submenu_id), f'dish:{dish_id}')
