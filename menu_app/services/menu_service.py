import json
import redis
from typing import Optional
from ..schemas import MenuIn, MenuOut
from uuid import UUID
from fastapi import Depends
from ..repositories.menu_repository import MenuRepository
from fastapi.encoders import jsonable_encoder


class CacheMenu:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_conn = redis.Redis(host=host, port=port, db=db)

    def save_cache(self, subject: MenuOut, menu_id: UUID) -> None:
        self.redis_conn.set(f'menu:{menu_id}', json.dumps(
            jsonable_encoder(subject)))

    def load_cache(self, menu_id: UUID) -> Optional[MenuOut]:
        cached_data = self.redis_conn.get(f'menu:{menu_id}')
        if cached_data:
            return MenuOut(**json.loads(cached_data))
        return None

    def check_cache(self, menu_id: UUID) -> bool:
        return self.redis_conn.exists(f'menu:{menu_id}')

    def delete_cache(self, menu_id: UUID) -> int:
        return self.redis_conn.delete(f'menu:{menu_id}')


class MenuService:
    def __init__(self, database_repository: MenuRepository = Depends()):
        self.database_repository = database_repository
        self.cache = CacheMenu()

    def get_all(self):
        return self.database_repository.get_menus()

    def get_one(self, menu_id: UUID):
        if self.cache.check_cache(menu_id=menu_id):
            return self.cache.load_cache(menu_id=menu_id)
        result = self.database_repository.get_menu(menu_id=menu_id)
        self.cache.save_cache(subject=result, menu_id=result.id)
        return result

    def create(self, menu: MenuIn):
        result = self.database_repository.create_menu(menu=menu)
        self.cache.save_cache(subject=result, menu_id=result.id)
        return result

    def update(self, menu: MenuIn, menu_id: UUID):
        result = self.database_repository.update_menu(
            menu=menu, menu_id=menu_id)
        self.cache.save_cache(subject=result, menu_id=result.id)
        return result

    def delete(self, menu_id: UUID):
        self.cache.delete_cache(menu_id=menu_id)
        return self.database_repository.delete_menu(menu_id=menu_id)
