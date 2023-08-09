import json
from uuid import UUID

import redis
from fastapi.encoders import jsonable_encoder

from ..config import settings
from ..schemas import DishOut, MenuOut, SubmenuOut

host = settings.REDIS_HOST
port = settings.REDIS_PORT
db = settings.REDIS_DB
EXPIRE = 3000


class CacheBase:
    def __init__(self):
        self.redis_conn = redis.Redis(host=host, port=port, db=db)

    def key_generation(self, **kwargs) -> str:
        menu_id = kwargs.get('menu_id', None)
        submenu_id = kwargs.get('submenu_id', None)
        dish_id = kwargs.get('dish_id', None)
        form_key = f'{menu_id}:{submenu_id}:{dish_id}'
        return form_key

    def save_stage(self, subject: list, prefix: str) -> None:
        cache_data = jsonable_encoder(subject)
        self.redis_conn.set(prefix, json.dumps(cache_data))
        self.redis_conn.expire(f'{prefix}', EXPIRE)
        return

    def load_stage(self, prefix:
                   str) -> list[MenuOut] | list[SubmenuOut] | list[DishOut]:
        cached_data = self.redis_conn.get(prefix)
        return json.loads(cached_data)

    def check_stage(self, prefix: str) -> int:
        return self.redis_conn.exists(f'{prefix}')

    def del_stage(self, prefix: str) -> None:
        self.redis_conn.delete(prefix)

    def del_all_stages(self, **kwargs) -> None:
        menu_id = kwargs.get('menu_id', None)
        submenu_id = kwargs.get('submenu_id', None)
        self.redis_conn.delete('Menus',
                               f'Submenus:{menu_id}',
                               f'Dishes:{submenu_id}:{menu_id}')

    def save(self, subject: MenuOut | SubmenuOut | DishOut, **kwargs) -> None:
        cache_data = jsonable_encoder(subject)
        form_key = self.key_generation(**kwargs)
        self.redis_conn.set(form_key, json.dumps(cache_data))
        self.redis_conn.expire(form_key, EXPIRE)

    def load(self, subject, **kwargs) -> MenuOut | SubmenuOut | DishOut | None:
        form_key = self.key_generation(**kwargs)
        cached_data = self.redis_conn.get(form_key)
        if cached_data:
            return subject(**json.loads(cached_data))
        return None

    def check(self, **kwargs) -> int:
        form_key = self.key_generation(**kwargs)
        return self.redis_conn.exists(form_key)

    def delete(self, **kwargs) -> None:
        form_key = self.key_generation(**kwargs)
        self.redis_conn.delete(form_key)


class CacheMenu(CacheBase):

    def save_cache(self, subject: MenuOut, menu_id: UUID) -> None:
        self.save(subject=subject, menu_id=menu_id)

    def load_cache(self, menu_id: UUID) -> MenuOut | None:
        return self.load(subject=MenuOut, menu_id=menu_id)

    def check_cache(self, menu_id: UUID) -> int:
        return self.check(menu_id=menu_id)

    def delete_cache(self, menu_id: UUID) -> None:
        self.del_stage(prefix='Menus')
        self.delete(menu_id=menu_id)
        all_keys = self.redis_conn.keys('*')
        for key in all_keys:
            if str(menu_id) in str(key):
                self.redis_conn.delete(key)


class CacheSubmenu(CacheBase):

    def save_cache(self, subject: SubmenuOut,
                   menu_id: UUID, submenu_id: UUID) -> None:
        self.save(subject=subject, menu_id=menu_id, submenu_id=submenu_id)

    def load_cache(self, menu_id: UUID,
                   submenu_id: UUID) -> SubmenuOut | None:
        return self.load(subject=SubmenuOut,
                         menu_id=menu_id,
                         submenu_id=submenu_id)

    def check_cache(self, menu_id: UUID, submenu_id: UUID) -> int:
        return self.check(menu_id=menu_id, submenu_id=submenu_id)

    def delete_cache(self, menu_id: UUID, submenu_id: UUID) -> None:
        self.del_all_stages(menu_id=menu_id, submenu_id=submenu_id)
        self.delete(menu_id=menu_id)
        self.delete(menu_id=menu_id, submenu_id=submenu_id)
        all_keys = self.redis_conn.keys('*')
        for key in all_keys:
            if str(submenu_id) in str(key):
                self.redis_conn.delete(key)


class CacheDish(CacheBase):

    def save_cache(self, subject: DishOut,
                   menu_id: UUID,
                   submenu_id: UUID,
                   dish_id: UUID) -> None:
        self.save(subject=subject,
                  menu_id=menu_id,
                  submenu_id=submenu_id,
                  dish_id=dish_id)

    def load_cache(self, menu_id: UUID,
                   submenu_id: UUID,
                   dish_id: UUID) -> DishOut | None:
        return self.load(subject=DishOut,
                         menu_id=menu_id,
                         submenu_id=submenu_id,
                         dish_id=dish_id)

    def check_cache(self, menu_id: UUID,
                    submenu_id: UUID, dish_id: UUID) -> int:
        return self.check(menu_id=menu_id,
                          submenu_id=submenu_id,
                          dish_id=dish_id)

    def delete_cache(self,
                     menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> None:
        self.del_all_stages(menu_id=menu_id, submenu_id=submenu_id)
        self.delete(menu_id=menu_id)
        self.delete(menu_id=menu_id, submenu_id=submenu_id)
        self.delete(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
