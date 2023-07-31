from fastapi.testclient import TestClient
from menu_app.main import app

client = TestClient(app)

prefix = '/api/v1/menus'

created_dish = {
    "title": "My dish 1",
    "description": "My dish description 1",
    "price": "12.50"
}

updated_dish = {
    "title": "My updated dish 1",
    "description": "My updated dish description 1",
    "price": "14.50"
}


def test_reading_dishes(get_submenuid_for_dish_test):
    global test_menu_id, test_submenu_id
    test_menu_id, test_submenu_id = get_submenuid_for_dish_test
    response = client.get(f'{prefix}/{test_menu_id}/submenus/'
                          f'{test_submenu_id}/dishes')
    assert response.status_code == 200
    assert response.json() == []


def test_create_dish():
    response = client.post(f'{prefix}/{test_menu_id}/submenus/'
                           f'{test_submenu_id}/dishes', json=created_dish)
    assert response.status_code == 201
    result = response.json()
    global test_dish_id
    test_dish_id = result["id"]
    assert isinstance(result["id"], str)
    assert result["title"] == created_dish["title"]
    assert result["description"] == created_dish["description"]
    assert result["price"] == created_dish["price"]


def test_reading_dish():
    response = client.get(f'{prefix}/{test_menu_id}/submenus/'
                          f'{test_submenu_id}/dishes/{test_dish_id}')
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result["id"], str)
    assert result["title"] == created_dish["title"]
    assert result["description"] == created_dish["description"]
    assert result["price"] == created_dish["price"]


def test_updating_dish():
    response = client.patch(f'{prefix}/{test_menu_id}/submenus/'
                            f'{test_submenu_id}/dishes/{test_dish_id}',
                            json=updated_dish)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result["id"], str)
    assert result["title"] == updated_dish["title"]
    assert result["description"] == updated_dish["description"]
    assert result["price"] == updated_dish["price"]


def test_deleting_dish():
    response = client.delete(f'{prefix}/{test_menu_id}/submenus/'
                             f'{test_submenu_id}/dishes/{test_dish_id}')
    assert response.status_code == 200
    result = response.json()
    assert result["status"] is True
    assert result["message"] == "The dish has been deleted"


def test_reading_missing_dish():
    response = client.get(f'{prefix}/{test_menu_id}/submenus/'
                          f'{test_submenu_id}/dishes/{test_dish_id}')
    assert response.status_code == 404
    result = response.json()
    assert result["detail"] == "dish not found"


def test_clean_base(cleanup_db):
    response = client.get(f"{prefix}/")
    assert response.status_code == 200
    assert response.json() == []
