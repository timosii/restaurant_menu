# mypy: disable-error-code="name-defined"
from uuid import UUID

from httpx import AsyncClient

prefix = '/api/v1/menus'


async def test_reading_dishes(ac: AsyncClient, get_submenuid: tuple[UUID, UUID]) -> None:
    global test_menu_id, test_submenu_id
    test_menu_id, test_submenu_id = get_submenuid
    response = await ac.get(f'{prefix}/{test_menu_id}/submenus/'
                            f'{test_submenu_id}/dishes/')
    assert response.status_code == 200
    assert response.json() == []


async def test_create_dish(ac: AsyncClient, get_dish_1: dict) -> None:
    response = await ac.post(f'{prefix}/{test_menu_id}/submenus/'
                             f'{test_submenu_id}/dishes/', json=get_dish_1)
    assert response.status_code == 201
    result = response.json()
    global test_dish_id
    test_dish_id = result['id']
    assert isinstance(result['id'], str)
    assert result['title'] == get_dish_1['title']
    assert result['description'] == get_dish_1['description']
    assert result['price'] == get_dish_1['price']


async def test_reading_dish(ac: AsyncClient, get_dish_1: dict) -> None:
    response = await ac.get(f'{prefix}/{test_menu_id}/submenus/'
                            f'{test_submenu_id}/dishes/{test_dish_id}')
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result['id'], str)
    assert result['title'] == get_dish_1['title']
    assert result['description'] == get_dish_1['description']
    assert result['price'] == get_dish_1['price']


async def test_updating_dish(ac: AsyncClient, get_updated_dish: dict) -> None:
    response = await ac.patch(f'{prefix}/{test_menu_id}/submenus/'
                              f'{test_submenu_id}/dishes/{test_dish_id}',
                              json=get_updated_dish)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result['id'], str)
    assert result['title'] == get_updated_dish['title']
    assert result['description'] == get_updated_dish['description']
    assert result['price'] == get_updated_dish['price']


async def test_deleting_dish(ac: AsyncClient) -> None:
    response = await ac.delete(f'{prefix}/{test_menu_id}/submenus/'
                               f'{test_submenu_id}/dishes/{test_dish_id}')
    assert response.status_code == 200
    result = response.json()
    assert result['status'] is True
    assert result['message'] == 'The dish has been deleted'


async def test_reading_missing_dish(ac: AsyncClient) -> None:
    response = await ac.get(f'{prefix}/{test_menu_id}/submenus/'
                            f'{test_submenu_id}/dishes/{test_dish_id}')
    assert response.status_code == 404
    result = response.json()
    assert result['detail'] == 'dish not found'
