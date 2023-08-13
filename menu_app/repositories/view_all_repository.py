from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import defer, joinedload, selectinload

from menu_app.database import get_db
from menu_app.models import Dish, Menu, Submenu
from menu_app.schemas import MenuAllOut


class ViewAllRepository:
    def __init__(self, session: AsyncSession = Depends(get_db)) -> None:
        self.session = session

    async def get_all(self) -> list[MenuAllOut]:
        stmt = select(Menu).options(selectinload(Menu.submenus).options(
            joinedload(Submenu.dishes).defer(Dish.parent_submenu_id), defer(
                Submenu.parent_menu_id))).distinct()

        result = await self.session.execute(stmt)
        menu_list = result.scalars().all()
        for menu in menu_list:
            if menu.submenus:
                for submenu in menu.submenus:
                    if submenu.dishes:
                        for dish in submenu.dishes:
                            dish.price = str(dish.price)

        return menu_list
