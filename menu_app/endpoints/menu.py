from ..schemas import MenuOut, MenuIn, DeleteMSG
from uuid import UUID
from fastapi import Depends, status, APIRouter
from menu_app.repositories.menu_repository import MenuRepository


router = APIRouter(prefix="/api/v1/menus")


@router.get("/", response_model=list[MenuOut],
            status_code=status.HTTP_200_OK)
def reading_menus(menu: MenuRepository = Depends()):
    return menu.get_menus()


@router.post("/", response_model=MenuOut,
             status_code=status.HTTP_201_CREATED)
def creating_menu(menu_data: MenuIn,
                  menu: MenuRepository = Depends()):
    return menu.create_menu(menu_data)


@router.get("/{menu_id}",
            response_model=MenuOut,
            status_code=status.HTTP_200_OK)
def reading_menu(menu_id: UUID,
                 menu: MenuRepository = Depends()):
    return menu.get_menu(menu_id)


@router.delete("/{menu_id}",
               response_model=DeleteMSG,
               status_code=status.HTTP_200_OK)
def deleting_menu(menu_id: UUID,
                  menu: MenuRepository = Depends()):
    return menu.delete_menu(menu_id)


@router.patch("/{menu_id}",
              response_model=MenuOut)
def updating_menu(menu_data: MenuIn,
                  menu_id: UUID, menu: MenuRepository = Depends()):
    return menu.update_menu(menu_data, menu_id)
