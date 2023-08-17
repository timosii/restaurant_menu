# mypy: disable-error-code="arg-type"
from uuid import UUID, uuid4

from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from menu_app.database import get_db
from menu_app.models import Dish
from menu_app.repositories.errors import already_exist, not_found, success_delete
from menu_app.schemas import DishIn, DishOut

SAMPLE = 'dish'


class DishRepository:
    def __init__(self, session: AsyncSession = Depends(get_db)) -> None:
        self.session = session

    async def get_dishes(self, submenu_id: UUID) -> list[DishOut]:
        stmt = select(Dish).where(Dish.parent_submenu_id == submenu_id)
        result = await self.session.execute(stmt)
        current_dishes = result.scalars().all()

        for dish in current_dishes:
            dish.price = f'{dish.price:.2f}'

        return current_dishes

    async def create_dish(self,
                          submenu_id: UUID,
                          dish: DishIn) -> DishOut:
        await self.check_dish_by_id(dish_id=dish.id)
        await self.check_dish_by_title(dish_title=dish.title)
        db_dish = Dish(id=dish.id if dish.id else uuid4(),
                       title=dish.title,
                       description=dish.description,
                       price=dish.price,
                       parent_submenu_id=submenu_id)
        self.session.add(db_dish)
        await self.session.commit()
        await self.session.refresh(db_dish)
        db_dish.price = f'{db_dish.price:.2f}'
        return db_dish

    async def get_dish(self, dish_id: UUID) -> DishOut:
        stmt = select(Dish).where(Dish.id == dish_id)
        result = await self.session.execute(stmt)
        current_dish = result.scalars().first()

        if current_dish is None:
            not_found(SAMPLE)

        current_dish.price = f'{current_dish.price:.2f}'
        return current_dish

    async def check_dish_by_title(self, dish_title: str) -> None:
        stmt = select(Dish).where(Dish.title == dish_title)
        result = await self.session.execute(stmt)
        db_menu = result.scalars().first()

        if db_menu:
            already_exist(SAMPLE)
        return

    async def check_dish_by_id(self, dish_id: UUID) -> None:
        stmt = select(Dish).where(Dish.id == dish_id)
        result = await self.session.execute(stmt)
        db_menu = result.scalars().first()

        if db_menu:
            already_exist(SAMPLE)
        return

    async def update_dish(self,
                          submenu_id: UUID,
                          dish_id: UUID,
                          dish: DishIn) -> DishOut:
        stmt = select(Dish).where(
            Dish.id == dish_id,
            Dish.parent_submenu_id == submenu_id)
        result = await self.session.execute(stmt)
        db_dish = result.scalars().first()

        if db_dish is None:
            not_found(SAMPLE)

        db_dish.title = dish.title
        db_dish.description = dish.description
        db_dish.price = dish.price

        self.session.add(db_dish)
        await self.session.commit()
        db_dish.price = str(db_dish.price)
        return db_dish

    async def delete_dish(self,
                          dish_id: UUID) -> JSONResponse:
        stmt = select(Dish).where(Dish.id == dish_id)
        result = await self.session.execute(stmt)
        dish_for_delete = result.scalars().first()

        if dish_for_delete is None:
            not_found(SAMPLE)

        await self.session.delete(dish_for_delete)
        await self.session.commit()
        return success_delete(SAMPLE)
