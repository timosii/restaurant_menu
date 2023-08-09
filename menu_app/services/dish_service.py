from uuid import UUID

from fastapi import Depends
from fastapi.responses import JSONResponse

from ..repositories.dish_repository import DishRepository
from ..schemas import DishIn, DishOut
from .cache import CacheDish


class DishService:

    def __init__(self,
                 database_repository: DishRepository = Depends()) -> None:
        self.database_repository = database_repository
        self.cache = CacheDish()

    def get_all(self, menu_id: UUID,
                submenu_id: UUID) -> list[DishOut]:
        if self.cache.check_stage(prefix=f'Dishes:{submenu_id}:{menu_id}'):
            return self.cache.load_stage(
                prefix=f'Dishes:{submenu_id}:{menu_id}')
        result = self.database_repository.get_dishes(submenu_id=submenu_id)
        self.cache.save_stage(subject=result,
                              prefix=f'Dishes:{submenu_id}:{menu_id}')
        return result

    def get_one(self, menu_id: UUID,
                submenu_id: UUID,
                dish_id: UUID) -> DishOut | None:
        if self.cache.check_cache(menu_id=menu_id,
                                  submenu_id=submenu_id,
                                  dish_id=dish_id):
            return self.cache.load_cache(menu_id=menu_id,
                                         submenu_id=submenu_id,
                                         dish_id=dish_id)
        result = self.database_repository.get_dish(dish_id=dish_id)
        self.cache.save_cache(subject=result,
                              menu_id=menu_id,
                              submenu_id=submenu_id,
                              dish_id=dish_id)
        return result

    def create(self, menu_id: UUID,
               submenu_id: UUID, dish: DishIn) -> DishOut:
        result = self.database_repository.create_dish(
            submenu_id=submenu_id, dish=dish)
        self.cache.del_all_stages(menu_id=menu_id, submenu_id=submenu_id)
        self.cache.delete(menu_id=menu_id)
        self.cache.delete(menu_id=menu_id, submenu_id=submenu_id)
        self.cache.save_cache(subject=result,
                              menu_id=menu_id,
                              submenu_id=submenu_id,
                              dish_id=result.id)
        return result

    def update(self, menu_id: UUID,
               submenu_id: UUID,
               dish_id: UUID, dish: DishIn) -> DishOut:
        result = self.database_repository.update_dish(
            submenu_id=submenu_id, dish_id=dish_id, dish=dish)
        self.cache.del_stage(prefix=f'Dishes:{submenu_id}:{menu_id}')
        self.cache.save_cache(subject=result, menu_id=menu_id,
                              submenu_id=submenu_id, dish_id=dish_id)
        return result

    def delete(self, menu_id: UUID,
               submenu_id: UUID, dish_id: UUID) -> JSONResponse:
        self.cache.delete_cache(menu_id=menu_id,
                                submenu_id=submenu_id, dish_id=dish_id)
        return self.database_repository.delete_dish(dish_id=dish_id)
