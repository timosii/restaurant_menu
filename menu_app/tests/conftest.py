import pytest
from fastapi.testclient import TestClient

from menu_app import models
from menu_app.database import engine
from menu_app.main import app

client = TestClient(app)

created_menu_for_submenu_test = created_submenu_for_dish_test = {
    'title': 'My submenu 1',
    'description': 'My submenu description 1'
}

created_menu_for_dish_test = {
    'title': 'My menu 1',
    'description': 'My menu description 1'
}


@pytest.fixture
def cleanup_db():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    return


@pytest.fixture
def get_menuid_for_submenu_test():
    response = client.post('/api/v1/menus/',
                           json=created_menu_for_submenu_test)
    result = response.json()
    test_menu_id = result['id']
    return test_menu_id


@pytest.fixture
def get_menuid_for_dish_test():
    response = client.post('/api/v1/menus/',
                           json=created_menu_for_dish_test)
    result = response.json()
    test_menu_id = result['id']
    return test_menu_id


@pytest.fixture
def get_submenuid_for_dish_test(get_menuid_for_dish_test):
    test_menu_id = get_menuid_for_dish_test
    response = client.post(f'/api/v1/menus/{test_menu_id}/submenus',
                           json=created_submenu_for_dish_test)
    result = response.json()
    test_submenu_id = result['id']
    return test_menu_id, test_submenu_id
