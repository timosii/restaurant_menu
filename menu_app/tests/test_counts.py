# mypy: disable-error-code="name-defined"
from httpx import AsyncClient

prefix = '/api/v1/menus'


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
    assert result['submenus_count'] == 0
    assert result['dishes_count'] == 0


async def test_create_submenu(ac: AsyncClient, get_submenu):
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
    assert result['dishes_count'] == 0


async def test_create_dish_1(ac: AsyncClient, get_dish_1):
    response = await ac.post(f'{prefix}/{test_menu_id}/submenus/'
                             f'{test_submenu_id}/dishes/',
                             json=get_dish_1)
    assert response.status_code == 201
    result = response.json()
    global test_dish_id_1
    test_dish_id_1 = result['id']
    assert isinstance(result['id'], str)
    assert result['title'] == get_dish_1['title']
    assert result['description'] == get_dish_1['description']
    assert result['price'] == get_dish_1['price']


async def test_create_dish_2(ac: AsyncClient, get_dish_2):
    response = await ac.post(f'{prefix}/{test_menu_id}/submenus/'
                             f'{test_submenu_id}/dishes/',
                             json=get_dish_2)
    assert response.status_code == 201
    result = response.json()
    global test_dish_id_2
    test_dish_id_2 = result['id']
    assert isinstance(result['id'], str)
    assert result['title'] == get_dish_2['title']
    assert result['description'] == get_dish_2['description']
    assert result['price'] == get_dish_2['price']


async def test_reading_menu(ac: AsyncClient, get_menu):
    response = await ac.get(f'{prefix}/{test_menu_id}')
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result['id'], str)
    assert result['title'] == get_menu['title']
    assert result['description'] == get_menu['description']
    assert isinstance(result['submenus_count'], int)
    assert isinstance(result['dishes_count'], int)
    assert result['submenus_count'] == 1
    assert result['dishes_count'] == 2


async def test_reading_submenu(ac: AsyncClient, get_submenu):
    response = await ac.get(f'{prefix}/{test_menu_id}/submenus/'
                            f'{test_submenu_id}')
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result['id'], str)
    assert result['title'] == get_submenu['title']
    assert result['description'] == get_submenu['description']
    assert isinstance(result['dishes_count'], int)
    assert result['dishes_count'] == 2


async def test_deleting_submenu(ac: AsyncClient):
    response = await ac.delete(f'{prefix}/{test_menu_id}/submenus/'
                               f'{test_submenu_id}')
    assert response.status_code == 200
    result = response.json()
    assert result['status'] is True
    assert result['message'] == 'The submenu has been deleted'


async def test_reading_submenus(ac: AsyncClient):
    response = await ac.get(f'{prefix}/{test_menu_id}/submenus/')
    assert response.status_code == 200
    assert response.json() == []


async def test_reading_dishes(ac: AsyncClient):
    response = await ac.get(f'{prefix}/{test_menu_id}/submenus/'
                            f'{test_submenu_id}/dishes/')
    assert response.status_code == 200
    assert response.json() == []


async def test_reading_menu_after_delete(ac: AsyncClient, get_menu):
    response = await ac.get(f'{prefix}/{test_menu_id}')
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result['id'], str)
    assert result['title'] == get_menu['title']
    assert result['description'] == get_menu['description']
    assert isinstance(result['submenus_count'], int)
    assert isinstance(result['dishes_count'], int)
    assert result['submenus_count'] == 0
    assert result['dishes_count'] == 0


async def test_deleting_menu(ac: AsyncClient):
    response = await ac.delete(f'{prefix}/{test_menu_id}')
    assert response.status_code == 200
    result = response.json()
    assert result['status'] is True
    assert result['message'] == 'The menu has been deleted'


async def test_reading_menus(ac: AsyncClient):
    response = await ac.get(f'{prefix}/')
    assert response.status_code == 200
    assert response.json() == []
