import argparse
import requests

BASE_URL = "http://127.0.0.1:5000"


def view_inventory():
    response = requests.get(f"{BASE_URL}/inventory")

    if response.status_code == 200:
        items = response.json()

        if not items:
            print("Inventory is empty.")
            return

        print("\n===== INVENTORY =====")
        for item in items:
            print(f"""
ID: {item['id']}
Product: {item['product_name']}
Brand: {item['brand']}
Barcode: {item['barcode']}
Price: ${item['price']}
Stock: {item['stock']}
---------------------------
""")
    else:
        print("Error:", response.json())



def get_item(item_id):
    response = requests.get(f"{BASE_URL}/inventory/{item_id}")

    if response.status_code == 200:
        item = response.json()

        print("\n===== PRODUCT =====")
        for key, value in item.items():
            print(f"{key}: {value}")

    else:
        print(response.json())


def add_item(args):
    data = {
        "product_name": args.product_name,
        "brand": args.brand,
        "barcode": args.barcode,
        "price": args.price,
        "stock": args.stock
    }

    response = requests.post(
        f"{BASE_URL}/inventory",
        json=data
    )

    print(response.json())



def update_item(args):

    data = {}

    if args.product_name:
        data["product_name"] = args.product_name

    if args.brand:
        data["brand"] = args.brand

    if args.barcode:
        data["barcode"] = args.barcode

    if args.price is not None:
        data["price"] = args.price

    if args.stock is not None:
        data["stock"] = args.stock

    response = requests.patch(
        f"{BASE_URL}/inventory/{args.id}",
        json=data
    )

    print(response.json())


def delete_item(item_id):

    response = requests.delete(
        f"{BASE_URL}/inventory/{item_id}"
    )

    print(response.json())


def search_product(barcode):

    response = requests.get(
        f"{BASE_URL}/inventory/search/{barcode}"
    )

    if response.status_code == 200:
        product = response.json()

        print("\n===== PRODUCT FOUND =====")
        for key, value in product.items():
            print(f"{key}: {value}")

    else:
        print(response.json())


parser = argparse.ArgumentParser(
    description="Inventory Management CLI"
)

subparsers = parser.add_subparsers(dest="command")


subparsers.add_parser("list")


# Get one item
item_parser = subparsers.add_parser("get")
item_parser.add_argument("id", type=int)


# Add item
add_parser = subparsers.add_parser("add")

add_parser.add_argument("--product_name", required=True)
add_parser.add_argument("--brand", required=True)
add_parser.add_argument("--barcode", required=True)
add_parser.add_argument("--price", type=float, required=True)
add_parser.add_argument("--stock", type=int, required=True)


# Update item
update_parser = subparsers.add_parser("update")

update_parser.add_argument("id", type=int)

update_parser.add_argument("--product_name")
update_parser.add_argument("--brand")
update_parser.add_argument("--barcode")
update_parser.add_argument("--price", type=float)
update_parser.add_argument("--stock", type=int)


# Delete item
delete_parser = subparsers.add_parser("delete")
delete_parser.add_argument("id", type=int)


# Search OpenFoodFacts
search_parser = subparsers.add_parser("search")
search_parser.add_argument("barcode")


def main():
    args = parser.parse_args()

    if args.command == "list":
        view_inventory()

    elif args.command == "get":
        get_item(args.id)

    elif args.command == "add":
        add_item(args)

    elif args.command == "update":
        update_item(args)

    elif args.command == "delete":
        delete_item(args.id)

    elif args.command == "search":
        search_product(args.barcode)


if __name__ == "__main__":
    main()       