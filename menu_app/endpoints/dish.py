from ..schemas import DishOut, DishIn, DeleteMSG
from uuid import UUID
from fastapi import Depends, status, APIRouter
from menu_app.services.dish_service import DishService


prefix = "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes"
router = APIRouter(prefix=prefix)


@router.get('/', response_model=list[DishOut],
            status_code=status.HTTP_200_OK)
def reading_dishes(submenu_id: UUID,
                   dish: DishService = Depends()):
    return dish.get_all(submenu_id=submenu_id)


@router.get("/{dish_id}",
            response_model=DishOut,
            status_code=status.HTTP_200_OK)
def reading_dish(dish_id: UUID,
                 dish: DishService = Depends()):
    return dish.get_one(dish_id=dish_id)


@router.post("/", response_model=DishOut,
             status_code=status.HTTP_201_CREATED)
def creating_dish(submenu_id: UUID,
                  dish_data: DishIn,
                  dish: DishService = Depends()):
    return dish.create(submenu_id=submenu_id, dish=dish_data)


@router.patch("/{dish_id}",
              response_model=DishOut,
              status_code=status.HTTP_200_OK)
def updating_dish(submenu_id: UUID,
                  dish_id: UUID,
                  dish_data: DishIn,
                  dish: DishService = Depends()):
    return dish.update(
        submenu_id=submenu_id, dish_id=dish_id, dish=dish_data)


@router.delete("/{dish_id}",
               response_model=DeleteMSG,
               status_code=status.HTTP_200_OK)
def deleting_dish(dish_id: UUID,
                  dish: DishService = Depends()):
    return dish.delete(dish_id=dish_id)
