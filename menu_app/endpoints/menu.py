from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from menu_app.services.menu_service import MenuService

from .. import models
from ..database import engine
from ..schemas import DeleteMSG, MenuIn, MenuOut

models.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix='/api/v1/menus')


@router.get('/', response_model=list[MenuOut],
            status_code=status.HTTP_200_OK)
def reading_menus(menu: MenuService = Depends()) -> list[MenuOut]:
    return menu.get_all()


@router.get('/{menu_id}',
            response_model=MenuOut,
            status_code=status.HTTP_200_OK)
def reading_menu(menu_id: UUID,
                 menu: MenuService = Depends()) -> MenuOut | None:
    return menu.get_one(menu_id=menu_id)


@router.post('/', response_model=MenuOut,
             status_code=status.HTTP_201_CREATED)
def creating_menu(menu_data: MenuIn,
                  menu: MenuService = Depends()) -> MenuOut:
    return menu.create(menu=menu_data)


@router.patch('/{menu_id}',
              response_model=MenuOut,
              status_code=status.HTTP_200_OK)
def updating_menu(menu_data: MenuIn,
                  menu_id: UUID, menu: MenuService = Depends()) -> MenuOut:
    return menu.update(menu=menu_data, menu_id=menu_id)


@router.delete('/{menu_id}',
               response_model=DeleteMSG,
               status_code=status.HTTP_200_OK)
def deleting_menu(menu_id: UUID,
                  menu: MenuService = Depends()) -> JSONResponse:
    return menu.delete(menu_id=menu_id)
