from fastapi.testclient import TestClient

from menu_app.main import app

client = TestClient(app)

prefix = '/api/v1/menus'


def test_reading_menus(cleanup_db):
    response = client.get(f'{prefix}/')
    assert response.status_code == 200
    assert response.json() == []


def test_create_menu(get_menu):
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


def test_reading_menu(get_menu):
    response = client.get(f'{prefix}/{test_menu_id}')
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result['id'], str)
    assert result['title'] == get_menu['title']
    assert result['description'] == get_menu['description']
    assert isinstance(result['submenus_count'], int)
    assert isinstance(result['dishes_count'], int)


def test_updating_menu(get_updated_menu):
    response = client.patch(f'{prefix}/{test_menu_id}', json=get_updated_menu)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result['id'], str)
    assert result['title'] == get_updated_menu['title']
    assert result['description'] == get_updated_menu['description']
    assert isinstance(result['submenus_count'], int)
    assert isinstance(result['dishes_count'], int)


def test_deleting_menu():
    response = client.delete(f'{prefix}/{test_menu_id}')
    assert response.status_code == 200
    result = response.json()
    assert result['status'] is True
    assert result['message'] == 'The menu has been deleted'


def test_reading_missing_menu():
    response = client.get(f'{prefix}/{test_menu_id}')
    assert response.status_code == 404
    result = response.json()
    assert result['detail'] == 'menu not found'


def test_clean_base(cleanup_db):
    response = client.get(f'{prefix}/')
    assert response.status_code == 200
    assert response.json() == []
