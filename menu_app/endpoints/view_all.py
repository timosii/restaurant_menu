from fastapi import APIRouter, Depends, status

from menu_app.schemas import MenuAllOut
from menu_app.services.view_all_service import ViewAllService

router = APIRouter(prefix='/api/v1/viewall')


@router.get('/', response_model=list[MenuAllOut],
            status_code=status.HTTP_200_OK)
async def reading_all(viewall: ViewAllService = Depends()) -> list[MenuAllOut]:
    '''
    Вывод всех меню со всем связанными подменю и со всеми связанными блюдами
    '''
    return await viewall.get_all()
