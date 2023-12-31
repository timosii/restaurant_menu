from uuid import UUID

from fastapi import Depends
from fastapi.responses import JSONResponse

from menu_app.admin_utils.discount import Discount
from menu_app.cache.cache_subjects import CacheDish
from menu_app.repositories.dish_repository import DishRepository
from menu_app.schemas import DishIn, DishOut


class DishService:

    def __init__(self,
                 database_repository: DishRepository = Depends()) -> None:
        self.database_repository = database_repository
        self.cache = CacheDish()
        self.discount = Discount()

    async def get_all(self, menu_id: UUID,
                      submenu_id: UUID) -> list[DishOut]:
        if await self.cache.check_list(prefix=f'Dishes:{submenu_id}:{menu_id}'):
            _result = await self.cache.load_list(
                prefix=f'Dishes:{submenu_id}:{menu_id}')
            model_result = []
            for menu_data in _result:
                model_result.append(DishOut(**menu_data))
            result = model_result
        else:
            result = await self.database_repository.get_dishes(submenu_id=submenu_id)
            await self.cache.save_list(subject=result,
                                       prefix=f'Dishes:{submenu_id}:{menu_id}')
        for dish in result:
            price_discount = self.discount.calculate(dish_id=dish.id)
            dish.price = price_discount if price_discount else dish.price
        return result

    async def get_one(self, menu_id: UUID,
                      submenu_id: UUID,
                      dish_id: UUID) -> DishOut | None:
        if await self.cache.check_cache(menu_id=menu_id,
                                        submenu_id=submenu_id,
                                        dish_id=dish_id):
            result = await self.cache.load_cache(menu_id=menu_id,
                                                 submenu_id=submenu_id,
                                                 dish_id=dish_id)
        else:
            result = await self.database_repository.get_dish(dish_id=dish_id)
            await self.cache.save_cache(subject=result,
                                        menu_id=menu_id,
                                        submenu_id=submenu_id,
                                        dish_id=dish_id)
        if result:
            price_discount = self.discount.calculate(dish_id=result.id)
            result.price = price_discount if price_discount else result.price
            return result
        return None

    async def create(self, menu_id: UUID,
                     submenu_id: UUID, dish: DishIn) -> DishOut:
        result = await self.database_repository.create_dish(
            submenu_id=submenu_id, dish=dish)
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
        await self.cache.save_cache(subject=result, menu_id=menu_id,
                                    submenu_id=submenu_id, dish_id=dish_id)
        return result

    async def delete(self, dish_id: UUID) -> JSONResponse:
        return await self.database_repository.delete_dish(dish_id=dish_id)
