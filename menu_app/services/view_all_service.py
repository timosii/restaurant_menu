from fastapi import Depends

from menu_app.admin_utils.discount import Discount
from menu_app.cache.cache_subjects import CacheViewAll
from menu_app.repositories.view_all_repository import ViewAllRepository
from menu_app.schemas import MenuAllOut


class ViewAllService:
    def __init__(self,
                 database_repository: ViewAllRepository = Depends()) -> None:
        self.database_repository = database_repository
        self.cache = CacheViewAll()
        self.discount = Discount()

    async def get_all(self) -> list[MenuAllOut]:
        if await self.cache.check_list(prefix='ViewAll'):
            _result = await self.cache.load_list(prefix='ViewAll')
            model_result = []
            for menu_data in _result:
                model_result.append(MenuAllOut(**menu_data))
            result = model_result
        else:
            result = await self.database_repository.get_all()
        await self.cache.save_list(subject=result, prefix='ViewAll')

        for menu in result:
            if menu.submenus:
                for submenu in menu.submenus:
                    if submenu.dishes:
                        for dish in submenu.dishes:
                            price_discount = self.discount.calculate(dish_id=dish.id)
                            dish.price = price_discount if price_discount else dish.price

        return result
