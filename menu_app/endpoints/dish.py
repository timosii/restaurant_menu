from ..schemas import DishOut, DishIn, DeleteMSG
from uuid import UUID
from fastapi import Depends, status, APIRouter
from menu_app.repositories.dish_repository import DishRepository


prefix = "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes"
router = APIRouter(prefix=prefix)


@router.get('/', response_model=list[DishOut],
            status_code=status.HTTP_200_OK)
def reading_dishes(submenu_id: UUID,
                   dish: DishRepository = Depends()):
    return dish.get_dishes(submenu_id)


@router.get("/{dish_id}",
            response_model=DishOut)
def reading_dish(dish_id: UUID,
                 dish: DishRepository = Depends()):
    return dish.get_dish(dish_id)


@router.post("/", response_model=DishOut,
             status_code=status.HTTP_201_CREATED)
def creating_dish(submenu_id: UUID,
                  dish_data: DishIn,
                  dish: DishRepository = Depends()):
    return dish.create_dish(submenu_id=submenu_id, dish=dish_data)


@router.patch("/{dish_id}",
              response_model=DishOut)
def updating_dish(submenu_id: UUID,
                  dish_id: UUID,
                  dish_data: DishIn,
                  dish: DishRepository = Depends()):
    return dish.update_dish(submenu_id, dish_id, dish_data)


@router.delete("/{dish_id}",
               response_model=DeleteMSG,
               status_code=status.HTTP_200_OK)
def deleting_dish(dish_id: UUID,
                  dish: DishRepository = Depends()):
    return dish.delete_dish(dish_id)
