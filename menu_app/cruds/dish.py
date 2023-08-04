from ..schemas import DishIn
from ..models import Dish
from .errors import not_found, message_deleted
from uuid import UUID, uuid4
from sqlalchemy.orm import Session


SAMPLE = 'dish'


def get_dishes(db: Session,
               submenu_id: UUID):
    current_dishes = db.query(Dish).filter(
        Dish.parent_submenu_id == submenu_id).all()
    return current_dishes


def get_dish(db: Session,
             dish_id: UUID):
    current_dish = db.query(Dish).filter(
        Dish.id == dish_id).first()
    if current_dish is None:
        not_found(SAMPLE)
    return current_dish


def create_dish(menu_id: UUID,
                submenu_id: UUID,
                dish: DishIn,
                db: Session):
    db_dish = Dish(id=uuid4(),
                   title=dish.title,
                   description=dish.description,
                   price=dish.price,
                   parent_submenu_id=submenu_id)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


def update_dish(menu_id: UUID,
                submenu_id: UUID,
                dish_id: UUID,
                dish: DishIn,
                db: Session):
    db_dish = get_dish(db, dish_id=dish_id)
    if db_dish is None:
        not_found(SAMPLE)
    dish_to_update = db.query(Dish).filter(
        Dish.id == dish_id,
        Dish.parent_submenu_id == submenu_id).first()
    dish_to_update.title = dish.title
    dish_to_update.description = dish.description
    dish_to_update.price = dish.price
    db.add(dish_to_update)
    db.commit()
    return dish_to_update


def delete_dish(menu_id: UUID,
                submenu_id: UUID,
                dish_id: UUID,
                db: Session):
    dish_for_delete = db.query(Dish).filter(
            Dish.id == dish_id).first()
    if dish_for_delete is None:
        not_found(SAMPLE)
    db.delete(dish_for_delete)
    db.commit()
    return message_deleted(SAMPLE)
