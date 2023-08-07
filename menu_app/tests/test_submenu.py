from fastapi.testclient import TestClient

from menu_app.main import app

client = TestClient(app)

prefix = '/api/v1/menus'


def test_reading_submenus(get_menuid_for_submenu_test):
    global test_menu_id
    test_menu_id = get_menuid_for_submenu_test
    response = client.get(f'{prefix}/{test_menu_id}/submenus')
    assert response.status_code == 200
    assert response.json() == []


def test_create_submenu(get_submenu):
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


def test_reading_submenu(get_submenu):
    response = client.get(f'{prefix}/{test_menu_id}/submenus/'
                          f'{test_submenu_id}')
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result['id'], str)
    assert result['title'] == get_submenu['title']
    assert result['description'] == get_submenu['description']
    assert isinstance(result['dishes_count'], int)


def test_updating_submenu(get_updated_submenu):
    response = client.patch(f'{prefix}/{test_menu_id}/submenus/'
                            f'{test_submenu_id}',
                            json=get_updated_submenu)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result['id'], str)
    assert result['title'] == get_updated_submenu['title']
    assert result['description'] == get_updated_submenu['description']
    assert isinstance(result['dishes_count'], int)


def test_deleting_submenu():
    response = client.delete(f'{prefix}/{test_menu_id}/submenus/'
                             f'{test_submenu_id}')
    assert response.status_code == 200
    result = response.json()
    assert result['status'] is True
    assert result['message'] == 'The submenu has been deleted'


def test_reading_missing_submenu():
    response = client.get(f'{prefix}/{test_menu_id}/submenus/'
                          f'{test_submenu_id}')
    assert response.status_code == 404
    result = response.json()
    assert result['detail'] == 'submenu not found'


def test_clean_base(cleanup_db):
    response = client.get(f'{prefix}/')
    assert response.status_code == 200
    assert response.json() == []
