from .cache import CacheDish
from fastapi import Depends
from ..schemas import DishIn
from ..repositories.dish_repository import DishRepository
from uuid import UUID


class DishService:

    def __init__(self, database_repository: DishRepository = Depends()):
        self.database_repository = database_repository
        self.cache = CacheDish()

    def get_all(self, submenu_id: UUID):
        return self.database_repository.get_dishes(submenu_id=submenu_id)

    def get_one(self, submenu_id: UUID, dish_id: UUID):
        if self.cache.check_cache(submenu_id=submenu_id, dish_id=dish_id):
            return self.cache.load_cache(submenu_id=submenu_id,
                                         dish_id=dish_id)
        result = self.database_repository.get_dish(dish_id=dish_id)
        self.cache.save_cache(subject=result, dish_id=result.id)
        return result

    def create(self, menu_id: UUID,
               submenu_id: UUID, dish: DishIn):
        result = self.database_repository.create_dish(
            submenu_id=submenu_id, dish=dish)
        self.cache.save_cache(subject=result, menu_id=menu_id,
                              submenu_id=submenu_id, dish_id=result.id)
        return result

    def update(self, menu_id: UUID,
               submenu_id: UUID, dish_id: UUID, dish: DishIn):
        result = self.database_repository.update_dish(
            submenu_id=submenu_id, dish_id=dish_id, dish=dish)
        self.cache.save_cache(subject=result, menu_id=menu_id,
                              submenu_id=submenu_id, dish_id=dish_id)
        return result

    def delete(self, submenu_id: UUID, dish_id: UUID):
        self.cache.delete_cache(submenu_id=submenu_id, dish_id=dish_id)
        return self.database_repository.delete_dish(dish_id=dish_id)
