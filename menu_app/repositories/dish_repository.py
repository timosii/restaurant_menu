from ..schemas import DishIn
from ..models import Dish
from .errors import not_found, success_delete
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from fastapi import Depends
from ..database import get_db

SAMPLE = 'dish'


class DishRepository:
    def __init__(self, session: Session = Depends(get_db)) -> None:
        self.session = session
        self.model = Dish

    def get_dishes(self, submenu_id: UUID):
        current_dishes = self.session.query(Dish).filter(
            Dish.parent_submenu_id == submenu_id).all()
        for dish in current_dishes:
            dish.price = str(dish.price)
        return current_dishes

    def get_dish(self, dish_id: UUID):
        current_dish = self.session.query(Dish).filter(
            Dish.id == dish_id).first()
        if current_dish is None:
            not_found(SAMPLE)
        current_dish.price = str(current_dish.price)
        return current_dish

    def create_dish(self,
                    submenu_id: UUID,
                    dish: DishIn):
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

    def update_dish(self,
                    submenu_id: UUID,
                    dish_id: UUID,
                    dish: DishIn):
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
                    dish_id: UUID):
        dish_for_delete = self.session.query(Dish).filter(
                Dish.id == dish_id).first()
        if dish_for_delete is None:
            not_found(SAMPLE)
        self.session.delete(dish_for_delete)
        self.session.commit()
        return success_delete(SAMPLE)
