import os
import sys
from unittest.mock import patch, Mock


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openfoodfacts import get_product_by_barcode


@patch("openfoodfacts.requests.get")
def test_get_product_success(mock_get):

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Filtered water, almonds"
        }
    }

    mock_get.return_value = mock_response

    product = get_product_by_barcode("737628064502")

    assert product["product_name"] == "Organic Almond Milk"
    assert product["brand"] == "Silk"
    assert product["ingredients"] == "Filtered water, almonds"


@patch("openfoodfacts.requests.get")
def test_product_not_found(mock_get):

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": 0}

    mock_get.return_value = mock_response

    assert get_product_by_barcode("000000") is None


@patch("openfoodfacts.requests.get")
def test_api_failure(mock_get):

    mock_response = Mock()
    mock_response.status_code = 500

    mock_get.return_value = mock_response

    assert get_product_by_barcode("123456") is None