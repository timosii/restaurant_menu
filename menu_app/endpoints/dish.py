from ..schemas import DishOut, DishIn, DeleteMSG
from ..cruds.dish import (get_dish,
                          get_dishes,
                          create_dish,
                          update_dish,
                          delete_dish)
from ..database import get_db
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import Depends, status, APIRouter


prefix = "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes"
router = APIRouter(prefix=prefix)


@router.get('/', response_model=list[DishOut],
            status_code=status.HTTP_200_OK)
def reading_dishes(menu_id: UUID,
                   submenu_id: UUID,
                   db: Session = Depends(get_db)):
    dishes = get_dishes(submenu_id=submenu_id, db=db)
    for dish in dishes:
        dish.price = str(dish.price)
    return dishes


@router.get("/{dish_id}",
            response_model=DishOut)
def reading_dish(dish_id: UUID,
                 db: Session = Depends(get_db)):
    current_dish = get_dish(dish_id=dish_id, db=db)
    current_dish.price = str(current_dish.price)
    return current_dish


@router.post("/", response_model=DishOut,
             status_code=status.HTTP_201_CREATED)
def creating_dish(menu_id: UUID,
                  submenu_id: UUID,
                  dish: DishIn,
                  db: Session = Depends(get_db)):
    current_dish = create_dish(menu_id=menu_id,
                               submenu_id=submenu_id,
                               dish=dish,
                               db=db)
    current_dish.price = str(current_dish.price)
    return current_dish


@router.patch("/{dish_id}",
              response_model=DishOut)
def updating_dish(menu_id: UUID,
                  submenu_id: UUID,
                  dish_id: UUID,
                  dish: DishIn,
                  db: Session = Depends(get_db)):
    dish_to_update = update_dish(menu_id=menu_id,
                                 submenu_id=submenu_id,
                                 dish_id=dish_id,
                                 dish=dish,
                                 db=db)
    dish_to_update.price = str(dish_to_update.price)
    return dish_to_update


@router.delete("/{dish_id}",
               response_model=DeleteMSG,
               status_code=status.HTTP_200_OK)
def deleting_dish(menu_id: UUID,
                  submenu_id: UUID,
                  dish_id: UUID,
                  db: Session = Depends(get_db)):
    return delete_dish(menu_id=menu_id,
                       submenu_id=submenu_id,
                       dish_id=dish_id,
                       db=db)
