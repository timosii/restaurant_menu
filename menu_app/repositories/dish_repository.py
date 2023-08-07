from uuid import UUID, uuid4

from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Dish
from ..schemas import DishIn, DishOut
from .errors import already_exist, not_found, success_delete

SAMPLE = 'dish'


class DishRepository:
    def __init__(self, session: Session = Depends(get_db)) -> None:
        self.session = session
        self.model = Dish

    def get_dishes(self, submenu_id: UUID) -> list[DishOut]:
        current_dishes = self.session.query(Dish).filter(
            Dish.parent_submenu_id == submenu_id).all()
        for dish in current_dishes:
            dish.price = str(dish.price)
        return current_dishes

    def create_dish(self,
                    submenu_id: UUID,
                    dish: DishIn) -> DishOut:
        self.check_dish_by_title(dish_title=dish.title)
        db_dish = Dish(id=uuid4(),
                       title=dish.title,
                       description=dish.description,
                       price=dish.price,
                       parent_submenu_id=submenu_id)
        self.session.add(db_dish)
        self.session.commit()
        self.session.refresh(db_dish)
        db_dish.price = str(db_dish.price)
        return db_dish

    def get_dish(self, dish_id: UUID) -> DishOut:
        current_dish = self.session.query(Dish).filter(
            Dish.id == dish_id).first()
        if current_dish is None:
            not_found(SAMPLE)
        current_dish.price = str(current_dish.price)
        return current_dish

    def check_dish_by_title(self, dish_title: str) -> None:
        db_menu = self.session.query(Dish).filter(
            Dish.title == dish_title).first()
        if db_menu:
            already_exist(SAMPLE)
        return

    def update_dish(self,
                    submenu_id: UUID,
                    dish_id: UUID,
                    dish: DishIn) -> DishOut:
        db_dish = self.get_dish(dish_id=dish_id)
        if db_dish is None:
            not_found(SAMPLE)
        dish_to_update = self.session.query(Dish).filter(
            Dish.id == dish_id,
            Dish.parent_submenu_id == submenu_id).first()
        dish_to_update.title = dish.title
        dish_to_update.description = dish.description
        dish_to_update.price = dish.price
        self.session.add(dish_to_update)
        self.session.commit()
        dish_to_update.price = str(dish_to_update.price)
        return dish_to_update

    def delete_dish(self,
                    dish_id: UUID) -> JSONResponse:
        dish_for_delete = self.session.query(Dish).filter(
            Dish.id == dish_id).first()
        if dish_for_delete is None:
            not_found(SAMPLE)
        self.session.delete(dish_for_delete)
        self.session.commit()
        return success_delete(SAMPLE)
