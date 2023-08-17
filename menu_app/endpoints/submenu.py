from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse

from menu_app.schemas import DeleteMSG, SubmenuIn, SubmenuOut
from menu_app.services.submenu_service import SubmenuService

router = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus')


@router.get('/', response_model=list[SubmenuOut],
            status_code=status.HTTP_200_OK)
async def reading_submenus(menu_id: UUID,
                           submenu: SubmenuService = Depends()) -> list[SubmenuOut]:
    '''
    Функция принимает id меню, для которого отображает список подменю.
    Возвращает список подменю в виде экземпляров модели SubmenuOut.
    Если ни одного подменю не найдено, вернётся пустой список.
    '''
    return await submenu.get_all(menu_id=menu_id)


@router.get('/{submenu_id}',
            response_model=SubmenuOut,
            status_code=status.HTTP_200_OK)
async def reading_submenu(menu_id: UUID,
                          submenu_id: UUID,
                          submenu: SubmenuService = Depends()) -> SubmenuOut | None:
    '''
    Получение подменю в виде экземпляра модели SubmenuOut.
    Функция принимает id меню и id подменю, которое нужно найти.
    Если подменю не найдено - будет возбуждено исключение: ошибка 404
    "submenu not found"
    '''
    return await submenu.get_one(menu_id=menu_id, submenu_id=submenu_id)


@router.post('/', response_model=SubmenuOut,
             status_code=status.HTTP_201_CREATED)
async def creating_submenu(background_tasks: BackgroundTasks,
                           menu_id: UUID,
                           submenu_data: SubmenuIn,
                           submenu: SubmenuService = Depends()) -> SubmenuOut:
    '''
    Создание подменю. Функция принимает id меню, для которого
    нужно создать подменю, и экземпляр модели SubmenuIn.
    Возвращает экземпляр модели SubmenuOut.
    Если подменю с таким названием уже присутствует в базе -
    будет возбуждено исключение: ошибка 400 "submenu already exist"
    '''
    background_tasks.add_task(submenu.cache.create_invalidation,
                              menu_id=menu_id)
    return await submenu.create(menu_id=menu_id, submenu=submenu_data)


@router.patch('/{submenu_id}',
              response_model=SubmenuOut,
              status_code=status.HTTP_200_OK)
async def updating_submenu(background_tasks: BackgroundTasks,
                           menu_id: UUID,
                           submenu_id: UUID,
                           submenu_data: SubmenuIn,
                           submenu: SubmenuService = Depends()) -> SubmenuOut:
    '''
    Обновление подменю. Функция принимает id меню,
    в котором находится подменю для обновления,
    id подменю, которое нужно обновить и экземпляр модели SubmenuIn.
    Возвращает экземпляр модели SubmenuOut.
    Если подменю не найдено - будет возбуждено исключение: ошибка 404
    "submenu not found"
    '''
    background_tasks.add_task(submenu.cache.update_invalidation,
                              menu_id=menu_id)
    return await submenu.update(
        menu_id=menu_id, submenu_id=submenu_id, submenu=submenu_data)


@router.delete('/{submenu_id}',
               response_model=DeleteMSG,
               status_code=status.HTTP_200_OK)
async def deleting_submenu(background_tasks: BackgroundTasks,
                           menu_id: UUID,
                           submenu_id: UUID,
                           submenu: SubmenuService = Depends()) -> JSONResponse:
    '''
    Удаление подменю. Функция принимает id меню и id подменю,
    которое нужно удалить. Возвращает ответ в формате JSON
    с сообщением об успешном удалении.
    Если подменю не найдено - будет возбуждено исключение: ошибка 404
    "submenu not found"
    '''
    background_tasks.add_task(submenu.cache.delete_invalidation,
                              menu_id=menu_id, submenu_id=submenu_id)
    return await submenu.delete(submenu_id=submenu_id)
