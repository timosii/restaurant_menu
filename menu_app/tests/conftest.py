# import pytest
# from fastapi.testclient import TestClient

# from menu_app import models
# from menu_app.database import engine
# from menu_app.main import app

# client = TestClient(app)


# menu = {
#     'title': 'My menu 1',
#     'description': 'My menu description 1'
# }

# menu_updated = {
#     'title': 'My updated menu 1',
#     'description': 'My updated menu description 1'
# }

# submenu = {
#     'title': 'My submenu 1',
#     'description': 'My submenu description 1'
# }

# submenu_updated = {
#     'title': 'My updated submenu 1',
#     'description': 'My updated submenu description 1'
# }

# dish_1 = {
#     'title': 'My dish 1',
#     'description': 'My dish description 1',
#     'price': '12.50'
# }


# dish_updated = {
#     'title': 'My updated dish 1',
#     'description': 'My updated dish description 1',
#     'price': '14.50'
# }


# dish_2 = {
#     'title': 'My dish 2',
#     'description': 'My dish description 2',
#     'price': '13.50'
# }


# @pytest.fixture
# def get_menu():
#     return menu


# @pytest.fixture
# def get_updated_menu():
#     return menu_updated


# @pytest.fixture
# def get_submenu():
#     return submenu


# @pytest.fixture
# def get_updated_submenu():
#     return submenu_updated


# @pytest.fixture
# def get_dish_1():
#     return dish_1


# @pytest.fixture
# def get_dish_2():
#     return dish_2


# @pytest.fixture
# def get_updated_dish():
#     return dish_updated


# @pytest.fixture
# def cleanup_db():
#     models.Base.metadata.drop_all(bind=engine)
#     models.Base.metadata.create_all(bind=engine)
#     return


# @pytest.fixture
# def get_menuid_for_submenu_test(get_submenu):
#     response = client.post('/api/v1/menus/',
#                            json=get_submenu)
#     result = response.json()
#     test_menu_id = result['id']
#     return test_menu_id


# @pytest.fixture
# def get_menuid_for_dish_test(get_menu):
#     response = client.post('/api/v1/menus/',
#                            json=get_menu)
#     result = response.json()
#     test_menu_id = result['id']
#     return test_menu_id


# @pytest.fixture
# def get_submenuid_for_dish_test(get_menuid_for_dish_test, get_submenu):
#     test_menu_id = get_menuid_for_dish_test
#     response = client.post(f'/api/v1/menus/{test_menu_id}/submenus',
#                            json=get_submenu)
#     result = response.json()
#     test_submenu_id = result['id']
#     return test_menu_id, test_submenu_id

import pytest
from fastapi.testclient import TestClient

from menu_app import models
from menu_app.database import engine
from menu_app.main import app

client = TestClient(app)

menu = {
    'title': 'My menu 1',
    'description': 'My menu description 1'
}

menu_updated = {
    'title': 'My updated menu 1',
    'description': 'My updated menu description 1'
}

submenu = {
    'title': 'My submenu 1',
    'description': 'My submenu description 1'
}

submenu_updated = {
    'title': 'My updated submenu 1',
    'description': 'My updated submenu description 1'
}

dish_1 = {
    'title': 'My dish 1',
    'description': 'My dish description 1',
    'price': '12.50'
}

dish_updated = {
    'title': 'My updated dish 1',
    'description': 'My updated dish description 1',
    'price': '14.50'
}

dish_2 = {
    'title': 'My dish 2',
    'description': 'My dish description 2',
    'price': '13.50'
}


@pytest.fixture
async def get_menu():
    return menu


@pytest.fixture
async def get_updated_menu():
    return menu_updated


@pytest.fixture
async def get_submenu():
    return submenu


@pytest.fixture
async def get_updated_submenu():
    return submenu_updated


@pytest.fixture
async def get_dish_1():
    return dish_1


@pytest.fixture
async def get_dish_2():
    return dish_2


@pytest.fixture
async def get_updated_dish():
    return dish_updated


@pytest.fixture
async def cleanup_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)


@pytest.fixture
async def get_menuid_for_submenu_test(get_submenu):
    response = client.post('/api/v1/menus/',
                           json=get_submenu)
    result = response.json()
    test_menu_id = result['id']
    return test_menu_id


@pytest.fixture
async def get_menuid_for_dish_test(get_menu):
    response = client.post('/api/v1/menus/',
                           json=get_menu)
    result = response.json()
    test_menu_id = result['id']
    return test_menu_id


@pytest.fixture
async def get_submenuid_for_dish_test(get_menuid_for_dish_test, get_submenu):
    test_menu_id = get_menuid_for_dish_test
    response = client.post(f'/api/v1/menus/{test_menu_id}/submenus',
                           json=get_submenu)
    result = response.json()
    test_submenu_id = result['id']
    return test_menu_id, test_submenu_id
