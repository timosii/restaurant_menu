from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse

from menu_app.schemas import DeleteMSG, MenuIn, MenuOut
from menu_app.services.menu_service import MenuService

router = APIRouter(prefix='/api/v1/menus')


@router.get('/', response_model=list[MenuOut],
            status_code=status.HTTP_200_OK)
async def reading_menus(menu: MenuService = Depends()) -> list[MenuOut]:
    '''
    Получение списка меню в виде экземпляров модели MenuOut.
    Если ни одного меню не найдено, вернётся пустой список.
    '''
    return await menu.get_all()


@router.get('/{menu_id}',
            response_model=MenuOut,
            status_code=status.HTTP_200_OK)
async def reading_menu(menu_id: UUID,
                       menu: MenuService = Depends()) -> MenuOut | None:
    '''
    Получение меню по id в виде экземпляра модели MenuOut.
    Если меню не найдено - будет возбуждено исключение: ошибка 404
    "menu not found"
    '''
    return await menu.get_one(menu_id=menu_id)


@router.post('/', response_model=MenuOut,
             status_code=status.HTTP_201_CREATED)
async def creating_menu(background_tasks: BackgroundTasks, menu_data: MenuIn,
                        menu: MenuService = Depends()) -> MenuOut:
    '''
    Создание меню. Функция принимает экземпляр модели MenuIn.
    Возвращает экземпляр модели MenuOut.
    Если меню с таким названием уже присутствует в базе -
    будет возбуждено исключение: ошибка 400 "menu already exist"
    '''
    background_tasks.add_task(menu.cache.create_invalidation)
    return await menu.create(menu=menu_data)


@router.patch('/{menu_id}',
              response_model=MenuOut,
              status_code=status.HTTP_200_OK)
async def updating_menu(background_tasks: BackgroundTasks,
                        menu_data: MenuIn,
                        menu_id: UUID,
                        menu: MenuService = Depends()) -> MenuOut:
    '''
    Обновление меню. Функция принимает экземпляр модели MenuIn и id меню,
    которое нужно обновить. Возвращает экземпляр модели MenuOut.
    Если меню не найдено - будет возбуждено исключение: ошибка 404
    "menu not found"
    '''
    background_tasks.add_task(menu.cache.update_invalidation)
    return await menu.update(menu=menu_data, menu_id=menu_id)


@router.delete('/{menu_id}',
               response_model=DeleteMSG,
               status_code=status.HTTP_200_OK)
async def deleting_menu(background_tasks: BackgroundTasks,
                        menu_id: UUID,
                        menu: MenuService = Depends()) -> JSONResponse:
    '''
    Удаление меню. Функция принимает id меню,
    которое нужно удалить. Возвращает ответ в формате JSON с
    сообщением об успешном удалении.
    Если меню не найдено - будет возбуждено исключение: ошибка 404
    "menu not found"
    '''
    background_tasks.add_task(menu.cache.delete_invalidation, menu_id=menu_id)
    return await menu.delete(menu_id=menu_id)
