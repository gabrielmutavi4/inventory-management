import requests

BASE_URL = "https://world.openfoodfacts.org/api/v0/product"

HEADERS = {
    "User-Agent": "InventoryManagementApp/1.0 (gabriel@example.com)"
}

def get_product_by_barcode(barcode):
    url = f"{BASE_URL}/{barcode}.json"

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
       print("Status Code:", response.status_code)
       print("Response:", response.text)
       return None

    data = response.json()

    if data.get("status") != 1:
        return None

    product = data["product"]

    return {
        "product_name": product.get("product_name", ""),
        "brand": product.get("brands", ""),
        "ingredients": product.get("ingredients_text", "")
    }