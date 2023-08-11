# from fastapi.testclient import TestClient

# from menu_app.main import app

# client = TestClient(app)

# prefix = '/api/v1/menus'


# def test_create_menu(cleanup_db, get_menu):
#     response = client.post(f'{prefix}/', json=get_menu)
#     assert response.status_code == 201
#     result = response.json()
#     global test_menu_id
#     test_menu_id = result['id']
#     assert isinstance(result['id'], str)
#     assert result['title'] == get_menu['title']
#     assert result['description'] == get_menu['description']
#     assert isinstance(result['submenus_count'], int)
#     assert isinstance(result['dishes_count'], int)
#     assert result['submenus_count'] == 0
#     assert result['dishes_count'] == 0


# def test_create_submenu(get_submenu):
#     response = client.post(f'{prefix}/{test_menu_id}/submenus',
#                            json=get_submenu)
#     assert response.status_code == 201
#     result = response.json()
#     global test_submenu_id
#     test_submenu_id = result['id']
#     assert isinstance(result['id'], str)
#     assert result['title'] == get_submenu['title']
#     assert result['description'] == get_submenu['description']
#     assert isinstance(result['dishes_count'], int)
#     assert result['dishes_count'] == 0


# def test_create_dish_1(get_dish_1):
#     response = client.post(f'{prefix}/{test_menu_id}/submenus/'
#                            f'{test_submenu_id}/dishes',
#                            json=get_dish_1)
#     assert response.status_code == 201
#     result = response.json()
#     global test_dish_id_1
#     test_dish_id_1 = result['id']
#     assert isinstance(result['id'], str)
#     assert result['title'] == get_dish_1['title']
#     assert result['description'] == get_dish_1['description']
#     assert result['price'] == get_dish_1['price']


# def test_create_dish_2(get_dish_2):
#     response = client.post(f'{prefix}/{test_menu_id}/submenus/'
#                            f'{test_submenu_id}/dishes',
#                            json=get_dish_2)
#     assert response.status_code == 201
#     result = response.json()
#     global test_dish_id_2
#     test_dish_id_2 = result['id']
#     assert isinstance(result['id'], str)
#     assert result['title'] == get_dish_2['title']
#     assert result['description'] == get_dish_2['description']
#     assert result['price'] == get_dish_2['price']


# def test_reading_menu(get_menu):
#     response = client.get(f'{prefix}/{test_menu_id}')
#     assert response.status_code == 200
#     result = response.json()
#     assert isinstance(result['id'], str)
#     assert result['title'] == get_menu['title']
#     assert result['description'] == get_menu['description']
#     assert isinstance(result['submenus_count'], int)
#     assert isinstance(result['dishes_count'], int)
#     assert result['submenus_count'] == 1
#     assert result['dishes_count'] == 2


# def test_reading_submenu(get_submenu):
#     response = client.get(f'{prefix}/{test_menu_id}/submenus/'
#                           f'{test_submenu_id}')
#     assert response.status_code == 200
#     result = response.json()
#     assert isinstance(result['id'], str)
#     assert result['title'] == get_submenu['title']
#     assert result['description'] == get_submenu['description']
#     assert isinstance(result['dishes_count'], int)
#     assert result['dishes_count'] == 2


# def test_deleting_submenu():
#     response = client.delete(f'{prefix}/{test_menu_id}/submenus/'
#                              f'{test_submenu_id}')
#     assert response.status_code == 200
#     result = response.json()
#     assert result['status'] is True
#     assert result['message'] == 'The submenu has been deleted'


# def test_reading_submenus():
#     response = client.get(f'{prefix}/{test_menu_id}/submenus')
#     assert response.status_code == 200
#     assert response.json() == []


# def test_reading_dishes():
#     response = client.get(f'{prefix}/{test_menu_id}/submenus/'
#                           f'{test_submenu_id}/dishes')
#     assert response.status_code == 200
#     assert response.json() == []


# def test_reading_menu_after_delete(get_menu):
#     response = client.get(f'{prefix}/{test_menu_id}')
#     assert response.status_code == 200
#     result = response.json()
#     assert isinstance(result['id'], str)
#     assert result['title'] == get_menu['title']
#     assert result['description'] == get_menu['description']
#     assert isinstance(result['submenus_count'], int)
#     assert isinstance(result['dishes_count'], int)
#     assert result['submenus_count'] == 0
#     assert result['dishes_count'] == 0


# def test_deleting_menu():
#     response = client.delete(f'{prefix}/{test_menu_id}')
#     assert response.status_code == 200
#     result = response.json()
#     assert result['status'] is True
#     assert result['message'] == 'The menu has been deleted'


# def test_reading_menus():
#     response = client.get(f'{prefix}/')
#     assert response.status_code == 200
#     assert response.json() == []


# def test_clean_base(cleanup_db):
#     response = client.get(f'{prefix}/')
#     assert response.status_code == 200
#     assert response.json() == []

import pytest
from fastapi.testclient import TestClient

from menu_app.main import app

client = TestClient(app)

prefix = '/api/v1/menus'


@pytest.mark.asyncio
async def test_create_menu(cleanup_db, get_menu):
    response = client.post(f'{prefix}/', json=get_menu)
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


@pytest.mark.asyncio
async def test_create_submenu(get_submenu):
    response = client.post(f'{prefix}/{test_menu_id}/submenus',
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


@pytest.mark.asyncio
async def test_create_dish_1(get_dish_1):
    response = client.post(f'{prefix}/{test_menu_id}/submenus/'
                           f'{test_submenu_id}/dishes',
                           json=get_dish_1)
    assert response.status_code == 201
    result = response.json()
    global test_dish_id_1
    test_dish_id_1 = result['id']
    assert isinstance(result['id'], str)
    assert result['title'] == get_dish_1['title']
    assert result['description'] == get_dish_1['description']
    assert result['price'] == get_dish_1['price']


@pytest.mark.asyncio
async def test_create_dish_2(get_dish_2):
    response = client.post(f'{prefix}/{test_menu_id}/submenus/'
                           f'{test_submenu_id}/dishes',
                           json=get_dish_2)
    assert response.status_code == 201
    result = response.json()
    global test_dish_id_2
    test_dish_id_2 = result['id']
    assert isinstance(result['id'], str)
    assert result['title'] == get_dish_2['title']
    assert result['description'] == get_dish_2['description']
    assert result['price'] == get_dish_2['price']


@pytest.mark.asyncio
async def test_reading_menu(get_menu):
    response = client.get(f'{prefix}/{test_menu_id}')
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result['id'], str)
    assert result['title'] == get_menu['title']
    assert result['description'] == get_menu['description']
    assert isinstance(result['submenus_count'], int)
    assert isinstance(result['dishes_count'], int)
    assert result['submenus_count'] == 1
    assert result['dishes_count'] == 2


@pytest.mark.asyncio
async def test_reading_submenu(get_submenu):
    response = client.get(f'{prefix}/{test_menu_id}/submenus/'
                          f'{test_submenu_id}')
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result['id'], str)
    assert result['title'] == get_submenu['title']
    assert result['description'] == get_submenu['description']
    assert isinstance(result['dishes_count'], int)
    assert result['dishes_count'] == 2


@pytest.mark.asyncio
async def test_deleting_submenu():
    response = client.delete(f'{prefix}/{test_menu_id}/submenus/'
                             f'{test_submenu_id}')
    assert response.status_code == 200
    result = response.json()
    assert result['status'] is True
    assert result['message'] == 'The submenu has been deleted'


@pytest.mark.asyncio
async def test_reading_submenus():
    response = client.get(f'{prefix}/{test_menu_id}/submenus')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_reading_dishes():
    response = client.get(f'{prefix}/{test_menu_id}/submenus/'
                          f'{test_submenu_id}/dishes')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_reading_menu_after_delete(get_menu):
    response = client.get(f'{prefix}/{test_menu_id}')
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result['id'], str)
    assert result['title'] == get_menu['title']
    assert result['description'] == get_menu['description']
    assert isinstance(result['submenus_count'], int)
    assert isinstance(result['dishes_count'], int)
    assert result['submenus_count'] == 0
    assert result['dishes_count'] == 0


@pytest.mark.asyncio
async def test_deleting_menu():
    response = client.delete(f'{prefix}/{test_menu_id}')
    assert response.status_code == 200
    result = response.json()
    assert result['status'] is True
    assert result['message'] == 'The menu has been deleted'


@pytest.mark.asyncio
async def test_reading_menus():
    response = client.get(f'{prefix}/')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_clean_base(cleanup_db):
    response = client.get(f'{prefix}/')
    assert response.status_code == 200
    assert response.json() == []
