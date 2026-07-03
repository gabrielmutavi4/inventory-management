import os
import sys
import pytest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, inventory


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "message" in response.get_json()


def test_get_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_single_item(client):
    response = client.get("/inventory/1")

    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_item_not_found(client):
    response = client.get("/inventory/999")

    assert response.status_code == 404


def test_add_item(client):

    new_item = {
        "product_name": "Test Product",
        "brand": "Test Brand",
        "barcode": "123456789",
        "price": 20.50,
        "stock": 15
    }

    response = client.post("/inventory", json=new_item)

    assert response.status_code == 201

    data = response.get_json()

    assert data["product_name"] == "Test Product"
    assert data["brand"] == "Test Brand"


def test_patch_item(client):

    response = client.patch(
        "/inventory/1",
        json={
            "price": 8.99,
            "stock": 30
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["price"] == 8.99
    assert data["stock"] == 30


def test_delete_item(client):

    client.post(
        "/inventory",
        json={
            "product_name": "Delete Me",
            "brand": "Test",
            "barcode": "999999999",
            "price": 5,
            "stock": 5
        }
    )

    item_id = inventory[-1]["id"]

    response = client.delete(f"/inventory/{item_id}")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Item deleted successfully"


def test_delete_missing_item(client):

    response = client.delete("/inventory/999")

    assert response.status_code == 404


def test_search_product(client):
    response = client.get("/inventory/search/737628064502")

    assert response.status_code in [200, 404]