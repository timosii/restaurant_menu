import pytest

from fastapi.testclient import TestClient
from menu_app.main import app


prefix = '/api/v1/menus'

client = TestClient(app)

created_menu = {
    "title": "My menu 1",
    "description": "My menu description 1"
}

updated_menu = {
    "title": "My updated menu 1",
    "description": "My updated menu description 1"
}


def test_reading_menus(cleanup_db):
    response = client.get(f"{prefix}/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_menu():
    response = client.post(f"{prefix}/", json=created_menu)
    assert response.status_code == 201
    result = response.json()
    global test_menu_id
    test_menu_id = result["id"]
    assert isinstance(result["id"], str)
    assert isinstance(result["submenus_count"], int)
    assert isinstance(result["dishes_count"], int)
    assert result["title"] == created_menu["title"]
    assert result["description"] == created_menu["description"]


def test_reading_menu():
    response = client.get(f"{prefix}/{test_menu_id}")
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result["id"], str)
    assert isinstance(result["submenus_count"], int)
    assert isinstance(result["dishes_count"], int)
    assert result["title"] == created_menu["title"]
    assert result["description"] == created_menu["description"]


def test_updating_menu():
    response = client.patch(f"{prefix}/{test_menu_id}", json=updated_menu)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result["id"], str)
    assert isinstance(result["submenus_count"], int)
    assert isinstance(result["dishes_count"], int)
    assert result["title"] == updated_menu["title"]
    assert result["description"] == updated_menu["description"]


def test_deleting_menu():
    response = client.delete(f"{prefix}/{test_menu_id}")
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == True
    assert result["message"] == "The menu has been deleted"






