from fastapi.testclient import TestClient
from menu_app.main import app

client = TestClient(app)

prefix = '/api/v1/menus'

created_submenu = {
    "title": "My submenu 1",
    "description": "My submenu description 1"
}

updated_submenu = {
    "title": "My updated submenu 1",
    "description": "My updated submenu description 1"
}


def test_reading_submenus(get_menuid_for_submenu_test):
    global test_menu_id
    test_menu_id = get_menuid_for_submenu_test
    response = client.get(f"{prefix}/{test_menu_id}/submenus")
    assert response.status_code == 200
    assert response.json() == []


def test_create_submenu():
    response = client.post(f"{prefix}/{test_menu_id}\
                           /submenus", json=created_submenu)
    assert response.status_code == 201
    result = response.json()
    global test_submenu_id
    test_submenu_id = result["id"]
    assert isinstance(result["id"], str)
    assert result["title"] == created_submenu["title"]
    assert result["description"] == created_submenu["description"]
    assert isinstance(result["dishes_count"], int)


def test_reading_submenu():
    response = client.get(f"{prefix}/{test_menu_id}\
                          /submenus/{test_submenu_id}")
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result["id"], str)
    assert result["title"] == created_submenu["title"]
    assert result["description"] == created_submenu["description"]
    assert isinstance(result["dishes_count"], int)


def test_updating_submenu():
    response = client.patch(f"{prefix}/{test_menu_id}\
                            /submenus/{test_submenu_id}", json=updated_submenu)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result["id"], str)
    assert result["title"] == updated_submenu["title"]
    assert result["description"] == updated_submenu["description"]
    assert isinstance(result["dishes_count"], int)


def test_deleting_submenu():
    response = client.delete(f"{prefix}/{test_menu_id}\
                             /submenus/{test_submenu_id}")
    assert response.status_code == 200
    result = response.json()
    assert result["status"] is True
    assert result["message"] == "The submenu has been deleted"


def test_reading_missing_submenu():
    response = client.get(f"{prefix}/{test_menu_id}\
                          /submenus/{test_submenu_id}")
    assert response.status_code == 404
    result = response.json()
    assert result["detail"] == "submenu not found"


def test_clean_base(cleanup_db):
    response = client.get(f"{prefix}/")
    assert response.status_code == 200
    assert response.json() == []
