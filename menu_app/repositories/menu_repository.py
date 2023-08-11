from uuid import UUID, uuid4

from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from menu_app.database import get_db
from menu_app.models import Dish, Menu, Submenu
from menu_app.repositories.errors import already_exist, not_found, success_delete
from menu_app.schemas import MenuIn, MenuOut

SAMPLE = 'menu'


class MenuRepository:
    def __init__(self, session: AsyncSession = Depends(get_db)) -> None:
        self.session = session
        self.model = Menu

    async def get_menus(self) -> list[MenuOut]:
        stmt = select(Menu)
        result = await self.session.execute(stmt)
        menus = result.scalars().all()

        for menu in menus:
            menu.submenus_count = await self.submenu_count(menu_id=menu.id)
            menu.dishes_count = await self.dish_count(menu_id=menu.id)

        return menus

    async def create_menu(self, menu: MenuIn) -> MenuOut:
        await self.check_menu_by_title(menu_title=menu.title)
        db_menu = Menu(id=uuid4(),
                       title=menu.title,
                       description=menu.description)
        self.session.add(db_menu)
        await self.session.commit()
        await self.session.refresh(db_menu)
        db_menu.submenus_count = await self.submenu_count(menu_id=db_menu.id)
        db_menu.dishes_count = await self.dish_count(menu_id=db_menu.id)
        return db_menu

    async def get_menu(self, menu_id: UUID) -> MenuOut:
        stmt = select(Menu).where(Menu.id == menu_id)
        result = await self.session.execute(stmt)
        db_menu = result.scalars().first()

        if db_menu is None:
            not_found(SAMPLE)

        db_menu.submenus_count = await self.submenu_count(menu_id=db_menu.id)
        db_menu.dishes_count = await self.dish_count(menu_id=db_menu.id)

        return db_menu

    async def check_menu_by_title(self, menu_title: str) -> None:
        stmt = select(Menu).where(Menu.title == menu_title)
        result = await self.session.execute(stmt)
        db_menu = result.scalars().first()

        if db_menu:
            already_exist(SAMPLE)
        return

    async def delete_menu(self, menu_id: UUID) -> JSONResponse:
        stmt = select(Menu).where(Menu.id == menu_id)
        result = await self.session.execute(stmt)
        menu_for_delete = result.scalars().first()

        if menu_for_delete is None:
            not_found(SAMPLE)

        await self.session.delete(menu_for_delete)
        await self.session.commit()
        return success_delete(SAMPLE)

    async def update_menu(self, menu: MenuIn, menu_id: UUID) -> MenuOut:
        await self.check_menu_by_title(menu_title=menu.title)
        stmt = select(Menu).where(Menu.id == menu_id)
        result = await self.session.execute(stmt)
        db_menu = result.scalars().first()

        if db_menu is None:
            not_found(SAMPLE)

        db_menu.title = menu.title
        db_menu.description = menu.description

        self.session.add(db_menu)
        await self.session.commit()
        db_menu.submenus_count = await self.submenu_count(menu_id=db_menu.id)
        db_menu.dishes_count = await self.dish_count(menu_id=db_menu.id)

        return db_menu

    async def submenu_count(self, menu_id: UUID) -> int:
        stmt = select(func.count()).select_from(Menu).join(
            Submenu, Menu.id == Submenu.parent_menu_id).where(
            Menu.id == menu_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def dish_count(self, menu_id: UUID) -> int:
        stmt = select(func.count()).select_from(Menu).join(
            Submenu, Menu.id == Submenu.parent_menu_id).outerjoin(
            Dish, Submenu.id == Dish.parent_submenu_id).where(
            Menu.id == menu_id)
        result = await self.session.execute(stmt)
        return result.scalar()
