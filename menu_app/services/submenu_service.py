import json
import redis
from fastapi.encoders import jsonable_encoder
from ..schemas import SubmenuIn, SubmenuOut
from uuid import UUID
from fastapi import Depends
from ..repositories.submenu_repository import SubmenuRepository
from typing import Optional


class CacheSubmenu:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_conn = redis.Redis(host=host, port=port, db=db)

    def save_cache(self, subject: SubmenuOut, submenu_id: UUID) -> None:
        self.redis_conn.set(f'submenu:{submenu_id}', json.dumps(
            jsonable_encoder(subject)))

    def load_cache(self, submenu_id: UUID) -> Optional[SubmenuOut]:
        cached_data = self.redis_conn.get(f'submenu:{submenu_id}')
        if cached_data:
            return SubmenuOut(**json.loads(cached_data))
        return None

    def check_cache(self, submenu_id: UUID) -> bool:
        return self.redis_conn.exists(f'submenu:{submenu_id}')

    def delete_cache(self, submenu_id: UUID) -> int:
        return self.redis_conn.delete(f'submenu:{submenu_id}')


class SubmenuService:

    def __init__(self, database_repository: SubmenuRepository = Depends()):
        self.database_repository = database_repository
        self.cache = CacheSubmenu()

    def get_all(self, menu_id: UUID):
        return self.database_repository.get_submenus(menu_id)

    def get_one(self, submenu_id: UUID):
        if self.cache.check_cache(submenu_id=submenu_id):
            return self.cache.load_cache(submenu_id=submenu_id)
        result = self.database_repository.get_submenu(
            submenu_id=submenu_id)
        self.cache.save_cache(subject=result, submenu_id=result.id)
        return result

    def create(self, submenu: SubmenuIn, menu_id: UUID):
        result = self.database_repository.create_submenu(
            submenu=submenu, menu_id=menu_id)
        self.cache.save_cache(subject=result, submenu_id=result.id)
        return result

    def update(self, menu_id: UUID, submenu_id: UUID, submenu: SubmenuIn):
        result = self.database_repository.update_submenu(
            menu_id=menu_id, submenu_id=submenu_id, submenu=submenu)
        self.cache.save_cache(subject=result, submenu_id=result.id)
        return result

    def delete(self, submenu_id: UUID):
        self.cache.delete_cache(submenu_id=submenu_id)
        return self.database_repository.delete_submenu(submenu_id=submenu_id)
