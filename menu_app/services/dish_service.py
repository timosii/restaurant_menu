import json
import redis
from fastapi.encoders import jsonable_encoder
from fastapi import Depends
from ..schemas import DishIn, DishOut
from ..repositories.dish_repository import DishRepository
from uuid import UUID
from typing import Optional


class CacheDish:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_conn = redis.Redis(host=host, port=port, db=db)

    def save_cache(self, subject: DishOut, dish_id: UUID) -> None:
        self.redis_conn.set(f'dish:{dish_id}', json.dumps(
            jsonable_encoder(subject)))

    def load_cache(self, dish_id: UUID) -> Optional[DishOut]:
        cached_data = self.redis_conn.get(f'dish:{dish_id}')
        if cached_data:
            return DishOut(**json.loads(cached_data))
        return None

    def check_cache(self, dish_id: UUID) -> bool:
        return self.redis_conn.exists(f'dish:{dish_id}')

    def delete_cache(self, dish_id: UUID) -> int:
        return self.redis_conn.delete(f'dish:{dish_id}')


class DishService:

    def __init__(self, database_repository: DishRepository = Depends()):
        self.database_repository = database_repository
        self.cache = CacheDish()

    def get_all(self, submenu_id: UUID):
        return self.database_repository.get_dishes(submenu_id=submenu_id)

    def get_one(self, dish_id: UUID):
        if self.cache.check_cache(dish_id=dish_id):
            return self.cache.load_cache(dish_id=dish_id)
        result = self.database_repository.get_dish(dish_id=dish_id)
        self.cache.save_cache(subject=result, dish_id=result.id)
        return result

    def create(self, submenu_id: UUID, dish: DishIn):
        result = self.database_repository.create_dish(
            submenu_id=submenu_id, dish=dish)
        self.cache.save_cache(subject=result, dish_id=result.id)
        return result

    def update(self, submenu_id: UUID, dish_id: UUID, dish: DishIn):
        result = self.database_repository.update_dish(
            submenu_id=submenu_id, dish_id=dish_id, dish=dish)
        self.cache.save_cache(subject=result, dish_id=dish_id)
        return result

    def delete(self, dish_id: UUID):
        self.cache.delete_cache(dish_id=dish_id)
        return self.database_repository.delete_dish(dish_id=dish_id)
