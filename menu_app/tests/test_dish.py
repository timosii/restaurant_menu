# from fastapi.testclient import TestClient

# from menu_app.main import app

# client = TestClient(app)

# prefix = '/api/v1/menus'


# def test_reading_dishes(get_submenuid_for_dish_test):
#     global test_menu_id, test_submenu_id
#     test_menu_id, test_submenu_id = get_submenuid_for_dish_test
#     response = client.get(f'{prefix}/{test_menu_id}/submenus/'
#                           f'{test_submenu_id}/dishes')
#     assert response.status_code == 200
#     assert response.json() == []


# def test_create_dish(get_dish_1):
#     response = client.post(f'{prefix}/{test_menu_id}/submenus/'
#                            f'{test_submenu_id}/dishes', json=get_dish_1)
#     assert response.status_code == 201
#     result = response.json()
#     global test_dish_id
#     test_dish_id = result['id']
#     assert isinstance(result['id'], str)
#     assert result['title'] == get_dish_1['title']
#     assert result['description'] == get_dish_1['description']
#     assert result['price'] == get_dish_1['price']


# def test_reading_dish(get_dish_1):
#     response = client.get(f'{prefix}/{test_menu_id}/submenus/'
#                           f'{test_submenu_id}/dishes/{test_dish_id}')
#     assert response.status_code == 200
#     result = response.json()
#     assert isinstance(result['id'], str)
#     assert result['title'] == get_dish_1['title']
#     assert result['description'] == get_dish_1['description']
#     assert result['price'] == get_dish_1['price']


# def test_updating_dish(get_updated_dish):
#     response = client.patch(f'{prefix}/{test_menu_id}/submenus/'
#                             f'{test_submenu_id}/dishes/{test_dish_id}',
#                             json=get_updated_dish)
#     assert response.status_code == 200
#     result = response.json()
#     assert isinstance(result['id'], str)
#     assert result['title'] == get_updated_dish['title']
#     assert result['description'] == get_updated_dish['description']
#     assert result['price'] == get_updated_dish['price']


# def test_deleting_dish():
#     response = client.delete(f'{prefix}/{test_menu_id}/submenus/'
#                              f'{test_submenu_id}/dishes/{test_dish_id}')
#     assert response.status_code == 200
#     result = response.json()
#     assert result['status'] is True
#     assert result['message'] == 'The dish has been deleted'


# def test_reading_missing_dish():
#     response = client.get(f'{prefix}/{test_menu_id}/submenus/'
#                           f'{test_submenu_id}/dishes/{test_dish_id}')
#     assert response.status_code == 404
#     result = response.json()
#     assert result['detail'] == 'dish not found'


# def test_clean_base(cleanup_db):
#     response = client.get(f'{prefix}/')
#     assert response.status_code == 200
#     assert response.json() == []

from fastapi.testclient import TestClient

from menu_app.main import app

# from menu_app.database import get_db

client = TestClient(app)

prefix = '/api/v1/menus'


async def test_reading_dishes(get_submenuid_for_dish_test):
    global test_menu_id, test_submenu_id
    test_menu_id, test_submenu_id = get_submenuid_for_dish_test
    response = client.get(f'{prefix}/{test_menu_id}/submenus/'
                          f'{test_submenu_id}/dishes')
    assert response.status_code == 200
    assert response.json() == []


async def test_create_dish(get_dish_1):
    response = client.post(f'{prefix}/{test_menu_id}/submenus/'
                           f'{test_submenu_id}/dishes', json=get_dish_1)
    assert response.status_code == 201
    result = response.json()
    global test_dish_id
    test_dish_id = result['id']
    assert isinstance(result['id'], str)
    assert result['title'] == get_dish_1['title']
    assert result['description'] == get_dish_1['description']
    assert result['price'] == get_dish_1['price']


async def test_reading_dish(get_dish_1):
    response = client.get(f'{prefix}/{test_menu_id}/submenus/'
                          f'{test_submenu_id}/dishes/{test_dish_id}')
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result['id'], str)
    assert result['title'] == get_dish_1['title']
    assert result['description'] == get_dish_1['description']
    assert result['price'] == get_dish_1['price']


async def test_updating_dish(get_updated_dish):
    response = client.patch(f'{prefix}/{test_menu_id}/submenus/'
                            f'{test_submenu_id}/dishes/{test_dish_id}',
                            json=get_updated_dish)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result['id'], str)
    assert result['title'] == get_updated_dish['title']
    assert result['description'] == get_updated_dish['description']
    assert result['price'] == get_updated_dish['price']


async def test_deleting_dish():
    response = client.delete(f'{prefix}/{test_menu_id}/submenus/'
                             f'{test_submenu_id}/dishes/{test_dish_id}')
    assert response.status_code == 200
    result = response.json()
    assert result['status'] is True
    assert result['message'] == 'The dish has been deleted'


async def test_reading_missing_dish():
    response = client.get(f'{prefix}/{test_menu_id}/submenus/'
                          f'{test_submenu_id}/dishes/{test_dish_id}')
    assert response.status_code == 404
    result = response.json()
    assert result['detail'] == 'dish not found'


async def test_clean_base(cleanup_db):
    response = client.get(f'{prefix}/')
    assert response.status_code == 200
    assert response.json() == []
