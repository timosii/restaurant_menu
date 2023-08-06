from ..schemas import SubmenuOut, SubmenuIn, DeleteMSG
from uuid import UUID
from fastapi import Depends, status, APIRouter
from menu_app.services.submenu_service import SubmenuService


router = APIRouter(prefix="/api/v1/menus/{menu_id}/submenus")


@router.get("/", response_model=list[SubmenuOut],
            status_code=status.HTTP_200_OK)
def reading_submenus(menu_id: UUID,
                     submenu: SubmenuService = Depends()):
    return submenu.get_all(menu_id=menu_id)


@router.get("/{submenu_id}",
            response_model=SubmenuOut,
            status_code=status.HTTP_200_OK)
def reading_submenu(menu_id: UUID,
                    submenu_id: UUID,
                    submenu: SubmenuService = Depends()):
    return submenu.get_one(menu_id=menu_id, submenu_id=submenu_id)


@router.post("/", response_model=SubmenuOut,
             status_code=status.HTTP_201_CREATED)
def creating_submenu(menu_id: UUID,
                     submenu_data: SubmenuIn,
                     submenu: SubmenuService = Depends()):
    return submenu.create(menu_id=menu_id, submenu=submenu_data)


@router.patch("/{submenu_id}",
              response_model=SubmenuOut,
              status_code=status.HTTP_200_OK)
def updating_submenu(menu_id: UUID,
                     submenu_id: UUID,
                     submenu_data: SubmenuIn,
                     submenu: SubmenuService = Depends()):
    return submenu.update(
        menu_id=menu_id, submenu_id=submenu_id, submenu=submenu_data)


@router.delete("/{submenu_id}",
               response_model=DeleteMSG,
               status_code=status.HTTP_200_OK)
def deleting_submenu(menu_id: UUID,
                     submenu_id: UUID,
                     submenu: SubmenuService = Depends()):
    return submenu.delete(menu_id=menu_id, submenu_id=submenu_id)
