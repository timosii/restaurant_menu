import redis
import json
from ..schemas import MenuOut, SubmenuOut, DishOut
from typing import Optional
from uuid import UUID
from fastapi.encoders import jsonable_encoder


class CacheMenu:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_conn = redis.Redis(host=host, port=port, db=db)

    def save_cache(self, subject: MenuOut, menu_id: UUID) -> None:
        cache_data = jsonable_encoder(subject)
        self.redis_conn.set(f'menu:{menu_id}', json.dumps(cache_data))

    def load_cache(self, menu_id: UUID) -> Optional[MenuOut]:
        cached_data = self.redis_conn.get(f'menu:{menu_id}')
        if cached_data:
            return MenuOut(**json.loads(cached_data))
        return None

    def check_cache(self, menu_id: UUID) -> bool:
        return self.redis_conn.exists(f'menu:{menu_id}')

    def delete_cache(self, menu_id: UUID):
        self.redis_conn.delete(f'menu:{menu_id}')
        for key in self.redis_conn.hkeys(hash(menu_id)):
            self.redis_conn.hdel(hash(menu_id), key)


class CacheSubmenu:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_conn = redis.Redis(host=host, port=port, db=db)

    def save_cache(self, subject: SubmenuOut,
                   menu_id: UUID, submenu_id: UUID) -> None:
        cache_menu = CacheMenu()
        cache_menu.delete_cache(menu_id=menu_id)
        cache_data = jsonable_encoder(subject)
        self.redis_conn.hset(hash(menu_id), f'submenu:{submenu_id}',
                             json.dumps(cache_data))

    def load_cache(self, menu_id: UUID,
                   submenu_id: UUID) -> Optional[SubmenuOut]:
        cached_data = self.redis_conn.hget(hash(menu_id),
                                           f'submenu:{submenu_id}')
        if cached_data:
            return SubmenuOut(**json.loads(cached_data))
        return None

    def check_cache(self, menu_id: UUID, submenu_id: UUID) -> bool:
        return self.redis_conn.hexists(hash(menu_id), f'submenu:{submenu_id}')

    def delete_cache(self, menu_id: UUID, submenu_id: UUID) -> None:
        self.redis_conn.delete(hash(menu_id), f'submenu:{submenu_id}')
        for key in self.redis_conn.hkeys(hash(submenu_id)):
            self.redis_conn.hdel(hash(submenu_id), key)


class CacheDish:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_conn = redis.Redis(host=host, port=port, db=db)

    def save_cache(self, subject: DishOut,
                   menu_id: UUID,
                   submenu_id: UUID,
                   dish_id: UUID) -> None:
        cache_menu = CacheMenu()
        cache_menu.delete_cache(menu_id=menu_id)
        cache_data = jsonable_encoder(subject)
        self.redis_conn.hset(hash(submenu_id), f'dish:{dish_id}',
                             json.dumps(cache_data))

    def load_cache(self, submenu_id: UUID, dish_id: UUID) -> Optional[DishOut]:
        cached_data = self.redis_conn.hget(hash(submenu_id),
                                           f'dish:{dish_id}')
        if cached_data:
            return DishOut(**json.loads(cached_data))
        return None

    def check_cache(self, submenu_id: UUID, dish_id: UUID) -> bool:
        return self.redis_conn.hexists(hash(submenu_id), f'dish:{dish_id}')

    def delete_cache(self, submenu_id: UUID, dish_id: UUID) -> None:
        self.redis_conn.hdel(hash(submenu_id), f'dish:{dish_id}')
