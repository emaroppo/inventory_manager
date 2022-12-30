import csv


class Store:
    def __init__(self, street_n, street_name, city, ZIP):
        self.street_n = street_n.upper()
        self.street_name = street_name.upper()
        self.city = city.upper()
        self.ZIP = ZIP


class Product:
    def __init__(self, product_name, category_name):
        self.product_name = product_name.lower()
        self.category_name = category_name


class Order:
    def __init__(self, items):
        self.items = items


def stores_from_csv(csv_path):
    stores = []
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            stores.append(Store(row[0], row[1], row[2], row[3]))
    return stores


def products_from_csv(csv_path):
    products = []
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            products.append(Product(row[0], row[1]))
    return products


def order_from_csv(csv_path):

    with open(csv_path, "r") as f:
        order_lines = f.read().splitlines()

    order_items = [
        (i.split(",")[0], i.split(",")[1], i.split(",")[2]) for i in order_lines
    ]
    order = Order(order_items)

    return order
