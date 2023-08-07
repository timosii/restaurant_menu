from uuid import UUID

from fastapi import APIRouter, Depends, status

from menu_app.services.dish_service import DishService

from ..schemas import DeleteMSG, DishIn, DishOut

prefix = '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes'
router = APIRouter(prefix=prefix)


@router.get('/', response_model=list[DishOut],
            status_code=status.HTTP_200_OK)
def reading_dishes(submenu_id: UUID,
                   dish: DishService = Depends()) -> list[DishOut]:
    return dish.get_all(submenu_id=submenu_id)


@router.get('/{dish_id}',
            response_model=DishOut,
            status_code=status.HTTP_200_OK)
def reading_dish(menu_id: UUID,
                 submenu_id: UUID,
                 dish_id: UUID,
                 dish: DishService = Depends()) -> DishOut | None:
    return dish.get_one(menu_id=menu_id,
                        submenu_id=submenu_id,
                        dish_id=dish_id)


@router.post('/', response_model=DishOut,
             status_code=status.HTTP_201_CREATED)
def creating_dish(menu_id: UUID,
                  submenu_id: UUID,
                  dish_data: DishIn,
                  dish: DishService = Depends()) -> DishOut:
    return dish.create(menu_id=menu_id,
                       submenu_id=submenu_id,
                       dish=dish_data)


@router.patch('/{dish_id}',
              response_model=DishOut,
              status_code=status.HTTP_200_OK)
def updating_dish(menu_id: UUID,
                  submenu_id: UUID,
                  dish_id: UUID,
                  dish_data: DishIn,
                  dish: DishService = Depends()) -> DishOut:
    return dish.update(menu_id=menu_id,
                       submenu_id=submenu_id,
                       dish_id=dish_id, dish=dish_data)


@router.delete('/{dish_id}',
               response_model=DeleteMSG,
               status_code=status.HTTP_200_OK)
def deleting_dish(menu_id: UUID,
                  submenu_id: UUID,
                  dish_id: UUID,
                  dish: DishService = Depends()) -> DishOut:
    return dish.delete(menu_id=menu_id,
                       submenu_id=submenu_id, dish_id=dish_id)
