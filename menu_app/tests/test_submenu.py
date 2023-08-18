# mypy: disable-error-code="name-defined"
from uuid import UUID

from httpx import AsyncClient

prefix = '/api/v1/menus'


async def test_reading_submenus(ac: AsyncClient, get_menuid_for_submenu_test: UUID) -> None:
    global test_menu_id
    test_menu_id = get_menuid_for_submenu_test
    response = await ac.get(f'{prefix}/{test_menu_id}/submenus/')
    assert response.status_code == 200
    assert response.json() == []


async def test_create_submenu(ac: AsyncClient, get_submenu: dict) -> None:
    response = await ac.post(f'{prefix}/{test_menu_id}/submenus/',
                             json=get_submenu)
    assert response.status_code == 201
    result = response.json()
    global test_submenu_id
    test_submenu_id = result['id']
    assert isinstance(result['id'], str)
    assert result['title'] == get_submenu['title']
    assert result['description'] == get_submenu['description']
    assert isinstance(result['dishes_count'], int)


async def test_reading_submenu(ac: AsyncClient, get_submenu: dict) -> None:
    response = await ac.get(f'{prefix}/{test_menu_id}/submenus/'
                            f'{test_submenu_id}')
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result['id'], str)
    assert result['title'] == get_submenu['title']
    assert result['description'] == get_submenu['description']
    assert isinstance(result['dishes_count'], int)


async def test_updating_submenu(ac: AsyncClient, get_updated_submenu: dict) -> None:
    response = await ac.patch(f'{prefix}/{test_menu_id}/submenus/'
                              f'{test_submenu_id}',
                              json=get_updated_submenu)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result['id'], str)
    assert result['title'] == get_updated_submenu['title']
    assert result['description'] == get_updated_submenu['description']
    assert isinstance(result['dishes_count'], int)


async def test_deleting_submenu(ac: AsyncClient) -> None:
    response = await ac.delete(f'{prefix}/{test_menu_id}/submenus/'
                               f'{test_submenu_id}')
    assert response.status_code == 200
    result = response.json()
    assert result['status'] is True
    assert result['message'] == 'The submenu has been deleted'


async def test_reading_missing_submenu(ac: AsyncClient) -> None:
    response = await ac.get(f'{prefix}/{test_menu_id}/submenus/'
                            f'{test_submenu_id}')
    assert response.status_code == 404
    result = response.json()
    assert result['detail'] == 'submenu not found'
