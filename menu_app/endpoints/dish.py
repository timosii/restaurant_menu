from .. import schemas, models
from ..cruds.dish import (get_dish, 
                   get_dishes, 
                   create_dish, 
                   update_dish, 
                   delete_dish)
from ..database import engine, get_db
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import Depends, status, FastAPI, APIRouter


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router = APIRouter(prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")


# Просмотр списка блюд
@router.get('/', response_model=list[schemas.DishOut])
def reading_dishes(menu_id: UUID, 
               submenu_id: UUID, 
               db: Session = Depends(get_db)):
    dishes = get_dishes(submenu_id=submenu_id, db=db)
    for dish in dishes:
        dish.price = str(dish.price)
    return dishes

# Посмотреть определённое блюдо
@router.get("/{dish_id}", 
         response_model=schemas.DishOut)
def reading_dish(dish_id: UUID, 
                         db: Session = Depends(get_db)
                         ):
    current_dish = get_dish(dish_id=dish_id, db=db)
    current_dish.price = str(current_dish.price)
    return current_dish

# Создать блюдо
@router.post("/", response_model=schemas.DishOut, 
             status_code=status.HTTP_201_CREATED)
def creating_dish(menu_id: UUID, 
                submenu_id: UUID, 
                dish: schemas.DishIn, 
                db: Session = Depends(get_db)):
    current_dish = create_dish(menu_id=menu_id, 
                                    submenu_id=submenu_id, 
                                    dish=dish, 
                                    db=db)
    current_dish.price = str(current_dish.price)
    return current_dish

# Обновить блюдо
@router.patch("/{dish_id}", 
           response_model=schemas.DishOut)
def updating_dish(menu_id: UUID, 
                        submenu_id: UUID, 
                        dish_id: UUID, 
                        dish: schemas.DishIn, 
                        db: Session = Depends(get_db)):
    dish_to_update = update_dish(menu_id=menu_id, 
                                      submenu_id=submenu_id, 
                                      dish_id=dish_id, 
                                      dish=dish, 
                                      db=db)
    dish_to_update.price = str(dish_to_update.price)
    return dish_to_update

# Удалить блюдо
@router.delete("/{dish_id}", response_model=schemas.DeleteMSG)
def deleting_dish(menu_id: UUID, 
                submenu_id: UUID, 
                dish_id: UUID, 
                db: Session = Depends(get_db)):
    return delete_dish(menu_id=menu_id, 
                     submenu_id=submenu_id, 
                     dish_id=dish_id, 
                     db=db)
    