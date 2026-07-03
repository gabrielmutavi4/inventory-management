from flask import Flask, jsonify, request
from openfoodfacts import get_product_by_barcode

app = Flask(__name__)

inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brand": "Silk",
        "barcode": "737628064502",
        "price": 5.99,
        "stock": 20
    },
    {
        "id": 2,
        "product_name": "Peanut Butter",
        "brand": "Skippy",
        "barcode": "3760043630885",
        "price": 4.99,
        "stock": 10
    }
]



# GET ALL PRODUCTS

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200



# GET ONE PRODUCT

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):

    item = next((item for item in inventory if item["id"] == item_id), None)

    if item:
        return jsonify(item), 200

    return jsonify({"error": "Item not found"}), 404



# ADD NEW PRODUCT

@app.route("/inventory", methods=["POST"])
def add_item():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    required_fields = [
        "product_name",
        "brand",
        "barcode",
        "price",
        "stock"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    new_item = {
        "id": inventory[-1]["id"] + 1 if inventory else 1,
        "product_name": data["product_name"],
        "brand": data["brand"],
        "barcode": data["barcode"],
        "price": data["price"],
        "stock": data["stock"]
    }

    inventory.append(new_item)

    return jsonify(new_item), 201



# UPDATE PRODUCT

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):

    item = next((item for item in inventory if item["id"] == item_id), None)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    for key in ["product_name", "brand", "barcode", "price", "stock"]:
        if key in data:
            item[key] = data[key]

    return jsonify(item), 200



# DELETE PRODUCT

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):

    item = next((item for item in inventory if item["id"] == item_id), None)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    inventory.remove(item)

    return jsonify({"message": "Item deleted successfully"}), 200



# SEARCH OPENFOODFACTS

@app.route("/inventory/search/<barcode>", methods=["GET"])
def search_product(barcode):

    product = get_product_by_barcode(barcode)

    if product:
        return jsonify(product), 200

    return jsonify({"error": "Product not found"}), 404


# HOME ROUTE

@app.route("/")
def home():

    return jsonify({
        "message": "Inventory Management API",
        "routes": [
            "GET /inventory",
            "GET /inventory/<id>",
            "POST /inventory",
            "PATCH /inventory/<id>",
            "DELETE /inventory/<id>",
            "GET /inventory/search/<barcode>"
        ]
    })



if __name__ == "__main__":
    app.run(debug=True)