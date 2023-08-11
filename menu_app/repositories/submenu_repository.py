from uuid import UUID, uuid4

from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from menu_app.database import get_db
from menu_app.models import Dish, Submenu
from menu_app.repositories.errors import already_exist, not_found, success_delete
from menu_app.schemas import SubmenuIn, SubmenuOut

SAMPLE = 'submenu'


class SubmenuRepository:
    def __init__(self, session: AsyncSession = Depends(get_db)) -> None:
        self.session = session
        self.model = Submenu

    async def get_submenus(self, menu_id: UUID) -> list[SubmenuOut]:
        stmt = select(Submenu).where(Submenu.parent_menu_id == menu_id)
        result = await self.session.execute(stmt)
        submenus = result.scalars().all()

        for submenu in submenus:
            submenu.dishes_count = await self.dish_for_submenu_count(
                submenu_id=submenu.id)

        return submenus

    async def create_submenu(self,
                             submenu: SubmenuIn,
                             menu_id: UUID) -> SubmenuOut:
        await self.check_submenu_by_title(submenu_title=submenu.title)
        db_submenu = Submenu(id=uuid4(),
                             title=submenu.title,
                             description=submenu.description,
                             parent_menu_id=menu_id)
        self.session.add(db_submenu)
        await self.session.commit()
        await self.session.refresh(db_submenu)
        db_submenu.dishes_count = await self.dish_for_submenu_count(
            submenu_id=db_submenu.id)
        return db_submenu

    async def get_submenu(self, submenu_id: UUID) -> SubmenuOut:
        stmt = select(Submenu).where(Submenu.id == submenu_id)
        result = await self.session.execute(stmt)
        current_submenu = result.scalars().first()

        if current_submenu is None:
            not_found(SAMPLE)

        current_submenu.dishes_count = await self.dish_for_submenu_count(
            submenu_id=current_submenu.id)

        return current_submenu

    async def check_submenu_by_title(self, submenu_title: str) -> None:
        stmt = select(Submenu).where(Submenu.title == submenu_title)
        result = await self.session.execute(stmt)
        db_menu = result.scalars().first()

        if db_menu:
            already_exist(SAMPLE)

    async def delete_submenu(self, submenu_id: UUID) -> JSONResponse:
        stmt = select(Submenu).where(Submenu.id == submenu_id)
        result = await self.session.execute(stmt)
        submenu_for_delete = result.scalars().first()

        if submenu_for_delete is None:
            not_found(SAMPLE)

        await self.session.delete(submenu_for_delete)
        await self.session.commit()
        return success_delete(SAMPLE)

    async def update_submenu(self, menu_id: UUID,
                             submenu_id: UUID,
                             submenu: SubmenuIn) -> SubmenuOut:
        await self.check_submenu_by_title(submenu_title=submenu.title)
        stmt = select(Submenu).where(
            Submenu.id == submenu_id,
            Submenu.parent_menu_id == menu_id)
        result = await self.session.execute(stmt)
        db_submenu = result.scalars().first()

        if db_submenu is None:
            not_found(SAMPLE)

        db_submenu.title = submenu.title
        db_submenu.description = submenu.description

        self.session.add(db_submenu)
        await self.session.commit()
        db_submenu.dishes_count = await self.dish_for_submenu_count(
            submenu_id=db_submenu.id)

        return db_submenu

    async def dish_for_submenu_count(self, submenu_id: UUID) -> int:
        stmt = select(func.count()).select_from(Submenu).join(
            Dish, Submenu.id == Dish.parent_submenu_id).where(
            Submenu.id == submenu_id)
        result = await self.session.execute(stmt)
        return result.scalar()
