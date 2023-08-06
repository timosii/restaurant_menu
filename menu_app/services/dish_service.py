from fastapi import Depends
from ..schemas import DishIn
from ..repositories.dish_repository import DishRepository
from uuid import UUID


class DishService:

    def __init__(self, database_repository: DishRepository = Depends()):
        self.database_repository = database_repository

    def get_all(self, submenu_id: UUID):
        return self.database_repository.get_dishes(submenu_id=submenu_id)

    def get_one(self, dish_id: UUID):
        return self.database_repository.get_dish(dish_id=dish_id)

    def create(self, submenu_id: UUID, dish: DishIn):
        return self.database_repository.create_dish(
            submenu_id=submenu_id, dish=dish)

    def update(self, submenu_id: UUID, dish_id: UUID, dish: DishIn):
        return self.database_repository.update_dish(
            submenu_id=submenu_id, dish_id=dish_id, dish=dish)

    def delete(self, dish_id: UUID):
        return self.database_repository.delete_dish(dish_id=dish_id)
