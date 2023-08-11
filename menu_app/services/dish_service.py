from uuid import UUID

from fastapi import Depends
from fastapi.responses import JSONResponse

from menu_app.repositories.dish_repository import DishRepository
from menu_app.schemas import DishIn, DishOut
from menu_app.services.cache import CacheDish


class DishService:

    def __init__(self,
                 database_repository: DishRepository = Depends()) -> None:
        self.database_repository = database_repository
        self.cache = CacheDish()

    async def get_all(self, menu_id: UUID,
                      submenu_id: UUID) -> list[DishOut]:
        if await self.cache.check_stage(prefix=f'Dishes:{submenu_id}:{menu_id}'):
            return await self.cache.load_stage(
                prefix=f'Dishes:{submenu_id}:{menu_id}')
        result = await self.database_repository.get_dishes(submenu_id=submenu_id)
        await self.cache.save_stage(subject=result,
                                    prefix=f'Dishes:{submenu_id}:{menu_id}')
        return result

    async def get_one(self, menu_id: UUID,
                      submenu_id: UUID,
                      dish_id: UUID) -> DishOut | None:
        if await self.cache.check_cache(menu_id=menu_id,
                                        submenu_id=submenu_id,
                                        dish_id=dish_id):
            return await self.cache.load_cache(menu_id=menu_id,
                                               submenu_id=submenu_id,
                                               dish_id=dish_id)
        result = await self.database_repository.get_dish(dish_id=dish_id)
        await self.cache.save_cache(subject=result,
                                    menu_id=menu_id,
                                    submenu_id=submenu_id,
                                    dish_id=dish_id)
        return result

    async def create(self, menu_id: UUID,
                     submenu_id: UUID, dish: DishIn) -> DishOut:
        result = await self.database_repository.create_dish(
            submenu_id=submenu_id, dish=dish)
        await self.cache.del_all_stages(menu_id=menu_id, submenu_id=submenu_id)
        await self.cache.delete(menu_id=menu_id)
        await self.cache.delete(menu_id=menu_id, submenu_id=submenu_id)
        await self.cache.save_cache(subject=result,
                                    menu_id=menu_id,
                                    submenu_id=submenu_id,
                                    dish_id=result.id)
        return result

    async def update(self, menu_id: UUID,
                     submenu_id: UUID,
                     dish_id: UUID, dish: DishIn) -> DishOut:
        result = await self.database_repository.update_dish(
            submenu_id=submenu_id, dish_id=dish_id, dish=dish)
        await self.cache.del_stage(prefix=f'Dishes:{submenu_id}:{menu_id}')
        await self.cache.save_cache(subject=result, menu_id=menu_id,
                                    submenu_id=submenu_id, dish_id=dish_id)
        return result

    async def delete(self, menu_id: UUID,
                     submenu_id: UUID, dish_id: UUID) -> JSONResponse:
        await self.cache.delete_cache(menu_id=menu_id,
                                      submenu_id=submenu_id, dish_id=dish_id)
        return await self.database_repository.delete_dish(dish_id=dish_id)
