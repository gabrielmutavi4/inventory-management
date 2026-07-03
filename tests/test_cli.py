from unittest.mock import patch, Mock
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cli


@patch("cli.requests.get")
def test_list_inventory(mock_get):

    mock_response = Mock()

    mock_response.json.return_value = [
        {
            "id": 1,
            "product_name": "Milk"
        }
    ]

    mock_response.status_code = 200

    mock_get.return_value = mock_response

    response = cli.requests.get("http://127.0.0.1:5000/inventory")

    assert response.status_code == 200
    assert response.json()[0]["product_name"] == "Milk"


@patch("cli.requests.post")
def test_add_product(mock_post):

    mock_response = Mock()

    mock_response.status_code = 201

    mock_response.json.return_value = {
        "id": 3,
        "product_name": "Coffee"
    }

    mock_post.return_value = mock_response

    response = cli.requests.post(
        "http://127.0.0.1:5000/inventory"
    )

    assert response.status_code == 201


@patch("cli.requests.patch")
def test_update_product(mock_patch):

    mock_response = Mock()

    mock_response.status_code = 200

    mock_response.json.return_value = {
        "price": 20
    }

    mock_patch.return_value = mock_response

    response = cli.requests.patch(
        "http://127.0.0.1:5000/inventory/1"
    )

    assert response.status_code == 200


@patch("cli.requests.delete")
def test_delete_product(mock_delete):

    mock_response = Mock()

    mock_response.status_code = 200

    mock_response.json.return_value = {
        "message": "Item deleted successfully"
    }

    mock_delete.return_value = mock_response

    response = cli.requests.delete(
        "http://127.0.0.1:5000/inventory/1"
    )

    assert response.status_code == 200