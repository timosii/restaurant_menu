# mypy: disable-error-code="name-defined"
from httpx import AsyncClient

prefix = '/api/v1/menus'


async def test_reading_menus(ac: AsyncClient):
    response = await ac.get(f'{prefix}/')
    assert response.status_code == 200
    assert response.json() == []


async def test_create_menu(ac: AsyncClient, get_menu):
    response = await ac.post(f'{prefix}/', json=get_menu)
    assert response.status_code == 201
    result = response.json()
    global test_menu_id
    test_menu_id = result['id']
    assert isinstance(result['id'], str)
    assert result['title'] == get_menu['title']
    assert result['description'] == get_menu['description']
    assert isinstance(result['submenus_count'], int)
    assert isinstance(result['dishes_count'], int)


async def test_reading_menu(ac: AsyncClient, get_menu):
    response = await ac.get(f'{prefix}/{test_menu_id}')
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result['id'], str)
    assert result['title'] == get_menu['title']
    assert result['description'] == get_menu['description']
    assert isinstance(result['submenus_count'], int)
    assert isinstance(result['dishes_count'], int)


async def test_updating_menu(ac: AsyncClient, get_updated_menu):
    response = await ac.patch(f'{prefix}/{test_menu_id}', json=get_updated_menu)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result['id'], str)
    assert result['title'] == get_updated_menu['title']
    assert result['description'] == get_updated_menu['description']
    assert isinstance(result['submenus_count'], int)
    assert isinstance(result['dishes_count'], int)


async def test_deleting_menu(ac: AsyncClient):
    response = await ac.delete(f'{prefix}/{test_menu_id}')
    assert response.status_code == 200
    result = response.json()
    assert result['status'] is True
    assert result['message'] == 'The menu has been deleted'


async def test_reading_missing_menu(ac: AsyncClient):
    response = await ac.get(f'{prefix}/{test_menu_id}')
    assert response.status_code == 404
    result = response.json()
    assert result['detail'] == 'menu not found'
